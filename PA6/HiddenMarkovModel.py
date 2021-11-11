import numpy as np
import random

class HiddenMarkovModel:
    def __init__(self, maze):

        self.maze_height = 0
        self.maze_width = 0
        self.maze_array = []
        self.load_maze(maze)   # loads maze and updates dimensions

        self.colors = ['red', 'green', 'yellow', 'blue']
        self.colors_map = {i:color for i, color in enumerate(self.colors)}
        self.maze_color_map = { }  # tuple to integer
        self.assign_color()
        self.colors_truth = self.gen_colors_truth()

        self.sensor_acc = 0.88
        self.sensor_err = (1-self.sensor_acc) / (len(self.colors)-1) # 0.04
        self.intial_distribution = np.ones((self.maze_height, self.maze_width)) * (1/(self.maze_width*self.maze_height))

    # def __str__(self):
    #     str = "The output: "
    #     return str +=

    def gen_colors_truth(self):
        truth = np.ones((self.maze_width, self.maze_height))
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                truth[r][c] = self.maze_color_map[(r, c)]

        return truth

    def load_maze(self, filename):

        # read the maze file into a list of strings
        f = open(filename)
        lines = []
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            else:
                lines.append(line)
        f.close()

        self.maze_width = len(lines[0])
        self.maze_height = len(lines)
        self.maze_array = list("".join(lines))

    # def rc_to_index(self, x, y):
    #     return (self.maze_height - y - 1) * self.maze_width + x

    # assume top-left x, y starts with 0, 0 (matrix convention)
    def assign_color(self):
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                self.maze_color_map[(r, c)] = random.randrange(0, len(self.colors))

    def move_robot(self, moves, start_pos):

        r, c = start_pos
        direction = [[1,0], [-1, 0], [0, 1], [0, -1]]

        result = [ ]
        movements = [ ]

        i = 0
        while i < moves:
            rand_dr, rand_dc = random.choice(direction)
            new_r, new_c = r + rand_dr, c + rand_dc
            if new_r >= 0 and new_r < self.maze_height and new_c >= 0 and new_c < self.maze_width:
                # append color if the robot has moved
                i += 1
                random_var = random.uniform(0, 1)
                if random_var >= 0.88:
                    result.append(self.maze_color_map[(new_r, new_c)])
                else:
                    other_colors = [k for k in self.colors_map.keys() if k != self.maze_color_map[(new_r, new_c)] ]
                    result.append(random.choice(other_colors))

                movements.append((rand_dr, rand_dc))

        return result, movements


    # update vector: 0.88 (sensor)

    def filter(self, sensor_reading):

        prob_dist = self.intial_distribution
        print("before", prob_dist)
        for i, color in enumerate(sensor_reading):
            pos_p = self.get_prediction_vector(color)
            next = np.zeros((self.maze_width, self.maze_height))
            for r1 in range(self.maze_height):
                for c1 in range(self.maze_width):
                    trans_model = self.get_update_vector(r1, c1)
                    m = 0
                    for r2 in range(self.maze_height):
                        for c2 in range(self.maze_width):
                            m += (trans_model[r2][c2]*prob_dist[r2][c2])
                    next[r1][c1] = m
            print("next,", next)
            pos_p += next
            prob_dist = self.normalize(pos_p)
            print(f"curr state at iteration {i}")
            print(prob_dist)
        return prob_dist

    def normalize(self, matrix):
        total_sum = 0
        h, w = matrix.shape
        norm_matrix = np.zeros((h, w))
        for r in range(h):
            for c in range(w):
                total_sum += matrix[r][c]

        for r in range(h):
            for c in range(w):
                norm_matrix[r][c] = (matrix[r][c]/total_sum)

        return norm_matrix
    # sensor model
    def get_prediction_vector(self, color):
        update_vector = np.ones((self.maze_width, self.maze_height))
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                if color == self.maze_color_map[(r,c)]:
                    update_vector[r][c] = self.sensor_acc   # 0.88
                else:
                    update_vector[r][c] = self.sensor_err   # 0.04

        return update_vector


    def product_sum(self, A, B):
        h, w = A.shape
        result = np.zeros((h, w))
        for r in range(h):
            for c in range(w):
                result[r][c] = A[r][c] * B[r][c]
        return result

    # transition model
    # def get_update_vector(self, probability):
    def get_update_vector(self, r, c):

        # prediction = np.zeros((self.maze_width, self.maze_height))
        direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        #
        # for r in range(self.maze_height):
        #     for c in range(self.maze_width):
        transition = np.zeros((self.maze_width, self.maze_height))
        for dr, dc in direction:
            new_r, new_c = r + dr, c + dc
            if not (new_r >= 0 and new_r < self.maze_height and new_c >= 0 and new_c < self.maze_width):
                new_r, new_c = r, c
            transition[new_r][new_c] += 0.25

        return transition
        # for r in range(self.maze_height):
        #     for c in range(self.maze_width):
        #         prediction[r][c] += (transition[r][c] * probability[r][c])
        #
        # return prediction

if __name__ == "__main__":
    print("Hello World")
    HMM = HiddenMarkovModel("maze1.maz")
    print(HMM.maze_array)
    print(HMM.maze_width, HMM.maze_height)
    print(HMM.intial_distribution)
    print(HMM.colors_map)
    print(HMM.maze_color_map)
    start_pos = (1, 1)
    colors_path, movement = HMM.move_robot(20, start_pos)
    print("Starting position", start_pos)
    print("Colors & Movement of Path", colors_path, movement)
    print("Filter Result: ")
    HMM.filter(colors_path)
    print("Ground Truth: ")
    print(HMM.colors_truth)


    # def filter(self, sensor_reading):
    #     prob_matrix_norm = None
    #     new_prob = self.intial_distribution
    #
    #     for i, color in enumerate(sensor_reading):
    #         predict = self.get_prediction_vector(color)
    #         update = self.get_update_vector(new_prob)
    #         print("update", update)
    #         prob_matrix = predict.dot(update)
    #         #print("prob matrix 2", prob_matrix)
    #         new_prob = prob_matrix.dot(new_prob)
    #         #print(f"After step {i}: ")
    #         #print(new_prob)
    #
    #     prob_matrix_norm = new_prob / sum(new_prob)
    #
    #     return prob_matrix_norm
