# Class: COSC 76
# Assignment: PA 6
# Date: Nov 11, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

import numpy as np
import random
import copy

class HiddenMarkovModel:
    def __init__(self, maze, start_pos):

        self.maze_height = 0
        self.maze_width = 0
        self.maze_array = self.load_maze(maze)   # loads maze and updates dimensions

        # possible colors of the maze cell
        self.colors = ['Red', 'Green', 'Yellow', 'Blue']
        self.colors_map = {i:color for i, color in enumerate(self.colors)}   # int to color
        self.maze_color_map = {}                                             # tuple to integer (color)
        self.assign_color()                               # randomly assign color to cell
        self.colors_truth = self.gen_colors_truth(integer=False)       # pass in True to print as int

        self.start_pos = start_pos         # starting (r, c) of robot
        self.locations = []                # path in terms of (r, c)
        self.locations.append(start_pos)

        self.sensor_acc = 0.88       # sensor accuracy
        self.sensor_err = (1-self.sensor_acc) / (len(self.colors)-1) # error rate for each color (0.04)
        # create uniform distribution of initial probabilities
        self.intial_distribution = np.ones((self.maze_height, self.maze_width)) * (1/(self.maze_width*self.maze_height))
        self.prob_dist_list = [ ]

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

        # return an array of the maze
        return list("".join(lines))

    # randomly assign colors (integers) into each cell
    # assume top-left x, y starts with 0, 0 (matrix convention)
    def assign_color(self):
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                self.maze_color_map[(r, c)] = random.randrange(0, len(self.colors))

    # create a map of a true colors of the maze cells
    #
    def gen_colors_truth(self, integer):
        truth = np.ones((self.maze_height, self.maze_width), dtype='str')
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                if integer:
                    truth[r][c] = self.maze_color_map[(r, c)]
                else:
                    truth[r][c] = self.colors[self.maze_color_map[(r, c)]]

        return truth

    # move the robot for a given number of steps from given position
    def move_robot(self, steps):

        direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        color_seq = [ ]

        i = 0
        while i < steps:

            # move in random direction
            r, c = self.locations[-1]
            rand_dr, rand_dc = random.choice(direction)
            new_r, new_c = r + rand_dr, c + rand_dc

            # check if the new position is within bounds and is empty floor
            if self.is_floor(new_r, new_c):
                i += 1
                random_var = random.uniform(0, 1)

                # accurately sense the color with 0.88 accuracy
                if random_var <= 0.88:
                    color_seq.append(self.maze_color_map[(new_r, new_c)])

                # otherwise choose from remaining colors
                else:
                    other_colors = [k for k in self.colors_map.keys() if k != self.maze_color_map[(new_r, new_c)] ]
                    color_seq.append(random.choice(other_colors))

                # keep track of actual positions
                self.locations.append((new_r, new_c))

        # result is color sequence (reflects sensor inaccuracy)
        # self.location contains sequence of positions
        return color_seq, self.locations

    def is_floor(self, r, c):
        if r >= 0 and r < self.maze_height and c >= 0 and c < self.maze_width:
            return self.maze_array[r * self.maze_width + c] == "."
        return False

    # sensor model
    # probability distribution given a single color reading
    def get_prediction_vector(self, color):

        update_vector = np.ones((self.maze_height, self.maze_width))

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
        transition = np.zeros((self.maze_height, self.maze_width))

        for dr, dc in direction:
            new_r, new_c = r + dr, c + dc
            # stay at current cell if out of bounds
            if not (self.is_floor(new_r, new_c)):
            #if not (new_r >= 0 and new_r < self.maze_height and new_c >= 0 and new_c < self.maze_width):
                new_r, new_c = r, c
            transition[new_r][new_c] += 0.25

        return transition


    def filter(self, sensor_reading):

        # load and print initial prob dist/robot loc
        prob_dist = self.intial_distribution
        print("Intial distribution: ")
        print(prob_dist)
        self.print_robotloc(0)
        print("Initial Location")
        print("(r, c) =", self.locations[0])
        print("-----------------------------------------------------------------------------")

        self.prob_dist_list.append(prob_dist)

        # for each sensor reading
        for i, color in enumerate(sensor_reading):
            position_prob = self.get_prediction_vector(color)
            # DEBUG:
            # print("position prob:")
            # print(position_prob)
            next = np.zeros((self.maze_height, self.maze_width))

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

            print("Difference w/ previous distriubtion: ")
            print(prob_dist-self.prob_dist_list[-1])
            self.prob_dist_list.append(prob_dist)

            # print actual robot location in maze
            print("Robot location in maze")
            self.print_robotloc(i+1)
            # print top 3 locations with highest probability
            prob_copy = copy.deepcopy(prob_dist)
            top_third = np.sort(prob_copy.flatten())[::-1][:3][-1]
            print("Locations w/ high prob")
            self.print_potential_robotloc(top_third, prob_dist)

            print("location: ", self.locations[i+1])
            print("Sensed color:", self.colors_map[color], "// Actual color:",
                  self.colors_map[self.maze_color_map[self.locations[i+1]]])
            print("Current path: ", [self.colors_map[i] for i in sensor_reading[:i+1]])
            print(self.colors_truth)
            print("-----------------------------------------------------------------------------")

        return prob_dist

    # helper function that returns normalized matrix
    def normalize(self, matrix):
        total_sum = 0
        h, w = matrix.shape
        norm_matrix = np.zeros((h, w))

        # calculate total sum
        for r in range(h):
            for c in range(w):
                total_sum += matrix[r][c]

        # divide each cell by total
        for r in range(h):
            for c in range(w):
                norm_matrix[r][c] = (matrix[r][c]/total_sum)

        return norm_matrix

    # print maze with robot
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

    # print maze with robot
    def print_potential_robotloc(self, top_third, prob_dist):
        s = ""
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                if prob_dist[r][c] >= top_third:
                    s += "$"
                else:
                    s += "."
            s += "\n"
        print(s)

if __name__ == "__main__":
    HMM = HiddenMarkovModel("maze1.maz", start_pos=(1, 2))
    # print(HMM.colors_map)
    colors_path, positions = HMM.move_robot(steps=20)
    print("-----------------------------------------------------------------------------")
    print("Hidden Markov Model Filtering: ")
    print("-----------------------------------------------------------------------------")
    HMM.filter(colors_path)

    print("Colors sequence", colors_path)
    print("Robot positions", positions)