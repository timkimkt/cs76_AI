# Class: COSC 76
# Assignment: PA 2
# Date: Sep 30, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

from MazeworldProblem import MazeworldProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

## Test case #1: Maze 2
print("maze 2")
print("--------------------------------")
test_maze2 = Maze("maze2.maz")
test_mp = MazeworldProblem(test_maze2, (3,0))
print(test_mp.get_successors(test_mp.start_state))

# Blind robot problem with A* Search using null_heuristic
result = astar_search(test_mp, null_heuristic)
print(result)

# Blind robot problem with A* Search using manhattan_heuristic
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

########################
# Test case #2: Maze 3
print("maze 3")
print("--------------------------------")

test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
print(test_mp.get_successors(test_mp.start_state))

# Blind robot problem with A* Search using null_heuristic
result = astar_search(test_mp, null_heuristic)
print(result)

# Blind robot problem with A* Search using manhattan_heuristic
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

########################
## Test case #3: Maze 4
# print("maze 4")
# print("--------------------------------")
#
# test_maze4 = Maze("maze4.maz")
# test_mp = MazeworldProblem(test_maze4, (3, 3, 1, 3))
# print(test_mp.get_successors(test_mp.start_state))
#
# # Blind robot problem with A* Search using null_heuristic
# result = astar_search(test_mp, null_heuristic)
# print(result)
#
# # Blind robot problem with A* Search using manhattan_heuristic
# result = astar_search(test_mp, test_mp.manhattan_heuristic)
# print(result)
# test_mp.animate_path(result.path)

########################
# # Test case #4: Maze 5
# print("maze 5")
# print("--------------------------------")
#
# test_maze5 = Maze("maze5.maz")
# test_mp = MazeworldProblem(test_maze5, (4, 3, 4, 5, 1, 0))
# print(test_mp.get_successors(test_mp.start_state))
#
# # Blind robot problem with A* Search using null_heuristic
# result = astar_search(test_mp, null_heuristic)
# print(result)
#
# # Blind robot problem with A* Search using manhattan_heuristic
# result = astar_search(test_mp, test_mp.manhattan_heuristic)
# print(result)
# test_mp.animate_path(result.path)

###############################

# Other mazes that can be explored
# Note: they can take a long time

test_maze6 = Maze("maze6.maz")
test_maze7 = Maze("maze7.maz")
test_maze8 = Maze("maze8.maz")

#################################
