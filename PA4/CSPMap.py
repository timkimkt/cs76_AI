# Class: COSC 81
# Assignment: PA 4
# Date: Oct 23, 2021
# Author: Tim (Kyoung Tae) Kim
# Year: '22

from CSPSolver import CSPSolver

class CSPMap():
    def __init__(self, map, domain):

        # initialize dictionaries
        self.var_to_region = {}
        self.var_to_domain = {}
        self.var_map = map

        # variables and domains are integers starting at 0
        self.variable = self.assign_var(list(map.keys()))
        self.domain = self.assign_domain(domain)

        # reversed var_to_domain for map_number
        self.var_to_region_rev = {v: k for k, v in self.var_to_region.items()}
        self.var_to_domain_rev = {v: k for k, v in self.var_to_domain.items()}

        self.map_number = self.map_text_to_number(map)

        # constraint mapping pair of integer (two regions) to pair of integer (two color)
        self.constraint = self.generate_constraint()
        self.assignment = [(-1) for _ in range(len(self.variable))]

    # assigns variables to number from zero
    def assign_var(self, variable):
        variables = []

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

    # create a map of neighbors based on variable number
    def map_text_to_number(self, map):

        output = {}

        for region in map.keys():
            output[self.var_to_region_rev[region]] = []
            for other in map[region]:
                output[self.var_to_region_rev[region]].append(self.var_to_region_rev[other])

        return output

    # generate constraint map (pair of var to pair of domain)
    def generate_constraint(self):

        output = {}

        # for each variable pair
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
            # skip if neighbor has not been assigned
            if state[neigh] != -1:
                # check both pairs in the constraint
                if (var, neigh) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[var], state[neigh]) not in self.constraint[(var, neigh)]:
                        return False

                if (neigh, var) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[neigh], state[var]) not in self.constraint[(neigh, var)]:
                        return False

        return True

    # checks if assignment is complete
    def assignment_complete(self):
        return -1 not in self.assignment

    # checks for unassigned variable
    def unassigned(self, var):
        return var == -1


    # string method for printing
    # converts integer values to respective string values
    def __str__(self):
        res = [ ]

        for i,v in enumerate(self.assignment):
            if v == -1:
                res.append(str(self.var_to_region[i]) + ": Unassigned")
                continue

            res.append(str(self.var_to_region[i]) + ": " + str(self.var_to_domain[self.assignment[i]]))

        string = "Assignment:  " + str(res)
        return string



def main():
    colors = ["red", "green", "blue", "purple"]
    var_map = {"WA": ["NT", "SA"], "NT": ["WA", "SA", "Q"], "Q": ["NT", "SA", "NSW"],
               "NSW": ["Q", "SA", "V"], "V": ["NSW", "SA"], "SA": ["WA", "NT", "Q", "NSW", "V"], "T": []}

    var_map = {
        'AK': [],
        'AL': ['MS', 'TN', 'GA', 'FL'],
        'AR': ['MO', 'TN', 'MS', 'LA', 'TX', 'OK'],
        'AZ': ['CA', 'NV', 'UT', 'CO', 'NM'],
        'CA': ['OR', 'NV', 'AZ'],
        'CO': ['WY', 'NE', 'KS', 'OK', 'NM', 'AZ', 'UT'],
        'CT': ['NY', 'MA', 'RI'],
        'DC': ['MD', 'VA'],
        'DE': ['MD', 'PA', 'NJ'],
        'FL': ['AL', 'GA'],
        'GA': ['FL', 'AL', 'TN', 'NC', 'SC'],
        'HI': [],
        'IA': ['MN', 'WI', 'IL', 'MO', 'NE', 'SD'],
        'ID': ['MT', 'WY', 'UT', 'NV', 'OR', 'WA'],
        'IL': ['IN', 'KY', 'MO', 'IA', 'WI'],
        'IN': ['MI', 'OH', 'KY', 'IL'],
        'KS': ['NE', 'MO', 'OK', 'CO'],
        'KY': ['IN', 'OH', 'WV', 'VA', 'TN', 'MO', 'IL'],
        'LA': ['TX', 'AR', 'MS'],
        'MA': ['RI', 'CT', 'NY', 'NH', 'VT'],
        'MD': ['VA', 'WV', 'PA', 'DC', 'DE'],
        'ME': ['NH'],
        'MI': ['WI', 'IN', 'OH'],
        'MN': ['WI', 'IA', 'SD', 'ND'],
        'MO': ['IA', 'IL', 'KY', 'TN', 'AR', 'OK', 'KS', 'NE'],
        'MS': ['LA', 'AR', 'TN', 'AL'],
        'MT': ['ND', 'SD', 'WY', 'ID'],
        'NC': ['VA', 'TN', 'GA', 'SC'],
        'ND': ['MN', 'SD', 'MT'],
        'NE': ['SD', 'IA', 'MO', 'KS', 'CO', 'WY'],
        'NH': ['VT', 'ME', 'MA'],
        'NJ': ['DE', 'PA', 'NY'],
        'NM': ['AZ', 'UT', 'CO', 'OK', 'TX'],
        'NV': ['ID', 'UT', 'AZ', 'CA', 'OR'],
        'NY': ['NJ', 'PA', 'VT', 'MA', 'CT'],
        'OH': ['PA', 'WV', 'KY', 'IN', 'MI'],
        'OK': ['KS', 'MO', 'AR', 'TX', 'NM', 'CO'],
        'OR': ['CA', 'NV', 'ID', 'WA'],
        'PA': ['NY', 'NJ', 'DE', 'MD', 'WV', 'OH'],
        'RI': ['CT', 'MA'],
        'SC': ['GA', 'NC'],
        'SD': ['ND', 'MN', 'IA', 'NE', 'WY', 'MT'],
        'TN': ['KY', 'VA', 'NC', 'GA', 'AL', 'MS', 'AR', 'MO'],
        'TX': ['NM', 'OK', 'AR', 'LA'],
        'UT': ['ID', 'WY', 'CO', 'NM', 'AZ', 'NV'],
        'VA': ['NC', 'TN', 'KY', 'WV', 'MD', 'DC'],
        'VT': ['NY', 'NH', 'MA'],
        'WA': ['ID', 'OR'],
        'WI': ['MI', 'MN', 'IA', 'IL'],
        'WV': ['OH', 'PA', 'MD', 'VA', 'KY'],
        'WY': ['MT', 'SD', 'NE', 'CO', 'UT', 'ID'],
    }

    print("Here are the regions:", list(var_map.keys()))
    print("here are the colors: ", colors)
    print("Here is the map: ", var_map)
    print("-------------------------------------------------------------------------------------------------------------------------")

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=False, MRV=False, Degree=False, LCV=False, Tiebreak=False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=False, MRV=True, Degree=False, LCV=False, Tiebreak=False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=False, MRV=False, Degree=True, LCV=False, Tiebreak=False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=False, MRV=True, Degree=False, LCV=False, Tiebreak=True)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=False, MRV=False, Degree=False, LCV=True, Tiebreak=False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=False, MRV=True, Degree=False, LCV=True, Tiebreak=True)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=False, MRV=False, Degree=True, LCV=True, Tiebreak=False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=True, MRV=False, Degree=False, LCV=False, Tiebreak=False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_map = CSPMap(var_map, colors)
    csp_solution = CSPSolver(csp_map)
    csp_solution.backtrack(csp_map.domain, inference=True, MRV=False, Degree=True, LCV=True, Tiebreak=False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_map)
    csp_solution.check_conflict(csp_map)

if __name__ == '__main__':
    main()
