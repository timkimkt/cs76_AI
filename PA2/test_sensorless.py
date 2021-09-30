# Class: COSC 76
# Assignment: PA 2
# Date: Sep 30, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

from SensorlessProblem import SensorlessProblem
from Maze import Maze
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

########################
## Test case #1: Maze 3
test_maze3 = Maze("maze3.maz")
test_mp = SensorlessProblem(test_maze3)
print(test_mp.get_successors(test_mp.start_state))

# Blind robot problem with A* Search using null_heuristic
result = astar_search(test_mp, null_heuristic)
print(result)

# Blind robot problem with A* Search using blind_heuristic
result = astar_search(test_mp, test_mp.blind_heuristic)
print(result)
test_mp.animate_path(result.path)  # animate path returned

########################
## Test case #2: Maze 4
#
# test_maze4 = Maze("maze4.maz")
# test_mp = SensorlessProblem(test_maze4)
# print(test_mp.get_successors(test_mp.start_state))
#
# # Blind robot problem with A* Search using null_heuristic
# result = astar_search(test_mp, null_heuristic)
# print(result)
#
# # Blind robot problem with A* Search using blind_heuristic
# result = astar_search(test_mp, test_mp.blind_heuristic)
# print(result)
# test_mp.animate_path(result.path)  # animate path returned


########################
## Test case #3: Maze 5
#
# test_maze5 = Maze("maze5.maz")
# test_mp = SensorlessProblem(test_maze5)
# print(test_mp.get_successors(test_mp.start_state))
#
# # Blind robot problem with A* Search using null_heuristic
# result = astar_search(test_mp, null_heuristic)
# print(result)
#
# # Blind robot problem with A* Search using blind_heuristic
# result = astar_search(test_mp, test_mp.blind_heuristic)
# print(result)
# test_mp.animate_path(result.path)  # animate path returned


########################
# Test case #4: Maze 6
#
# test_maze6 = Maze("maze6.maz")
# test_mp = SensorlessProblem(test_maze6)
# print(test_mp.get_successors(test_mp.start_state))
#
# # Blind robot problem with A* Search using null_heuristic
# result = astar_search(test_mp, null_heuristic)
# print(result)
#
# # Blind robot problem with A* Search using blind_heuristic
# result = astar_search(test_mp, test_mp.blind_heuristic)
# print(result)
# test_mp.animate_path(result.path)  # animate path returned