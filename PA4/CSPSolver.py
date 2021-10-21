class CSPSolver():
    def __init__(self, ProblemType, mrv=False):

        self.problem = ProblemType

        # turning on/off heuristics
        self.mrv = mrv


    # state is being passed as a list
    def MRV_heuristic(self, state):

        # remaining values, associated variable
        MRV, max_var = float('-inf'), 0
        # for all unassigned variables
        for i, v in enumerate(self.problem.assignment):
            ## if v == -1:
            # if v is None:
            if self.problem.unassigned(v):
                rv = 0
                # try assigning possible domain values
                for d in self.problem.domain:
                    state[i] = d
                    # increment count if it is legal
                    if self.problem.constraint_satisfy(state, i):
                        rv += 1
                    # reset assignment
                    #state[i] = -1
                    state[i] = self.problem.domain[-1]
                # if current count is greater than max
                if rv > MRV:
                    # record MRV and variable
                    MRV, max_var = rv, i

        return max_var

    # move this to constraintsatisfactionproblem
    def backtrack(self):

        self.problem.assignment = list(self.problem.assignment)
        #print("BackTrack: ", self.problem)

        # check if all the variables have been assigned
        #for a in self.problem.assignment:
        print("p", self.problem.assignment)
        #if None not in self.problem.assignment:
        if self.problem.assignment_complete():
            print("complete", self.problem.assignment)
            return tuple(self.problem.assignment)

        # if self.problem.assignment_complete():
        #     return tuple(self.problem.assignment)

        #if self.mrv:
        unassigned_var = self.MRV_heuristic(self.problem.assignment)
        #print("uassigned MRV", unassigned_var)

        #MOD: DM
        for d in self.problem.domain[unassigned_var]:
        ## for d in self.problem.domain:
            # assign value to variable
            self.problem.assignment[unassigned_var] = d
            #print("assigning", d, self.problem.assignment)


            # new assignment saitsfy constraint
            if self.problem.constraint_satisfy(self.problem.assignment, unassigned_var):
                print("constraint satisfy")

                # inference

                result = self.backtrack()
                #if result is not None:
                print(not result)
                if result:
                    print('return result')
                    return result

            # reset variable value
            else:
                ## self.problem.assignment[unassigned_var] = -1
                print("not satisfy")


                #self.problem.assignment[unassigned_var] = None
                self.problem.assignment[unassigned_var] = self.problem.domain[-1]

        #print('return false')
        return False


def main():
    pass

if __name__ == '__main__':
    main()