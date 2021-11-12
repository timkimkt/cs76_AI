# Class: COSC 76
# Assignment: PA 6
# Date: Nov 11, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

import numpy as np
import random

class HiddenMarkovModel:
    def __init__(self, maze, start_pos):

        self.maze_height = 0
        self.maze_width = 0
        self.maze_array = self.load_maze(maze)   # loads maze and updates dimensions
        self.colors = ['Red', 'Green', 'Yellow', 'Blue']
        self.colors_map = {i:color for i, color in enumerate(self.colors)}
        self.maze_color_map = {}  # tuple to integer
        self.assign_color()
        self.colors_truth = self.gen_colors_truth(False) # true for int / false for str

        self.start_pos = start_pos
        self.locations = []
        self.locations.append(start_pos)

        self.sensor_acc = 0.88
        self.sensor_err = (1-self.sensor_acc) / (len(self.colors)-1) # 0.04
        self.intial_distribution = np.ones((self.maze_height, self.maze_width)) * (1/(self.maze_width*self.maze_height))

    # def __str__(self):
    #     str = "The output: "
    #     return str +=


    # read the maze file into a list of strings
    def load_maze(self, filename):

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
        # update maze dimensions
        self.maze_width = len(lines[0])
        self.maze_height = len(lines)

        return list("".join(lines))

    # def rc_to_index(self, x, y):
    #     return (self.maze_height - y - 1) * self.maze_width + x

    # randomly assign colors (integers) into each cell
    # assume top-left x, y starts with 0, 0 (matrix convention)
    def assign_color(self):
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                self.maze_color_map[(r, c)] = random.randrange(0, len(self.colors))

    # create a map of a true colors of the maze cells
    def gen_colors_truth(self, integer=False):
        truth = np.ones((self.maze_width, self.maze_height), dtype='str')
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                if integer:
                    truth[r][c] = self.maze_color_map[(r, c)]
                else:
                    truth[r][c] = self.colors[self.maze_color_map[(r, c)]]

        return truth

    # move the robot for a given number of steps from given position
    def move_robot(self, steps):

        #####
        direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        result = [ ]
        #movements = [ ]

        i = 0
        while i < steps:
            r, c = self.locations[-1]
            # move in random direction
            rand_dr, rand_dc = random.choice(direction)
            #print("rand move", rand_dr, rand_dc)
            new_r, new_c = r + rand_dr, c + rand_dc

            # check if the new position is within bounds
            if self.is_floor(new_r, new_c):
            #if new_r >= 0 and new_r < self.maze_height and new_c >= 0 and new_c < self.maze_width:
                i += 1
                random_var = random.uniform(0, 1)

                # accurately sense the color with 0.88 accuracy
                if random_var <= 0.88:
                    result.append(self.maze_color_map[(new_r, new_c)])

                # otherwise choose from remaining colors
                else:
                    other_colors = [k for k in self.colors_map.keys() if k != self.maze_color_map[(new_r, new_c)] ]
                    result.append(random.choice(other_colors))

                # keep track of actual movments
                #movements.append((rand_dr, rand_dc))
                self.locations.append((new_r, new_c))
        # result is color sequence (reflects sensor inaccuracy)
        # movements is the sequence of movements
        # new_r, new_c is the final position of the robot
        return result, self.locations
        #return result, movements, (new_r, new_c)

    def is_floor(self, r, c):
        if r >= 0 and r < self.maze_height and c >= 0 and c < self.maze_width:
            return self.maze_array[r * self.maze_width + c] == "."
        return False

    # sensor model
    # probability distribution given a single color reading
    def get_prediction_vector(self, color):

        update_vector = np.ones((self.maze_width, self.maze_height))

        for r in range(self.maze_height):
            for c in range(self.maze_width):
                # if sensor reading matches color of maze
                if color == self.maze_color_map[(r,c)]:
                    update_vector[r][c] = self.sensor_acc   # 0.88 probability
                # if sensor reading is different
                else:
                    update_vector[r][c] = self.sensor_err   # 0.04 probability

        return update_vector

    # transition model
    # probability distribution from a given cell location
    def get_update_vector(self, r, c):

        direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        transition = np.zeros((self.maze_width, self.maze_height))

        for dr, dc in direction:
            new_r, new_c = r + dr, c + dc
            # stay at current cell if out of bounds
            if not (new_r >= 0 and new_r < self.maze_height and new_c >= 0 and new_c < self.maze_width):
                new_r, new_c = r, c
            transition[new_r][new_c] += 0.25

        return transition


    def filter(self, sensor_reading):

        prob_dist = self.intial_distribution

        print("Initial Location")
        self.print_robotloc(0)
        print("(r, c) =", self.locations[0])
        print("-----------------------------------------------------------------------------")

        # for each sensor reading
        for i, color in enumerate(sensor_reading):
            position_prob = self.get_prediction_vector(color)
            # DEBUG:
            # print("position prob:")
            # print(position_prob)
            next = np.zeros((self.maze_width, self.maze_height))

            for r1 in range(self.maze_height):
                for c1 in range(self.maze_width):
                    trans_model = self.get_update_vector(r1, c1)
                    # DEBUG:
                    # print("transition model:")
                    # print(trans_model)
                    m = 0
                    for r2 in range(self.maze_height):
                        for c2 in range(self.maze_width):
                            m += (trans_model[r2][c2]*prob_dist[r2][c2])

                    # print('m', m, (trans_model * prob_dist).sum())
                    next[r1][c1] = m

                    # DEBUG:
                    # print("next: ")
                    # print(next)
            position_prob += next
            prob_dist = self.normalize(position_prob)
            # print prob distrib at every iteration (sensor reading)
            print(f"Prob Distribution after {i+1} x filter")
            np.set_printoptions(precision=3)
            print(prob_dist)

            self.print_robotloc(i+1)
            print("location: ", self.locations[i+1])
            print("Sensed color:", self.colors_map[color], "// Actual color:",
                  self.colors_map[self.maze_color_map[self.locations[i+1]]])
            print(self.colors_truth)
            print("-----------------------------------------------------------------------------")
        return prob_dist

    # helper function that returned normalized matrix
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

    def print_robotloc(self, i):

        s = ""
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                if (r, c) == self.locations[i]:
                    s += "R"
                else:
                    s += self.maze_array[r*self.maze_width + c]

            s += "\n"

        print(s)

    # def product_sum(self, A, B):
    #     h, w = A.shape
    #     result = np.zeros((h, w))
    #     for r in range(h):
    #         for c in range(w):
    #             result[r][c] = A[r][c] * B[r][c]
    #     return result


if __name__ == "__main__":
    HMM = HiddenMarkovModel("maze1.maz", start_pos=(1, 2))
    print("Intial distribution: ")
    print(HMM.intial_distribution)
    print("-----------------------------------------------------------------------------")

    # print(HMM.colors_map)

    #colors_path, movement, final_pos = HMM.move_robot(steps_no, start_pos)
    colors_path, positions = HMM.move_robot(steps=20)
    #print("Starting position", start_pos)

    print("Filter Result: ")
    print("-----------------------------------------------------------------------------")

    HMM.filter(colors_path)

    print("Colors sequence", colors_path)
    print("Robot positions", positions)
    #print("Robot path", movement)
    #print("Final position", final_pos)

    #print("Ground Truth: ")
    #print(HMM.colors_truth)
