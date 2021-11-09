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

    def rc_to_index(self, x, y):
        return (self.maze_height - y - 1) * self.maze_width + x

    def assign_color(self):
        for x in range(self.maze_width):
            for y in range(self.maze_height-1, -1, -1):
                self.maze_color_map[(x, y)] = random.randrange(0, len(self.colors))

    # assume bottom-left x, y starts with 0, 0
    def move_robot(self, moves, start_pos):

        x, y = start_pos
        direction = [[1,0], [-1, 0], [0, 1], [0, -1]]

        result = [ ]
        # movements = [ ]

        i = 0
        while i < moves:
            rand_dx, rand_dy = random.choice(direction)
            new_x, new_y = x + rand_dx, y + rand_dy
            if new_x >= 0 and x < self.maze_width and y >= 0 and y < self.maze_height:
                # append color if the robot has moved
                i += 1
                result.append(self.maze_color_map[(new_x, new_y)])
                # movements.append((rand_dx, rand_dy))

        return result

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

    # update vector: 0.88 (sensor)

    # for each sensor reading:
    #     get prediction vector
    #     get update vector
    #     multiply them
    #     normalize

    def get_update_vector(self, color):
        update_vector = np.ones((self.maze_width, self.maze_height))
        for x in range(self.maze_width):
            for y in range(self.maze_height):




    def state_transition(self):

        trans_matrix = np.zeros((16, 16))


        pass

    def sensor_model(self):
        pass

if __name__ == "__main__":
    print("Hello World")
    HMM = HiddenMarkovModel("maze1.maz")
    print(HMM.maze_array)
    print(HMM.maze_width, HMM.maze_height)
    print(HMM.intial_distribution)
    print(HMM.colors_map)
    print(HMM.maze_color_map)
    print(HMM.move_robot(4, (1, 1)))
