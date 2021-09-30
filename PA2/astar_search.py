# Class: COSC 76
# Assignment: PA 2
# Date: Sep 30, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):

        self.state = state            # state (robot moved, coordinates of robot1, ..etc)
        self.heuristic = heuristic    # heuristic calculated by the function (zero if UCS)
        self.parent = parent          # parent of node

        # if the robot has moved (i.e. states are different)
        if (self.parent and (self.parent.state[1:] != self.state[1:])):
            # fuel spent = 1
            self.transition_cost = 1
        else:
            # fuel spent = 0
            self.transition_cost = transition_cost

    def priority(self):
        # calculation of total cost of heappop
        return self.heuristic + self.transition_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):

    # create root node, priority queue
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)  # push root in the heap

    # create SearchSolution object to store solution
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # a dictionary that keeps of lowest total cost of states visited
    visited_cost = {}
    visited_cost[start_node.state] = 0

    # while priority queue is not empty
    while pqueue:

        # pop the node with lowest cost
        curr_node = heappop(pqueue)

        # if state has been visited but at a lower cost, we do not visit
        if curr_node.state in visited_cost and curr_node.transition_cost > visited_cost[curr_node.state]:
            continue

        # increment node visited
        solution.nodes_visited += 1

        # check if we have reached goal state (all robots in goal location)
        if search_problem.goal_test(curr_node.state):
            solution.cost = curr_node.transition_cost       # update cost (cumulative)
            solution.path = backchain(curr_node)            # update solution path
            return solution

        # for each successor state
        for child in search_problem.get_successors(curr_node.state):

            # if the node has not been visited yet
            if (child not in visited_cost):
                # create a new AstarNode with the child
                child_node = AstarNode(child, heuristic_fn(child), curr_node)
                # calculate the total cost to reaching child
                visited_cost[child_node.state] = child_node.transition_cost + curr_node.transition_cost
                # update child cost as the total cost
                child_node.transition_cost = child_node.transition_cost + curr_node.transition_cost
                # push the node into the heap
                heappush(pqueue, child_node)

            # otherwise if the child has been visited
            elif child in visited_cost:

                # calculate the total cost to reaching child
                child_total_cost = child_node.transition_cost + curr_node.transition_cost

                # if the child has been visited and we find a node with lower cost
                if child_total_cost < visited_cost[child]:

                    # create a new AstarNode and push into heap
                    child_node = AstarNode(child, heuristic_fn(child), curr_node)
                    # update the new lower cost of state
                    visited_cost[child_node.state] = child_total_cost
                    # create new AstarNode with lower cost
                    child_node.transition_cost = child_total_cost
                    # push the node into the heap
                    heappush(pqueue, child_node)

    # return if no solution found
    return solution
