from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze =  maze
        self.start_state = self.create_start_state()
        self.blind_heuristic = self.blind_heuristic_fn
    def __str__(self):
        string =  "Blind robot problem: "
        return string

    def create_start_state(self):
        res = [ ]

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    res.append((x, y))
        return tuple(res)

    def blind_heuristic_fn(self, state):
        return len(state)

    # question: so only print where the robot can go?
    def get_successors(self, state):

        # list of successors
        successors = [ ]

        # # update robot location
        # self.maze.robotloc = state

        # for 4 possible actions from each state
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for dx, dy in directions:
            state_list = list(state)
            res = set()
            for i in range(len(state)):
                # for each possible coordinate in state
                x, y = state_list[i]
                # move it in current direction
                new_x, new_y = x + dx, y + dy
                # if the new coordinate is valid
                if (self.maze.is_floor(new_x, new_y)):
                    res.add((new_x, new_y))
            successors.append(tuple(res))

        return successors


    def goal_test(self, state):
        return len(state) == 1

    # robot doesn't know if it has moved
    # def robot_moved(self, state):
    #     directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))




## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
