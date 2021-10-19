class CSPMap():
    def __init__(self, variable, domain, map):

        # initialize dictionaries
        self.var_to_region = {}
        self.var_to_domain = {}

        # variables and domains are integers starting at 0
        self.variable = self.assign_var(variable)
        self.domain = self.assign_domain(domain)

        # reversed var_to_domain for map_number
        self.var_to_region_rev = {v: k for k, v in self.var_to_region.items()}
        self.map_number = self.map_text_to_number(map)

        # constraint mapping pair of integer (two regions) to pair of integer (two color)
        self.constraint = self.generate_constraint()
        self.assignment = (-1,-1,-1,-1,-1,-1,-1)      # starting state


    # assigns variables to number from zero
    def assign_var(self, variable):
        variables = [ ]

        i = 0
        for v in variable:
            variables.append(i)
            self.var_to_region[i] = v
            i += 1

        return variables

    # assigns domains to number from zero
    # -1 is unassigned (uncolored)
    def assign_domain(self, domain):
        domains = []
        self.var_to_domain[-1] = "Unassigned"

        i = 0
        for d in domain:
            domains.append(i)
            self.var_to_domain[i] = d
            i += 1

        return domains

    # converts text map from user to map of numbers
    # based on variable assignment
    def map_text_to_number(self, map):

        output = { }

        for region in map.keys():
            output[self.var_to_region_rev[region]] = []
            for other in map[region]:
                output[self.var_to_region_rev[region]].append(self.var_to_region_rev[other])

        return output

    # string method for printing
    # converts integer values to respective string values
    def __str__(self):
        res = [ ]

        for i,v in enumerate(self.assignment):
            if v == -1:
                res.append(str(self.var_to_region[i]) + ": Unassigned")
                continue

            res.append(str(self.var_to_region[i]) + ": " + str(self.var_to_domain[v]))

        string = "Assignment:  " + str(res)
        return string

    # generaate constraint map (pair of var to pair of domain)
    def generate_constraint(self):

        output = { }

        #for each variable pair
        for r1 in self.map_number:
            for r2 in self.map_number[r1]:
                # avoid duplicates
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

    # check for recently assigned var if constraint is satisfied
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

    # state is being passed as a list
    def MRV_heuristic(self, state):

        # remaining values, associated variable
        MRV, max_var = float('-inf'), 0

        # for all unassigned variables
        for i, v in enumerate(self.assignment):
            if v == -1:
                rv = 0
                # try assigning possible domain values
                for d in self.domain:
                    state[i] = d
                    # increment count if it is legal
                    if self.constraint_satisfy(state, i):
                        rv += 1
                    # reset assignment
                    state[i] = -1
                # if current count is greater than max
                if rv > MRV:
                    # record MRV and variable
                    MRV, max_var = rv, i

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

    print(len(map_csp.constraint), "constraints generated: ", map_csp.constraint)
    print("Map to number", map_csp.map_number)
    print("---------------------------------------------------------------------")
    print("backtrack: ", map_csp.backtrack())
    print("Final output: ", map_csp)

if __name__ == '__main__':
    main()