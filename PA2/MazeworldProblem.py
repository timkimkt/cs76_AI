# Class: COSC 76
# Assignment: PA 2
# Date: Sep 30, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

from Maze import Maze
from time import sleep

class MazeworldProblem:

    # constructor
    def __init__(self, maze, goal_locations):

        self.maze = maze                               # current maze
        self.goal_locations = goal_locations           # goal coordinate of robots
        self.start_state = (0,) + tuple(maze.robotloc) # state (robot moved, coordinates,..)
        self.robot_count = len(maze.robotloc)//2       # number of robots in maze

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

    # heuristic function that calculates manhatten distance
    def manhattan_heuristic(self, curr_state):

        man_total = 0
        # for each coordinate in state
        for i in range(1, len(curr_state)):
            # sum difference in absolute value of coordinates
            man_total += abs(curr_state[i] - self.goal_locations[i-1])

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

    # returns successors of given state
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

        # coordinate of robot being currently moved
        x, y = robot_list[robot_moved]

        # increment 1 to get to next robot that needs to be moved
        robot_to_move = robot_moved + 1 if robot_moved + 1 < self.robot_count else 0

        # unless we are at the goal state
        if not self.goal_test(state):
            # while the robot to be moved has already eached the goal state
            while ((self.goal_locations[2*robot_to_move], self.goal_locations[2*robot_to_move+1])
                   == robot_list[robot_to_move]):
                # keep incrementing to the next robot, resetting to 0 if we are end
                robot_to_move = robot_to_move + 1 if robot_to_move + 1 < self.robot_count else 0

        # for each of 5 possible directions
        for dx, dy in directions:

            # calculate new coordinates
            new_x, new_y = x + dx, y + dy

            # if the robot has not moved or has moved to a floor not occupied by another robot
            if (new_x == x and new_y == y) or (self.maze.is_floor(new_x, new_y) and not self.maze.has_robot(new_x, new_y)):
                # update coordinate of robot that was moved
                robot_list[robot_moved] = (new_x, new_y)
                # create tuple to add to successors
                res = (robot_to_move, )
                # concat robot coordinates to state
                for i in range(len(robot_list)):
                    res += robot_list[i]
                # append current state to successors
                successors.append(res)

        return successors

    def goal_test(self, state):
        # the first element in state is the robot moved
        return state[1:] == self.goal_locations


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    #print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
    print(test_mp.get_successors((0, 1, 3, 1, 2, 2, 1)))
