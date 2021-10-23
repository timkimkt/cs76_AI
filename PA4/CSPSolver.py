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

        #print("neigh_choices", neigh_choices)
        sorted_domain = sorted(domain[curr_var], key=lambda x: neigh_choices.get(x), reverse=True)
        domain[curr_var] = sorted_domain
        # print("domain after sort", domain)
        # print("domain[curr_var] after sort", domain[curr_var])

        return domain

    def AC_3(self, domain):
        q = deque()

        for k in self.problem.constraint.keys():
            q.append(k)
            q.append((k[1],k[0]))

        while q:
            v1, v2 = q.popleft()
            #print("popped", (v1, v2))
            if self.revise(domain, v1, v2):
                if len(domain) == 0:
                ## if len(self.problem.domain[v1]) == 0:
                    return False
                for neigh in self.problem.map_number[v1]:
                    if neigh != v2:
                        q.append((neigh, v1))

        return True

    def revise(self, domain, v1, v2):
        revised = False
        for d_v1 in domain[v1]:
        #for d_v1 in self.problem.domain[v1]:

            satisfy = False

            # self.problem.assignment[v1] = d_v1
            # if self.problem.constraint_satisfy(self.problem.assignment, v1):
            for d_v2 in domain[v2]:
            #for d_v2 in self.problem.domain[v2]:

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
            domain = self.LCV_heuristic(domain, curr_var)
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

            self.value_count += 1

            # assign value to variable
            self.problem.assignment[curr_var] = d

            # new assignment satisfy constraint
            if self.problem.constraint_satisfy(self.problem.assignment, curr_var):

                if inference:
                    domain_copy = copy.deepcopy(domain)

                # # forward checking
                # for neigh in self.problem.map_number[curr_var]:                #
                #     if self.problem.unassigned(self.problem.assignment[neigh]) and d in domain_copy[neigh]:
                #         domain_copy[neigh].remove(d)

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

