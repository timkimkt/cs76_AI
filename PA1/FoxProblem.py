# Class: COSC 76
# Assignment: PA 1
# Date: Sep 23, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.chicken_total, self.fox_total, self.boat_location = start_state
        self.boat_size = 2              # boat capacity

        # you might want to add other things to the problem,
        #  like the total number of chickens (which you can figure out
        #  based on start_state

    # get successor states for the given state
    def get_successors(self, state):
        # you write this part. I also had a helper function
        #  that tested if states were safe before adding to successor list

        # list of successors
        successors = [ ]
        # current state
        chicken, fox, boat = state

        # if the boat is on the left
        if boat == 1:

        # from minimum required to maximum capacity of boat
         for curr_boat_size in range(1, self.boat_size + 1):
                # each animal may ride 0 to max of current boat capacity
                for b in range(curr_boat_size + 1):
                    # current new state
                    new_state = (chicken - b, fox - (curr_boat_size - b), 0)
                    # add to successors if valid state
                    if self.valid_state(new_state):
                        successors.append(new_state)

        # if boat is on the right
        else:
            # from minimum required to maximum capacity of boat
            for curr_boat_size in range(1, self.boat_size + 1):
                # each animal may ride 0 to max of current boat capacity
                for b in range(curr_boat_size + 1):
                    # current new state
                    new_state = (chicken + b, fox + (curr_boat_size - b), 1)
                    # add to successors if valid state
                    if self.valid_state(new_state):
                        successors.append(new_state)

        # return list of successors
        return successors

    # helper function that checks if state is valid
    def valid_state(self, state):

        chicken, fox, boat = state
        # number of chicken and fox on the other side
        opp_chicken, opp_fox = self.chicken_total - chicken, self.fox_total - fox

        # states that are no possible (less than zero or greater than total number)
        if (chicken < 0 or fox < 0 or chicken > self.chicken_total or fox > self.fox_total):
            return False

        # states that are no possible (all animals on one side and boat on the other )
        if ((chicken == self.chicken_total and fox == self.fox_total and boat == 0) and
                (chicken == 0 and fox == 0 and boat == 1)):
            return False

        # if there are 0 number of chickens on one side (only check other side)
        if (chicken == 0 and opp_chicken >= opp_fox) or (opp_chicken == 0 and chicken >= fox):
            return True

        # return true if chicken is equal or greater than fox on both sides
        return (chicken >= fox and opp_chicken >= opp_fox)

    # I also had a goal test method. You should write one.
    def goal_test(self, state):

        # return true if current state is goal state
        return state ==self.goal_state

    def __str__(self):
        string =  "Chickens and foxes problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":

    # test case 1
    test_cp = FoxProblem((3, 3, 1))
    print(test_cp.get_successors((3, 3, 1)))
    print(test_cp)

    # test case 2
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)

    # test case 3
    test_cp = FoxProblem((5, 4, 1))
    print(test_cp.get_successors((5, 4, 1)))
    print(test_cp)
