from collections import deque

class CSPSolver():
    def __init__(self, ProblemType, mrv=False):

        self.problem = ProblemType

        # turning on/off heuristics
        self.mrv = mrv

        # variable for no heuristic
        self.i = -1

        self.initial = True

        self.backtrack_count = 0

    # state is being passed as a list
    def MRV_heuristic(self, state, tiebreak=False):

        # remaining values, associated variable
        MRV, min_var = float('inf'), 0
        tied = [ ]

        # for all unassigned variables
        for i, v in enumerate(self.problem.assignment):

            if self.problem.unassigned(v):
                rv = 0
                # try assigning possible domain values
                for d in self.problem.domain:
                    state[i] = d
                    # increment count if it is legal
                    if self.problem.constraint_satisfy(state, i):
                        rv += 1
                    # reset assignment
                    state[i] = self.problem.domain[-1]
                # if current count is greater than max
                if tiebreak and rv == MRV:
                    tied.append(i)

                elif rv < MRV:
                    # record MRV and variable
                    MRV, min_var = rv, i
                    #print("tied: ", tied)
                    if tiebreak:
                        tied = [ ]
                        tied.append(i)

        #print("tied: ", tied)
        if tiebreak and len(tied) > 1:
            for i in tied:
                max_const, max_var = float('-inf'), 0
                for d in self.problem.domain:
                    state[i] = d
                    curr_const, curr_var = self.Degree_heuristic(state)
                    if curr_const > max_const:
                        max_const, max_var = curr_const, curr_var

                    state[i] = self.problem.domain[-1]

                return max_var

        return min_var

    def Degree_heuristic(self, state):

        assigned = [ ]
        max_const, max_var = float('-inf'), 0

        for i, v in enumerate(state):

            if not self.problem.unassigned(v):
                assigned.append(i)

        for i, v in enumerate(state):

            if self.problem.unassigned(v):
                subtracted = [c for c in self.problem.map_number[i] if c not in assigned]
                if len(subtracted) > max_const:
                    max_const, max_var = len(subtracted), i

        return max_const, max_var

    # pick domain that rules out the fewest values in remaining values
    def LCV_heuristic(self, unassigned_var):

        LCV_domain = {}

        # try assign domain for unassigned var
        for d1 in self.problem.domain[unassigned_var]:
            illegal_count = 0

            self.problem.assignment[unassigned_var] = d1

            for i, v in enumerate(self.problem.assignment):

                # for unassigned variables
                if self.problem.unassigned(v):
                    for d2 in self.problem.domain[i]:
                        # assign value to variable
                        self.problem.assignment[i] = d2

                        # count legal domain for remaining variables
                        # increment count if it is legal
                        if not self.problem.constraint_satisfy(self.problem.assignment, i):
                            illegal_count += 1
                        # reset assignment
                        self.problem.assignment[i] = self.problem.domain[-1]

            self.problem.assignment[unassigned_var] = self.problem.domain[-1]
            #print("adding, ", d1, "to LCV")
            LCV_domain[d1] = illegal_count

        #print("DICT", LCV_domain)
        sorted_domain = [k for k, v in sorted(LCV_domain.items(), key=lambda i: i[1])]
        #print("sorted domain", sorted_domain)
        return sorted_domain


    def no_heuristic(self):
        self.i += 1
        return self.i if self.i < len(self.problem.assignment) else 0

    def AC_3(self):
        q = deque()

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

        return revised



    def backtrack(self, MRV, Degree, LCV, Tiebreak=False):
    # def backtrack(self):

        self.problem.assignment = list(self.problem.assignment)
        #print("BackTrack: ", self.problem)

        # check if all the variables have been assigned
        if self.problem.assignment_complete():
            self.backtrack_count += 1
            print("Backtrack called ", self.backtrack_count, "times... ")
            #print("complete", self.problem.assignment)
            return tuple(self.problem.assignment)

        #unassigned_var = self.MRV_heuristic(self.problem.assignment)
        #unassigned_var = self.Degree_heuristic(self.problem.assignment)
        # unassigned_var = self.no_heuristic()

        # # uncomment each heurisitc
        if MRV:
            unassigned_var = self.MRV_heuristic(self.problem.assignment, Tiebreak)

            if MRV and Tiebreak:
                print("MRV selected with Tiebreak (Degree)") if self.initial else None

            else:
                print("MRV selected") if self.initial else None
            #self.initial = False

        elif Degree:
            print("Degree selected") if self.initial else None
            unassigned_var = self.Degree_heuristic(self.problem.assignment)[1]
            #self.initial = False
        else:
            print("No heuristic selected") if self.initial else None
            unassigned_var = self.no_heuristic()

        print("Selecting unassigned: ", unassigned_var)

        # sort according to LCV (unassigned var)
        if LCV:
            print("LCV heuristic selected") if self.initial else None
            self.initial = False
            domain = self.LCV_heuristic(unassigned_var)
        else:
            print("LCV not selected") if self.initial else None
            self.initial = False
            domain = self.problem.domain[unassigned_var]


        # domain = self.LCV_heuristic(unassigned_var)
        #print("heuristic domain", domain)
        # domain = self.problem.domain[unassigned_var]
        # print("non-heuristic domain", domain)

        self.backtrack_count += 1
        print("Backtrack called ", self.backtrack_count, "times... ")

        for d in domain:

            # assign value to variable
            self.problem.assignment[unassigned_var] = d
            #print("assigning", d, self.problem.assignment)

            # new assignment satisfy constraint
            if self.problem.constraint_satisfy(self.problem.assignment, unassigned_var):
                #print("constraint satisfy")

                # conduct inference (modifies domain in place)

                #self.AC_3()


                # result = self.backtrack()
                result = self.backtrack(MRV, Degree, LCV, Tiebreak)
                if result:
                    return result

            # reset variable value
            else:
                #print("not satisfy")
                # undo assignment
                self.problem.assignment[unassigned_var] = self.problem.domain[-1]

        #print('return false')
        return False


def main():
    pass

if __name__ == '__main__':
    main()