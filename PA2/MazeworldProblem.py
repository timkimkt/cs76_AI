from Maze import Maze
from time import sleep
import math

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):

        # my addition
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = (0,) + tuple(maze.robotloc)
        self.robot_count = len(maze.robotloc)//2
        # self.manhattan_heuristic = self.manhattan_heuristic_fn()
        #print("start state:", self.start_state)
        ###

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

    # my addition
    def manhattan_heuristic(self, curr_state):

        man_total = 0

        for i in range(1, len(curr_state)-1):
            man_total += abs(curr_state[i] - self.goal_locations[i])

        return man_total


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))

    def get_successors(self, state):

        # list of successors
        successors = [ ]
        # list of tuples of robot coordinates (length == no. of robots)
        robot_list = [ ]

        # split tuple into robot being moved and coordinates
        robot_moved, robots = state[0], state[1:]

        # update robot location
        self.maze.robotloc = list(robots)

        # store all coordinates of robots
        for i in range(len(robots)//2):
            # store each coordinate as tuple
            robot_list.append((robots[2*i], robots[2*i + 1]))

        # for 5 possible actions from each state
        directions = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]]

        #print("robot moved: ", robot_moved + 1)
        # coordinate of robot being currently moved
        x, y = robot_list[robot_moved]

        robot_to_move = robot_moved + 1 if robot_moved + 1 < self.robot_count else 0
        if not self.goal_test(state):
            while ((self.goal_locations[2*robot_to_move], self.goal_locations[2*robot_to_move+1]) == robot_list[robot_to_move]):
                robot_to_move = robot_to_move + 1 if robot_to_move + 1 < self.robot_count else 0

        for dx, dy in directions:

            # new coordiante
            new_x, new_y = x + dx, y + dy

            #print("floor", self.maze.is_floor(new_x, new_y), self.maze.has_robot(new_x, new_y))
            #if self.maze.is_floor(new_x, new_y) and not self.maze.has_robot(new_x, new_y):

            # what about just moving on to the next robot?
            if (new_x == x and new_y == y) or (self.maze.is_floor(new_x, new_y) and not self.maze.has_robot(new_x, new_y)):
                #print(robot_list, "len of robot_list", len(robot_list), 2*robot_moved)
                robot_list[robot_moved] = (new_x, new_y)
                res = (robot_to_move, )
                for i in range(len(robot_list)):
                    res += robot_list[i]
                #successors.append((robot_moved,) + tuple(robot_list))
                successors.append(res)

        return successors

    def goal_test(self, state):
        return state[1:] == self.goal_locations


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    #print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
    print(test_mp.get_successors((0, 1, 3, 1, 2, 2, 1)))
