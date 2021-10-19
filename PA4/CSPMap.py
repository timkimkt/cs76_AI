class CSPMap():
    def __init__(self, variable, domain, map):
        self.var_to_region = {}
        self.var_to_domain = {}

        self.variable = self.assign_var(variable)
        self.domain = self.assign_domain(domain)

        self.var_to_region_rev = {v: k for k, v in self.var_to_region.items()}


        self.map_number = self.map_text_to_number(map)

        self.constraint = self.generate_constraint()
        self.assignment = (-1,-1,-1,-1,-1,-1,-1) # default assignment


    def map_text_to_number(self, map):

        output = { }

        for region in map.keys():
            output[self.var_to_region_rev[region]] = []
            for other in map[region]:
                output[self.var_to_region_rev[region]].append(self.var_to_region_rev[other])

        return output

    def assign_var(self, variable):
        #self.var_to_region = { }
        variables = [ ]

        i = 0
        for v in variable:
            variables.append(i)
            self.var_to_region[i] = v
            i += 1

        return variables

    def assign_domain(self, domain):
        domains = []
        self.var_to_domain[-1] = "Unassigned"

        i = 0
        for d in domain:
            domains.append(i)
            self.var_to_domain[i] = d
            i += 1

        return domains

    def __str__(self):
        res = [ ]

        for i,v in enumerate(self.assignment):
            if v == -1:
                res.append(str(self.var_to_region[i]) + ": Unassigned")
                continue

            res.append(str(self.var_to_region[i]) + ": " + str(self.var_to_domain[v]))

        string = "Assignment:  " + str(res)
        return string

    def generate_constraint(self):

        # self.constraint
        output = { }
        # assume variable is an array of integer
        # for each pair of variables
        # for key in self.map.keys():
        #     for val in self.map[key]:
        #         if (val, key) not in output:
        #             # create a list to store constraints
        #             output[(key, val)] = [ ]
        #             # append possible pair of domain values
        #             # switched pairs can also work
        #             for m in range(1, len(self.domain)):
        #                 for n in range(0, m):
        #                     output[(key, val)].append((n, m))
        #                     output[(key, val)].append((m, n))
        #
        # return output

        # assume variable is an array of integer
        #for each pair of variables
        for r1 in self.map_number:
            for r2 in self.map_number[r1]:
                if (r2, r1) not in output:
                    # create a list to store constraints
                    output[(r1, r2)] = [ ]
                    # append possible pair of domain values
                    # switched pairs can also work
                    for m in range(1, len(self.domain)):
                        for n in range(0, m):
                            output[(r1, r2)].append((n, m))
                            output[(r1, r2)].append((m, n))

        return output

    def constraint_satisfy(self, state, var):

        # for all neighbors of variable that has just been assigned
        for neigh in self.map_number[var]:
            # Debug: print('neig', self.var_to_region[neigh])
            # skip if neighbor has not been assigned
            if state[neigh] != -1:

                # check both pairs in the constraint

                if (var, neigh) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[var], state[neigh]) not in self.constraint[(var, neigh)]:
                        return False

                elif (neigh, var) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[neigh], state[var]) not in self.constraint[(neigh, var)]:
                        return False

        return True
        # for i, v in enumerate(state):
        #     # if variable assigned
        #     if v != -1:
        #         key = (self.var_to_region[var], self.var_to_region[v])
        #         key_r = (self.var_to_region[v], self.var_to_region[var])
        #
        #         if key in self.constraint:
        #             print("check if this works", key, self.var_to_domain[state[var]], self.var_to_domain[state[v]])
        #             if (state[var], state[v]) not in self.constraint[key]:
        #                 print('no!')
        #                 return False
        #             return True
        #         elif key_r in self.constraint:
        #             print("check if this works", key, self.var_to_domain[state[v]], self.var_to_domain[state[var]])
        #
        #             if (state[v], state[var]) not in self.constraint[key_r]:
        #                 print('no!')
        #
        #                 return False
        #             return True
        # return True

    # state is being passed as a list
    def MRV_heuristic(self, state):
        MRV, max_var = float('-inf'), 0
        for i in range(len(self.assignment)):
            if self.assignment[i] == -1:
                rv = 0
                for d in range(len(self.domain)):
                    state[i] = d
                    #print("exploring assignment", self.assignment)

                    if self.constraint_satisfy(state, i):
                        rv += 1
                    state[i] = -1
                if rv > MRV:
                    MRV = rv
                    max_var = i
        return max_var

    # move this to constraintsatisfactionproblem
    def backtrack(self):

        self.assignment = list(self.assignment)
        print("BackTrack: ", self)

        # check if all the variables have been assigned
        if -1 not in self.assignment:
            return tuple(self.assignment)

        # unassigned var
        unassigned_var = self.MRV_heuristic(self.assignment)
        print("uassigned MRV", unassigned_var)


        for d in self.domain:
            # assign value to variable
            self.assignment[unassigned_var] = d
            #print("assigning d", self.assignment)


            # new assignment saitsfy constraint
            if self.constraint_satisfy(self.assignment, unassigned_var):
                #print("constraint satisfy")

                # inference

                result = self.backtrack()
                if not result:
                    #print('return result')
                    return result

            # reset variable value
            else:
                self.assignment[unassigned_var] = -1

        #print('return false')
        return False



def main():
    regions = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
    colors = ["red", "green", "blue"]
    var_map = {"WA": ["NT", "SA"], "NT": ["WA", "SA", "Q"], "Q": ["NT", "SA", "NSW"],
           "NSW": ["Q", "SA", "V"], "V": ["NSW", "SA"], "SA": ["WA", "NT", "Q", "NSW", "V"], "T": []}

    map_csp = CSPMap(regions, colors, var_map)

    print("assinging var", map_csp.assign_var(var_map))
    print("Constraints generated: ", map_csp.constraint)
    # #print("Number of constraints: ", len(map_csp.constraint))
    #print(map_csp.var_to_region, map_csp.var_to_domain)
    print("Map to number", map_csp.map_number)
    print("backtrack: ", map_csp.backtrack())
    print(map_csp)

if __name__ == '__main__':
    main()

    # var_to_region = {0: "WA", 1: "NT", 2: "Q", 3: "NSW", 4: "V", 5: "SA", 6: "T" } # pass this to print function

    # # (index_altered, var1, var2, etc)
    # def get_successors(self, next_var, state):
    #
    #     # list of successors
    #     successors = [ ]
    #     # state = list(state)
    #     # curr_domain = state[0]
    #
    #     # # return empty list if out of variables
    #     # if state[0] + 1 < len(self.variable):
    #     #     next_var = state[0] + 1
    #     # else:
    #     #     # reached leaf node
    #     #     return [ ]
    #
    #     new_state = [next_var] + state[1:]
    #     for d in self.domain:
    #         # add one since first element is next_var
    #         new_state[next_var+1] = d
    #         print('new state', new_state)
    #
    #         if self.constraint_satisfy(new_state):
    #             successors.append(tuple(new_state))
    #
    #     return successors
# state = list(state)
# curr_var = state[0]
#
# for i in range(curr_var - 1, -1, -1):
#
#     # print("looking at", i, curr_var)
#     # check if domain pair is in constraint for given variables
#     if (state[i + 1], state[curr_var + 1]) not in self.constraint[(i, curr_var)]:
#         # print("Not found: ", (state[i+1], state[curr_var+1]))
#         return False
#
# return True