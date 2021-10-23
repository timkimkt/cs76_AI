
from CSPSolver import CSPSolver
import numpy as np
import copy


class CSPCircuit():
    def __init__(self, component, board, map):

        self.var_to_component = {}        # component pieces

        # board dimensions
        self.board = board
        self.board_size = [len(board[0]), len(board)]  # width and height (m & n)
        self.board_width, self.board_height = len(board[0]), len(board)

        # var no. to bottom left coordinate
        self.variable = self.assign_var(component)

        # reversed var_to_domain for map_number
        self.var_to_component_rev = {v: k for k, v in self.var_to_component.items()}

        # dictionary of component width and height
        self.component_size = self.gen_component_size(component, map)

        # initialize dictionaries (eg. A --> aaaaaa)
        self.letter_to_component = map

        # map of variables to its possible coordinates
        self.domain = self.assign_domain()

        # state
        self.assignment = [(-1, -1) for _ in range(len(self.variable))]

        # neighbor in number
        self.map_number = self.map_piece_to_number(map)

        # constraint mapping pair of integer (two regions) to pair of integer (two color)
        self.constraint = self.generate_constraint()

    # assigns variables to number from zero
    def assign_var(self, variable):

        variables = []
        for i, v in enumerate(variable):
            variables.append(i)
            self.var_to_component[i] = v
        return variables

    # creates a map of component width and height
    def gen_component_size(self, components, map):

        output = { }
        for c in components:
            output[self.var_to_component_rev[c]] = (len(map[c][0]), len(map[c]))
        return output

    # assigns domains to number from zero
    def assign_domain(self):

        # list of list containing tuples
        domains = { }
        domains[-1] = (-1, -1)   # unassigned variable

        for v in range(len(self.variable)):
            domains[v] = [ ]

            for i in range(self.board_height-1, -1, -1):
                for j in range(self.board_width):

                    # all the possible starting position of the compoentn
                    if ((i - (self.component_size[v][1]-1) >= 0) and
                            (j + (self.component_size[v][0]-1) < self.board_width)):
                        domains[v].append((j, i - (self.component_size[v][1]-1)))
        return domains

    # generate constraint map
    def generate_constraint(self):

        output = { }

        #for each variable pair
        for r1 in self.var_to_component.keys():
            for r2 in self.var_to_component.keys():
                # avoid duplicates
                if r1 != r2 and (r2, r1) not in output:
                    # create a list to store constraints
                    output[(r1, r2)] = [ ]
                    # append possible pair of domain values
                    # switched pairs can also work
                    for m in self.domain[r1]:
                        for n in self.domain[r2]:
                            # if the two pieces do not overlap
                            if not self.overlap(r1, r2, m, n):
                                output[(r1, r2)].append((m, n))

        return output

    # checks if two pieces overlap
    def overlap(self, r1, r2, m, n):
        r1_x, r1_y = m         # m is location of r1
        width_r1, height_r1 = self.component_size[r1]
        r2_x, r2_y = n         # n is location of r2
        width_r2, height_r2 = self.component_size[r2]

        # if any of the x coordinate of piece 2
        for x in range(r2_x, r2_x + width_r2):
            # overlaps with x coordinate of piece 1
            if x in range(r1_x, r1_x + width_r1):
                # and if any of the y coordinate of piece 2
                for y in range(r2_y, r2_y + height_r2):
                    # overlaps with y coordinate of piece 1
                    if y in range(r1_y, r1_y + height_r1):
                        return True

        return False

    def map_piece_to_number(self, map):

        output = { }

        for circuit in map.keys():
            output[self.var_to_component_rev[circuit]] = []
            for other in map.keys():
                if circuit != other:
                    output[self.var_to_component_rev[circuit]].append(self.var_to_component_rev[other])

        return output


    # check that recently assigned variable satisfies constraint
    def constraint_satisfy(self, state, var):

        # for all neighbors of variable that has just been assigned
        for neigh in self.map_number[var]:
            # skip if neighbor has not been assigned
            if state[neigh] != (-1, -1):
                # check both pairs in the constraint
                if (var, neigh) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[var], state[neigh]) not in self.constraint[(var, neigh)]:
                        return False

                # elif (neigh, var) in self.constraint:
                #     # return false if assignment does not exist in constraint
                #     if (state[neigh], state[var]) not in self.constraint[(neigh, var)]:
                #         return False

        return True

    # checks if assignment is complete
    def assignment_complete(self):
        return (-1, -1) not in self.assignment

    # checks for unassigned variable
    def unassigned(self, var):
        return var == (-1, -1)

    # print the final output
    def __str__(self):
        string = "Assignment:  " + str(self.assignment)
        return string

    def print_completed_board(self):
        # copy board for printing
        board_copy = copy.copy(self.board)

        # for points in final assignment
        for i, p in enumerate(self.assignment):

            # convert coordinates into points in 2d-array
            r, c = len(self.board)-1 - p[1], p[0]

            # print each component based on dimensions
            for y in range(r, r - self.component_size[i][1], -1):
                for x in range(c, c + self.component_size[i][0]):
                    board_copy[y][x] = self.var_to_component[i].lower()

        # print board
        print(board_copy)
        del board_copy

def main():

    ############### CLASS EXAMPLE ##################
    A = np.reshape([['a']*6], (2,3))
    B = np.reshape([['b']*10], (2,5))
    C = np.reshape([['c']*6], (3,2))
    E = np.reshape([['e']*7], (1,7))
    components = ["A", "B", "C", "E"]
    components_map = {"A": A, "B": B, "C": C, "E": E}
    print("Here are the components: \n", A, "\n", B, "\n", C, "\n", E)
    board = np.reshape([["."]*30], (3, 10))
    print("Here is the circuit: \n", board)
    print("-------------------------------------------------------------------------------------------------------------------------")

    ############### MY EXAMPLE ##################
    # A = np.reshape([['a']*8], (2,4))
    # B = np.reshape([['b']*20], (4,5))
    # C = np.reshape([['c']*10], (2,5))
    # E = np.reshape([['e']*10], (1,10))
    # components = ["A", "B", "C", "E"]
    # components_map = {"A": A, "B": B, "C": C, "E": E}
    # print("Here are the components: \n", A, "\n", B, "\n", C, "\n", E)
    # board = np.reshape([["."]*100], (10, 10))
    # print("Here is the circuit: \n", board)
    # print("-------------------------------------------------------------------------------------------------------------------------")
    # #################################

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, False, True, False, False, False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, False, False, True, False, False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, False, True, False, False, True)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, False, True, False, True, False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, False, True, False, True, True)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, False, False, True, True, False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, True, True, False, True, True)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

    print("-------------------------------------------------------------------------------------------------------------------------")
    # backtrack(Domain, Inference, MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    csp_solution.backtrack(csp_circuit.domain, True, False, True, True, False)
    print("Node count: ", csp_solution.node_count)
    print("Value count: ", csp_solution.value_count)
    print(csp_circuit)
    csp_circuit.print_completed_board()

if __name__ == '__main__':
    main()