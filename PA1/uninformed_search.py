# Class: COSC 76
# Assignment: PA 1
# Date: Sep 23, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

# deque required for queue in BFS
from collections import deque
# SearchSolution object is required for storing and printing solution path
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    # start with depth = 0 and no parent (root node)
    def __init__(self, state, depth=0, parent=None):

        self.state = state        # state of node
        self.depth = depth        # depth of node in graph
        self.parent = parent      # parent of node

# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions

def bfs_search(search_problem):

    # queue to store frontier
    q = deque()
    # pack start state into node
    root = SearchNode(search_problem.start_state)
    # add node to frontier
    q.append(root)

    # create a SearchSoutin object to store solution and related info
    solution = SearchSolution(search_problem, "BFS")

    # keeps track of explored nodes
    visited = set()

    # while frontier is not empty
    while q:

        # get current node from frontier
        curr_node = q.popleft()
        # get current state from current node
        curr_state = curr_node.state

        # if current state is the goal
        if (search_problem.goal_test(curr_state)):
            # call backchain helper
            backchain(curr_node, solution)

        # for each child of current state
        for child in search_problem.get_successors(curr_state):
            # if the child not already visited
            if child not in visited:
                # increment number of nodes visited
                solution.nodes_visited += 1
                # pack child state into node, with backpointer to parent
                next = SearchNode(child, curr_node.depth + 1, curr_node)
                # add node to frontier
                q.append(next)
                #
                visited.add(child)

    # return SearchSolution object
    return solution

# helper function that backchains from goal to start node
def backchain(node, solution):

    # keep travelling up while node exists
    while node:
        # append node to front of solution list
        solution.path = [node.state] + solution.path
        # move up to node's parent
        node = node.parent

# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
#########

def dfs_search(search_problem, depth_limit=100, node=None, solution=None):

    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # Base case #1: return if depth limit is exceeded
    if node.depth >= depth_limit:
        return solution

    # Base case #2: backchain if current state is goal
    if (search_problem.goal_test(node.state)):
        backchain(node, solution)

    # path-checking: add current state to solution path
    solution.path.append(node.state)
    # for each child of current state
    for child in search_problem.get_successors(node.state):
        # if child is not in current path
        if child not in solution.path:
            # increment number of nodes visited
            solution.nodes_visited += 1
            # recursively call dfs on child node
            dfs_search(search_problem, depth_limit, SearchNode(child, node.depth+1, node), solution)

    # path-checking: pop current state since solution is not in this path
    solution.path.pop()

    # return SearchSolution object
    return solution

def ids_search(search_problem, depth_limit=100):

    # create a SearchSolution and node object
    solution = SearchSolution(search_problem, "IDS")
    node = SearchNode(search_problem.start_state)

    # iteratively call DFS
    for i in range(depth_limit+1):
        # SearchSolution returned from current DFS call
        curr_solution = dfs_search(search_problem, i, node, solution)
        # if solution path exists and has reached the goal state
        if curr_solution.path and curr_solution.path[-1] == (0, 0, 0):
            # return the SearchSolution object
            return curr_solution

    # return SearchSolution object (no solution is found)
    return curr_solution
