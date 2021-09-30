from MazeworldProblem import MazeworldProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# test_maze2 = Maze("maze2.maz")
# test_mp = MazeworldProblem(test_maze2, (1, 4, 1, 3))
# print("successors: ", test_mp.get_successors(test_mp.start_state))
# print(test_mp.get_successors(test_mp.start_state)

# Test problems
test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# # this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

# Your additional tests here:
# test_maze4 = Maze("maze4.maz")
# test_mp4 = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
# result4 = astar_search(test_mp4, test_mp4.manhattan_heuristic)
# print(result4)
# test_mp4.animate_path(result.path)


test_maze5 = Maze("maze5.maz")
test_maze6 = Maze("maze6.maz")
test_maze6 = Maze("maze7.maz")
test_maze6 = Maze("maze8.maz")