#######
    # state is being passed as a list
    # Choose the variable with the fewest legal values
    # def MRV_heuristic(self, state, domain, tiebreak=False):
    #     #print("in mrv", domain)
    #     # remaining values, associated variable
    #     MRV, min_var = float('inf'), 0
    #     tied = [ ]
    #
    #     # for all unassigned variables
    #     for i, v in enumerate(self.problem.assignment):
    #
    #         # check if this variable is unassigned
    #         if self.problem.unassigned(v):
    #
    #             # if domain is less than current MRV
    #             if len(domain[i]) <= MRV:
    #                 print("MRV selects", i,"with domain", domain[i])
    #                 # update RMV and associated variable
    #                 MRV, min_var = len(domain[i]), i
    #
    #             # rv = 0
    #             # try assigning possible domain values
    #             # for d in domain[i]:
    #             ### for d in self.problem.domain:
    #                 # print(state)
    #                 # state[i] = d
    #                 # increment count if it is legal
    #                 # if self.problem.constraint_satisfy(state, i):
    #                 #     rv += 1
    #                 # # reset assignment
    #                 # state[i] = self.problem.domain[-1]
    #                 # print("how about", domain)
    #                 # print("changed?", self.problem.domain)
    #                 ### state[i] = self.problem.domain[-1]
    #             # if current count is greater than max
    #     #         if tiebreak and rv == MRV:
    #     #             tied.append(i)
    #     #
    #     #         elif rv < MRV:
    #     #             # record MRV and variable
    #     #             MRV, min_var = rv, i
    #     #             #print("tied: ", tied)
    #     #             if tiebreak:
    #     #                 tied = [ ]
    #     #                 tied.append(i)
    #     #
    #     # #print("tied: ", tied)
    #     # if tiebreak and len(tied) > 1:
    #     #     for i in tied:
    #     #         max_const, max_var = float('-inf'), 0
    #     #         for d in domain:
    #     #         ### for d in self.problem.domain:
    #     #             state[i] = d
    #     #             curr_const, curr_var = self.Degree_heuristic(state)
    #     #             if curr_const > max_const:
    #     #                 max_const, max_var = curr_const, curr_var
    #     #
    #     #             state[i] = self.problem.domain[-1]
    #     #
    #     #         return max_var
    #
    #     return min_var
    #
    # def Degree_heuristic(self, state):
    #
    #     assigned = [ ]
    #     max_const, max_var = float('-inf'), 0
    #
    #     for i, v in enumerate(state):
    #
    #         if not self.problem.unassigned(v):
    #             assigned.append(i)
    #
    #     for i, v in enumerate(state):
    #
    #         if self.problem.unassigned(v):
    #             subtracted = [c for c in self.problem.map_number[i] if c not in assigned]
    #             if len(subtracted) > max_const:
    #                 max_const, max_var = len(subtracted), i
    #
    #     return max_const, max_var
    #
    # # pick domain that rules out the fewest values in remaining values
    # def LCV_heuristic(self, domain, curr_var):
    #
    #     LCV_domain = {}
    #     print(curr_var,"domain in LCV", domain)
    #     # try assign domain for unassigned var
    #     for d1 in domain[curr_var]:
    #     ## for d1 in self.problem.domain[curr_var]:
    #         illegal_count = 0
    #
    #         self.problem.assignment[curr_var] = d1
    #
    #         for i, v in enumerate(self.problem.assignment):
    #
    #             # for unassigned variables
    #             if self.problem.unassigned(v):
    #                 for d2 in domain[i]:
    #                 ###for d2 in self.problem.domain[i]:
    #                     # assign value to variable
    #                     self.problem.assignment[i] = d2
    #
    #                     # count legal domain for remaining variables
    #                     # increment count if it is legal
    #                     if not self.problem.constraint_satisfy(self.problem.assignment, i):
    #                         illegal_count += 1
    #                     # reset assignment
    #                     self.problem.assignment[i] = self.problem.domain[-1]
    #
    #         self.problem.assignment[curr_var] = self.problem.domain[-1]
    #         #print("adding, ", d1, "to LCV")
    #         LCV_domain[d1] = illegal_count
    #
    #     # print("DICT", LCV_domain)
    #     sorted_domain = [k for k, v in sorted(LCV_domain.items(), key=lambda i: i[1])]
    #     # print("sorted domain", sorted_domain, domain)
    #     return sorted_domain

    # # return variable with most number of unassigned
    # def Degree_heuristic(self, state):
    #
    #     assigned = [ ]    # list of variables already assigned
    #     max_const, max_var = float('-inf'), 0
    #
    #     # constraints dict -> if var in pair: count len of constraint
    #     # count constraint for each variable (lower constraint --> fewer legal values)
    #     # check all pair of each variable
    #
    #     for i, v in enumerate(state):
    #         # for variables that are assigned
    #         if not self.problem.unassigned(v):
    #             assigned.append(i)          # add to list
    #
    #     for i, v in enumerate(state):
    #         # for variables that are not assigned
    #         if self.problem.unassigned(v):
    #
    #             # add to subtracted list neighbors of unassigned var that have not been assigned
    #             unassigned_neigh = [c for c in self.problem.map_number[i] if c not in assigned]
    #
    #             if len(unassigned_neigh) > max_const:
    #                 max_const, max_var = len(unassigned_neigh), i
    #
    #     return max_const, max_var
    #
    # LCV_domain = {}
    # print(curr_var, "domain in LCV", domain)
    #
    # # try assign domain for unassigned var
    # for d1 in domain[curr_var]:
    #     ## for d1 in self.problem.domain[curr_var]:
    #     # illegal_count = 0
    #     constraint_count = 0
    #     self.problem.assignment[curr_var] = d1
    #
    #     for i, v in enumerate(self.problem.assignment):
    #
    #         # for unassigned variables
    #         if self.problem.unassigned(v):
    #
    #             for d2 in domain[i]:
    #                 ###for d2 in self.problem.domain[i]:
    #                 # assign value to variable
    #                 self.problem.assignment[i] = d2
    #
    #                 # count legal domain for remaining variables
    #                 # increment count if it is legal
    #                 # if not self.problem.constraint_satisfy(self.problem.assignment, i):
    #                 #     illegal_count += 1
    #                 if self.problem.constraint_satisfy(self.problem.assignment, i):
    #                     constraint_count += 1
    #                 # reset assignment
    #                 self.problem.assignment[i] = self.problem.domain[-1]
    #
    #     self.problem.assignment[curr_var] = self.problem.domain[-1]
    #     # print("adding, ", d1, "to LCV")
    #     # LCV_domain[d1] = illegal_count
    #     LCV_domain[d1] = constraint_count
    #
    # print("DICT", LCV_domain)
    # sorted_domain = [k:[v]
    # for k, v in sorted(LCV_domain.items(), key=lambda i: i[1])]
    # sorted_domain = sorted(domain, key=lambda i: i[1])
    #
    # print("sorted domain", sorted_domain, domain)