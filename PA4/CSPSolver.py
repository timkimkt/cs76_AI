from collections import deque
import copy


class CSPSolver():
    def __init__(self, ProblemType):

        # for print statements
        self.problem = ProblemType
        self.initial = True
        self.node_count = 0
        self.value_count = 0

        # variable for no heuristic fn
        self.i = -1

        self.LCV_history = { }

    # Choose the variable with the fewest legal values
    # (i.e. the variable that will fail first)
    def MRV_heuristic(self, state, domain, tiebreak=False):

        min_count, min_var = float('inf'), 0
        tied = [ ]     # for tie-breaking

        # for all unassigned variables
        for i, v in enumerate(self.problem.assignment):
            if self.problem.unassigned(v):
                # append to tied list (if combined w/ degree)
                if len(domain[i]) == min_count and tiebreak:
                    tied.append(i)

                # if current count is less than minimum
                elif len(domain[i]) < min_count:
                    # update min count and associated variable
                    min_count, min_var = len(domain[i]), i

                    # create new list of tied variables
                    if tiebreak:
                        tied = [ ]
                        tied.append(i)

        # if degree heuristic is turned on
        if tiebreak and len(tied) > 1:
            min_var = self.Degree_heuristic(tied)

        return min_var

    # return variable involved in large number of constraints
    # also used for tie-breaking by MRV (esp. for map-coloring)
    def Degree_heuristic(self, unassigned):

        max_count, max_var = float('-inf'), 0

        # for each unassigned variable
        for i in unassigned:
            # count number of times it appears in constraint
            count = 0
            for k in self.problem.constraint:
                if i in k:
                    count += 1
            # store the maximum count and its variable
            if count > max_count:
                max_count, max_var = count, i

        return max_var

    # function for no heuristic (returns variables in order from zero)
    def no_heuristic(self):
        self.i += 1
        if self.i < len(self.problem.assignment):
            return self.i
        else:
            self.i = 0
            return self.i

    # once variable selected, reorder its domain so that
    # fewest choices for neighbor is ruled out (highest domain count)
    def LCV_heuristic(self, domain, curr_var):
        # print("domain before sort", domain)
        # print("domain[curr_var] before sort", domain[curr_var])

        neigh_choices = { }

        # for each domain of variable selected
        for d1 in domain[curr_var]:
            domain_count = 0
            # when the domain is assigned
            self.problem.assignment[curr_var] = d1
            # for each neighbor
            for neigh in self.problem.map_number[curr_var]:
                # that is unassigned
                if self.problem.unassigned(self.problem.assignment[neigh]):
                    for d2 in domain[neigh]:
                        if (curr_var, neigh) in self.problem.constraint:
                            if (d1, d2) in self.problem.constraint[(curr_var, neigh)]:
                                domain_count += 1
                        elif (neigh, curr_var) in self.problem.constraint:
                            if (d2, d1) in self.problem.constraint[(neigh, curr_var)]:
                                domain_count += 1
            neigh_choices[d1] = domain_count
            self.problem.assignment[curr_var] = self.problem.domain[0]

        # print("neigh_choices", neigh_choices)
        sorted_domain = sorted(domain[curr_var], key=lambda x: neigh_choices.get(x), reverse=True)
        domain[curr_var] = sorted_domain
        # print("domain after sort", domain)
        # print("domain[curr_var] after sort", domain[curr_var])

        return domain
        # max_val = max(neigh_choices, key= lambda x: neigh_choices.get(x))
        # # self.LCV_history
        # return max_val


    def AC_3(self, domain):
        q = deque()
        for k in self.problem.constraint.keys():
            q.append(k)
            q.append((k[1],k[0]))

        while q:
            v1, v2 = q.popleft()
            if self.revise(domain, v1, v2):
                if len(domain[v1]) == 0:
                    return False
                for neigh in self.problem.map_number[v1]:
                    if neigh != v2:
                        q.append((neigh, v1))

        return True

    def revise(self, domain, v1, v2):
        revised = False
        for d_v1 in domain[v1]:
            satisfy = False
            self.problem.assignment[v1] = d_v1
            if self.problem.constraint_satisfy(self.problem.assignment, v1):
                for d_v2 in domain[v2]:
                    self.problem.assignment[v2] = d_v2
                    if self.problem.constraint_satisfy(self.problem.assignment, v2):
                        satisfy = True

            if not satisfy:
                domain[v1].remove(d_v1)
                revised = True

        return revised


    def backtrack(self, domain, inference, MRV, Degree, LCV, Tiebreak=False):

        # # prints number of nodes (calls to backtrack)
        self.node_count += 1

        self.problem.assignment = list(self.problem.assignment)

        # check if all the variables have been assigned
        if self.problem.assignment_complete():
            return tuple(self.problem.assignment)
        ############################### heuristics ######################################
        # activate heuristic based on boolean passed in
        if inference:
            print("Inference on") if self.initial else None

        if MRV:
            curr_var = self.MRV_heuristic(self.problem.assignment, domain, Tiebreak)
            if MRV and Tiebreak:
                print("MRV selected with Tiebreak (Degree)") if self.initial else None
            else:
                print("MRV selected") if self.initial else None

        elif Degree:
            print("Degree selected") if self.initial else None

            # add unassigned variables to list
            unassigned = [ ]
            for i, v in enumerate(self.problem.assignment):
                if self.problem.unassigned(v):
                    unassigned.append(i)
            curr_var = self.Degree_heuristic(unassigned)

        else:
            print("No variable heuristic selected") if self.initial else None
            curr_var = self.no_heuristic()

        # sort domain according to LCV
        if LCV:
            print("LCV heuristic selected") if self.initial else None
            self.initial = False
            #domain = self.LCV_heuristic(domain, curr_var)
            #d = self.LCV_heuristic(domain, curr_var)

            # Bug: if LCV is called without MRV or Degree, leads to inifite loop
            if not MRV and not Degree:
                LCV = False
        else:
            print("LCV not selected") if self.initial else None
            self.initial = False
        ############################################################################

       # print("DEBUG: domain after LCV", curr_var, domain[curr_var])
        # in domain of current variable
        for d in domain[curr_var]:
            # if LCV:
            #     d = self.LCV_heuristic(domain, curr_var)

            self.value_count += 1

            # assign value to variable
            self.problem.assignment[curr_var] = d

            # new assignment satisfy constraint
            if self.problem.constraint_satisfy(self.problem.assignment, curr_var):

                if inference:
                    domain_copy = copy.deepcopy(domain)

                # forward checking
                    for neigh in self.problem.map_number[curr_var]:                #
                        if self.problem.unassigned(self.problem.assignment[neigh]) and d in domain_copy[neigh]:
                            domain_copy[neigh].remove(d)

                # conduct inference (modifies domain in place)
                if inference:
                    self.AC_3(domain_copy)

                result = self.backtrack(domain, inference, MRV, Degree, LCV, Tiebreak)

                if result:
                    return result

                if inference:
                    domain = domain_copy

            else:
                # undo assignment
                self.problem.assignment[curr_var] = self.problem.domain[-1]

        return False


def main():
    pass

if __name__ == '__main__':
    main()