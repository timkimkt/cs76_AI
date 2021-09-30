from Maze import Maze
from time import sleep

class SensorlessProblem:

    # constructor
    def __init__(self, maze):
        self.maze =  maze                              # maze
        self.start_state = self.create_start_state()   # possible locations
        self.blind_heuristic = self.blind_heuristic_fn # based on no. of possible locations

    def __str__(self):
        string =  "Blind robot problem: "
        return string

    # creates a tuple of all possible robot coordinates
    def create_start_state(self):
        res = [ ]
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    res.append((x, y))
        # returns a tuple of tuples (coordinates)
        return tuple(res)

    # simple heuristic based on number of possible robot locations
    def blind_heuristic_fn(self, state):
        return len(state)

    # returns successors for given state
    def get_successors(self, state):

        # list of successors
        successors = [ ]

        # update robot location
        self.maze.robotloc = state

        # for 4 possible actions from each state
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        # for each direction
        for dx, dy in directions:
            # convert to list to append
            state_list = list(state)
            # set of possible coordinates
            res = set()
            for i in range(len(state)):
                # for each coordinate in state
                x, y = state_list[i]
                # move it in current direction
                new_x, new_y = x + dx, y + dy
                # if the new coordinate is valid
                if (self.maze.is_floor(new_x, new_y)):
                    # add to the set
                    res.add((new_x, new_y))
            # append all possible coordinates to successor
            successors.append(tuple(res))
        return successors

    # we reach goal when there is only one possible location of robot
    def goal_test(self, state):
        return len(state) == 1

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        # modified to reflect that each state is a tuple of tuples
        # (i.e. tuple of robot coordinates)
        for state in path:
            print(str(self))

            # temporary list to unpack all coordinates
            temp = [ ]
            for cx, cy in state:
                temp.extend([cx, cy])

            # robotloc now contains all possible coordinates of robots in given state
            self.maze.robotloc = tuple(temp)

            sleep(1)
            print(str(self.maze))


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
