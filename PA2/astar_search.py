from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # you write this part
        self.state = state
        self.heuristic = heuristic
        self.parent = parent

        self.transition_cost = 1 if (self.parent and (self.parent.state[1:] != self.state[1:])) else transition_cost
        # self.transition_cost = transition_cost + self.parent.transition_cost if self.parent else transition_cost

    def priority(self):
        # you write this part
        # Q: is the priority = heuristic + transition cost ?
        return self.heuristic + self.transition_cost
        #return self.heuristic(self.state)

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
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:
    while pqueue:

        curr_node = pqueue.pop()
        solution.nodes_visited += 1

        #if visited curr_node
        #heuristic = curr_node.heuristic

        if search_problem.goal_test(curr_node.state):
            solution.cost = curr_node.transition_cost
            solution.path = backchain(curr_node)
            return solution

        for child in search_problem.get_successors(curr_node.state):

            #child_total_cost = curr_node.transition_cost + visited_cost[curr_node.state]

            # if the node has not been visited yet
            if (child not in visited_cost):
                # create a new AstarNode with the child
                child_node = AstarNode(child, heuristic_fn(child), curr_node)

                # calculate the total cost to reaching child
                visited_cost[child_node.state] = child_node.transition_cost + visited_cost[curr_node.state]
                # update child cost as the total cost
                child_node.transition_cost = visited_cost[child_node.state]


                # push the node into the heap
                heappush(pqueue, child_node)
                # increment number of nodes visited
                # solution.nodes_visited += 1

            # otherwise if the child has been visited
            elif child in visited_cost:
                # calculate the total cost
                child_total_cost = child_node.transition_cost + visited_cost[curr_node.state]

                # if the child has been visited and we find a node with lower cost
                if child_total_cost < visited_cost[child]:

                    # create a new AstarNode and push into heap
                    child_node = AstarNode(child, heuristic_fn(child), curr_node)
                    heappush(pqueue, child_node)

                    # update the new lower cost
                    visited_cost[child_node.state] = child_total_cost
                    # input new cost into newly created AstarNode
                    child_node.transition_cost = visited_cost[child_node.state]
                    # increment number of nodes visited
                    # solution.nodes_visited += 1

                else:
                    # otherwise skip the node
                    continue

    return solution