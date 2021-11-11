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

        self.sensor_acc = 0.88
        self.sensor_err = (1-self.sensor_acc) / (len(self.colors)-1) # 0.04
        self.intial_distribution = np.ones((self.maze_height, self.maze_width)) * (1/(self.maze_width*self.maze_height))

    # def __str__(self):
    #     str = "The output: "
    #     return str +=

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
        # movements = [ ]

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

                # movements.append((rand_dx, rand_dy))

        return result


    # update vector: 0.88 (sensor)

    def filter(self, sensor_reading):
        prob_matrix_norm = None
        new_prob = self.intial_distribution

        for color in sensor_reading:
            predict = self.get_prediction_vector(color)
            update = self.get_update_vector()
            prob_matrix = predict.dot(update)
            new_prob = prob_matrix.dot(new_prob)

        prob_matrix_norm = new_prob / sum(new_prob)

        return prob_matrix_norm
        #
        #     get prediction vector
        #     get update vector
        #     multiply them
        #     normalize

    # sensor model
    def get_prediction_vector(self, color):
        update_vector = np.ones((self.maze_width, self.maze_height))
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                print(color, r, c, self.maze_color_map.keys())
                if color == self.maze_color_map[(r,c)]:
                    update_vector[r][c] = self.sensor_acc   # 0.88
                else:
                    update_vector[r][c] = self.sensor_err   # 0.04

        return update_vector

    # transition model
    def get_update_vector(self):

        prediction = np.zeros((self.maze_width, self.maze_height))
        direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for r in range(self.maze_height):
            for c in range(self.maze_width):
                transition = np.zeros((self.maze_width, self.maze_height))
                for dr, dc in direction:
                    new_r, new_c = r + dr, c + dc
                    if not (new_r >= 0 and new_r < self.maze_width and new_c >= 0 and new_c < self.maze_height):
                        new_r, new_c = r, c
                    #transition[new_r][new_c] += 1.0
                    transition[new_r][new_c] += 0.25

                #transition_norm = transition / sum(transition)
                #transition_norm *= self.intial_distribution[r][c]
                prediction += transition

        return prediction

    # transition/prediction vector: xt+1, xt

    # prediction = zero vector - running sum
    # loop through every point
    #     transition vector  zero vector
    #     loop through NESW directions:
    #         get next_point
    #         add 1.0 to that point's probability in the transition vector
    #     noramlize transition vector
    #     transition vector x point probability
    #     preidction vector + transition vector


if __name__ == "__main__":
    print("Hello World")
    HMM = HiddenMarkovModel("maze1.maz")
    print(HMM.maze_array)
    print(HMM.maze_width, HMM.maze_height)
    print(HMM.intial_distribution)
    print(HMM.colors_map)
    print(HMM.maze_color_map)
    colors_path = HMM.move_robot(4, (1, 1))
    print("Colors path", colors_path)
    print("Filter result: ")
    print(HMM.filter(colors_path))

# for c in sensor_readings:
   ## predict
   # pos_p = [0.88, 0.04]
   # for w, for l:
      # trans_moel = [0.5, 0.25, 00]
      # m = for each cell: trasn_model[cell] x curr_state[cell
      # sum (m)
      # next[w][l] = sum(m)

   # pos_p += np.array(next)
   # curr_sate = noramlize(pos_p)    ( curr state --> 0.0625, 0.0625)
   # print
