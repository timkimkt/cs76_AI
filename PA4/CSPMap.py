from CSPSolver import CSPSolver

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
        self.var_to_domain_rev = {v: k for k, v in self.var_to_domain.items()}

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

        domains = {}
        #domains[-1] = None
        domains[-1] = -1

        for v in range(len(self.variable)):
            domains[v] = [ ]
            for i, d in enumerate(domain):
                domains[v].append(i)

        self.var_to_domain[-1] = "Unassigned"
        i = 0
        for d in domain:
            self.var_to_domain[i] = d
            i += 1

        return domains

        # ### MOD DM domains = []
        # domains = { }
        #
        # #self.var_to_domain[-1] = "Unassigned"
        # self.var_to_domain[None] = "Unassigned"
        #
        # i = 0
        # for d in domain:
        #     #domains.append(i)
        #     domains[i] = [i]
        #     self.var_to_domain[i] = d
        #     i += 1
        #
        # return domains

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
            #     res.append(str(self.var_to_region[i]) + ": Unassigned")
            #     continue
            # if v is None:
                res.append(str(self.var_to_region[i]) + ": Unassigned")
                continue

            #print("h", self.assignment)
            res.append(str(self.var_to_region[i]) + ": " + str(self.var_to_domain[self.assignment[i]]))

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
            ###if state[neigh] is not None:
                # check both pairs in the constraint
                if (var, neigh) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[var], state[neigh]) not in self.constraint[(var, neigh)]:
                        #print("False1")

                        return False

                elif (neigh, var) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[neigh], state[var]) not in self.constraint[(neigh, var)]:
                        #print("False2", state[neigh], state[var], self.constraint[(neigh, var)])

                        return False

        return True

    def assignment_complete(self):
        return -1 not in self.assignment
        #return None not in self.assignment
        # return -1 not in self.assignment

    def unassigned(self, var):
        return var == -1
        # return var is None


def main():
    regions = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
    colors = ["red", "green", "blue"]
    var_map = {"WA": ["NT", "SA"], "NT": ["WA", "SA", "Q"], "Q": ["NT", "SA", "NSW"],
               "NSW": ["Q", "SA", "V"], "V": ["NSW", "SA"], "SA": ["WA", "NT", "Q", "NSW", "V"], "T": []}

    # map_csp = CSPMap(regions, colors, var_map)
    # csp_solution = CSPSolver(map_csp)
    # print(len(map_csp.constraint), "constraints generated: ", map_csp.constraint)
    # print("Map to number", map_csp.map_number)


    # map_csp = CSPMap(regions, colors, var_map)
    # csp_solution = CSPSolver(map_csp)
    # print("Backtrack: ", csp_solution.backtrack())
    # print("Final output: ", map_csp)

    print("---------------------------------------------------------------------")
    # backtrack(MRV, Degree, LCV, Tiebreak=False):
    map_csp = CSPMap(regions, colors, var_map)
    csp_solution = CSPSolver(map_csp)
    print("Backtrack: ", csp_solution.backtrack(True, False, False))
    print("Final output: ", map_csp)

    print("---------------------------------------------------------------------")
    # backtrack(MRV, Degree, LCV, Tiebreak=False):
    map_csp = CSPMap(regions, colors, var_map)
    csp_solution = CSPSolver(map_csp)
    print("Backtrack: ", csp_solution.backtrack(True, False, False, True))
    print("Final output: ", map_csp)

    print("---------------------------------------------------------------------")
    map_csp = CSPMap(regions, colors, var_map)
    csp_solution = CSPSolver(map_csp)
    print("Backtrack: ", csp_solution.backtrack(False, True, False))
    print("Final output: ", map_csp)

    print("---------------------------------------------------------------------")
    map_csp = CSPMap(regions, colors, var_map)
    csp_solution = CSPSolver(map_csp)
    print("Backtrack: ", csp_solution.backtrack(False, False, True))
    print("Final output: ", map_csp)

    print("---------------------------------------------------------------------")
    map_csp = CSPMap(regions, colors, var_map)
    csp_solution = CSPSolver(map_csp)
    print("Backtrack: ", csp_solution.backtrack(False, False, False))
    print("Final output: ", map_csp)

if __name__ == '__main__':
    main()
