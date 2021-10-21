from collections import deque

class CSPSolver():
    def __init__(self, ProblemType, mrv=False):

        self.problem = ProblemType

        # turning on/off heuristics
        self.mrv = mrv

        # variable for no heuristic
        self.i = -1

    # state is being passed as a list
    def MRV_heuristic(self, state):

        # remaining values, associated variable
        MRV, min_var = float('inf'), 0
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
                if rv < MRV:
                    # record MRV and variable
                    MRV, min_var = rv, i

        return min_var

    def AC_3(self):
        q = deque()
        #print("Q", q)
        #self.problem.constraint.keys()
        for k in self.problem.constraint.keys():
            q.append(k)
            q.append((k[1],k[0]))
        while q:
            v1, v2 = q.popleft()
            #print("popped", (v1, v2))
            if self.revise(v1, v2):
                if len(self.problem.domain[v1]) == 0:
                    return False
                for neigh in self.problem.map_number[v1]:
                    if neigh != v2:
                        q.append((neigh, v1))
        return True

    def revise(self, v1, v2):
        revised = False
        for d_v1 in self.problem.domain[v1]:

            satisfy = False

            # self.problem.assignment[v1] = d_v1
            # if self.problem.constraint_satisfy(self.problem.assignment, v1):

            for d_v2 in self.problem.domain[v2]:

                # self.problem.assignment[v2] = d_v2
                # if self.problem.constraint_satisfy(self.problem.assignment, v2):
                #     satisfy = True
                if (v1, v2) in self.problem.constraint:
                    if (d_v1, d_v2) in self.problem.constraint[(v1, v2)]:
                        satisfy = True
                if (v2, v1) in self.problem.constraint:
                    if (d_v2, d_v1) in self.problem.constraint[(v2, v1)]:
                        satisfy = True

                # self.problem.assignment[v2] = self.problem.domain[-1]
            # self.problem.assignment[v1] = self.problem.domain[-1]

            if not satisfy:
                self.problem.domain[v1].remove(d_v1)
                revised = True

        if revised:
            print('revised! ')
        return revised

    def no_heuristic(self):
        self.i += 1
        return self.i if self.i < len(self.problem.assignment) else 0

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
        #unassigned_var = self.no_heuristic()
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

                # conduct inference (modifies domain in place)
                self.AC_3()

                result = self.backtrack()
                #if result is not None:
                if result:
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