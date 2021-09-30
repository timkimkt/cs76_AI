from SensorlessProblem import SensorlessProblem
from Maze import Maze
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems

test_maze3 = Maze("maze3.maz")
test_mp = SensorlessProblem(test_maze3)
print(test_mp.get_successors(test_mp.start_state))



# # this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# # this should do a bit better:
result = astar_search(test_mp, test_mp.blind_heuristic)
print(result)
test_mp.animate_path(result.path)

# Your additional tests here:
# You write this:
