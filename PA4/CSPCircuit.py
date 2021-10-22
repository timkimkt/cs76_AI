
from CSPSolver import CSPSolver
import numpy as np


class CSPCircuit():
    def __init__(self, component, board, map):

        self.var_to_component = {}        # component pieces
        #self.var_to_domain = {}           # size (width, height)

        # board dimensions
        self.board = board
        self.board_size = [len(board[0]), len(board)]  # width and height (m & n)
        self.board_width, self.board_height = len(board[0]), len(board)

        # var no. --> var dimension
        self.variable = self.assign_var(component)  # bottom left coordinate (list of tuples)

        # reversed var_to_domain for map_number
        self.var_to_component_rev = {v: k for k, v in self.var_to_component.items()}

        # 0 : (3, 2)
        self.component_size = self.gen_component_size(component, map)  # width and height

        # initialize dictionaries (int -> 'A')
        self.letter_to_component = map  # eg. A --> aaaaaa

        # variables are integers starting at 0
        self.domain = self.assign_domain()      # possible locations (list)

        #self.assignment = [-1]*(self.board_size[0] + self.board_size[1])   # starting state
        #self.assignment = [[None for _ in range(self.board_width)] for j in range(self.board_height)]
        self.assignment = [(-1, -1) for _ in range(len(self.variable))]

        # neighbor in number
        self.map_number = self.map_piece_to_number(map)

        # constraint mapping pair of integer (two regions) to pair of integer (two color)
        self.constraint = self.generate_constraint()

        #print(self.domain)
        print("domain: ")
        for k in self.domain.keys():
            print("Domain of ", k, "is ", self.domain[k])
        print("constraint: ")
        for k in self.constraint.keys():
            print("Constraint between:", self.var_to_component[k[0]].upper(), "and", self.var_to_component[k[1]].upper(), "is: ", self.constraint[k])
        print(self.var_to_component)

    def board_legal(self, x, y):
        if (x not in range(0, self.board_width)
        or y not in range(0, self.board_height)):
            return False

        # note that (0,0) is at bottom left corner
        return self.assignment[-y][x] is None
        #return state[-y][x] != -1

    # assigns variables to number from zero
    def assign_var(self, variable):
        # variables = [ ]
        # for i, v in enumerate(variable):
        #     variables.append((None, None))     # bottom left coordinate
        #     self.var_to_component[i] = v
        # return variables

        variables = []
        for i, v in enumerate(variable):
            variables.append(i)  # bottom left coordinate
            self.var_to_component[i] = v
        return variables

    def gen_component_size(self, components, map):

        output = { }

        for c in components:
            output[self.var_to_component_rev[c]] = (len(map[c][0]), len(map[c]))

        return output

    # assigns domains to number from zero
    def assign_domain(self):

        # list of list containing tuples
        # domains = []
        domains = { }
        domains[-1] = (-1, -1)

        for v in range(len(self.variable)):
            #domain_v = [ ]
            domains[v] = [ ]

            for i in range(self.board_height-1, -1, -1):
                for j in range(self.board_width):
                    #print(self.component_size[v][1] - i, j, self.component_size[v][1], self.component_size[v][0])

                    if (i - (self.component_size[v][1]-1) >= 0) and (j + (self.component_size[v][0]-1) < self.board_width):
                        #domain_v.append((self.component_size[v][1] - i, j))
                        #domain_v.append((j, i))
                        #domains[v].append((i - (self.component_size[v][1]-1), j))
                        domains[v].append((j, i - (self.component_size[v][1]-1)))

                        #domains[v].append((self.component_size[v][1] - i, j))

            #domains.append(domain_v)

        return domains


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

                            if not self.overlap(r1, r2, m, n):
                                # add fn to check if they overlap
                                output[(r1, r2)].append((m, n))

        return output

    def overlap(self, r1, r2, m, n):
        r1_x, r1_y = m         # m is location of r1
        width_r1, height_r1 = self.component_size[r1]
        r2_x, r2_y = n         # n is location of r2
        width_r2, height_r2 = self.component_size[r2]
        # print(r1, ": ", m)
        # print(r2, ": ", n)
        # print("debug", r1, r2, m, n)
        # print("size 1 ", self.component_size[r1])
        # print("size 2 ",  self.component_size[r2])
        # for i in range(r1_x)

        for x in range(r2_x, r2_x + width_r2):

        # on the right
            if x in range(r1_x, r1_x + width_r1):
                # top or bottom
                # if (height_r2 == 1):
                    #print("debug", r2_y, (r1_y, r1_y + height_r1))
                for y in range(r2_y, r2_y + height_r2):
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


    def constraint_satisfy(self, state, var):

        # for all neighbors of variable that has just been assigned

        for neigh in self.map_number[var]:
            # Debug: print('neig', self.var_to_region[neigh])
            # skip if neighbor has not been assigned
            if state[neigh] != (-1, -1):
            #if state[neigh] != (None, None):
            #print(state[neigh])
            # if all((state[neigh], state[var])):
                #print("debug", state[neigh])
                # check both pairs in the constraint
                if (var, neigh) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[var], state[neigh]) not in self.constraint[(var, neigh)]:
                        #print("False1")
                        #print("debug", state[var], state[neigh])
                        return False

                elif (neigh, var) in self.constraint:
                    # return false if assignment does not exist in constraint
                    if (state[neigh], state[var]) not in self.constraint[(neigh, var)]:
                        #print("False2")

                        return False

        return True

    def assignment_complete(self):
        return (-1, -1) not in self.assignment
        #return all(item is None for item in self.assignment)
        #rreturn not all(self.assignment)
        #return (None, None) not in self.assignment

    def unassigned(self, var):
        # return all(item is None for item in var)
        return var == (-1, -1)

    def __str__(self):
        string = "Assignment:  " + str(self.assignment)
        return string

    def print_completed_board(self):
        for i, p in enumerate(self.assignment):
            #print(p)
            r, c = len(self.board)-1 - p[1], p[0]
            # self.board[r][c] = self.var_to_component[i].lower()

            # print(r, c)
            for y in range(r, r - self.component_size[i][1], -1):
                for x in range(c, c + self.component_size[i][0]):
                    self.board[y][x] = self.var_to_component[i].lower()


            # for y in range(p[0], p[0] + self.component_size[i][1]):
            #     for x in range(p[1], p[1] + self.component_size[i][0]):
            #         # print(x, len(self.board[0])-y,)
            #         # self.board[x][len(self.board[0])-y] = self.var_to_component[i].lower()
            #
            #         self.board[len(self.board[0])-y][x] = self.var_to_component[i].lower()
        print(self.board)


def main():

    # A = np.reshape([['a']*8], (2,4))
    # B = np.reshape([['b']*20], (4,5))
    # C = np.reshape([['c']*10], (2,5))
    # E = np.reshape([['e']*10], (1,10))
    # components = ["A", "B", "C", "E"]
    # components_map = {"A": A, "B": B, "C": C, "E": E}
    # print("Here are the components: \n", A, "\n", B, "\n", C, "\n", E)
    # board = np.reshape([["."]*100], (10, 10))
    # print("Here is the circuit: \n", board)
    # print("---------------------------------------------------------------------")
    # print("---------------------------------------------------------------------")

    #################################
    A = np.reshape([['a']*6], (2,3))
    B = np.reshape([['b']*10], (2,5))
    C = np.reshape([['c']*6], (3,2))
    E = np.reshape([['e']*7], (1,7))
    components = ["A", "B", "C", "E"]
    components_map = {"A": A, "B": B, "C": C, "E": E}
    print("Here are the components: \n", A, "\n", B, "\n", C, "\n", E)
    board = np.reshape([["."]*30], (3, 10))
    print("Here is the circuit: \n", board)
    print("---------------------------------------------------------------------")
    print("---------------------------------------------------------------------")
    #################################

    # print("Final output: ", map_csp)
    #
    # csp_circuit = CSPCircuit(components, board, components_map)
    # csp_solution = CSPSolver(csp_circuit)
    # print("backtrack: ", csp_solution.backtrack())
    # print("Final output: ", csp_circuit)




    # print("---------------------------------------------------------------------")
    # # backtrack(MRV, Degree, LCV, Tiebreak=False):
    # csp_circuit = CSPCircuit(components, board, components_map)
    # csp_solution = CSPSolver(csp_circuit)
    # print("Backtrack: ", csp_solution.backtrack(True, False, False))
    # print("Final output: ", csp_circuit)
    #
    # print("---------------------------------------------------------------------")
    # # backtrack(MRV, Degree, LCV, Tiebreak=False):
    # csp_circuit = CSPCircuit(components, board, components_map)
    # csp_solution = CSPSolver(csp_circuit)
    # print("Backtrack: ", csp_solution.backtrack(True, False, False, True))
    # print("Final output: ", csp_circuit)
    #
    # print("---------------------------------------------------------------------")
    # # backtrack(MRV, Degree, LCV, Tiebreak=False):
    # csp_circuit = CSPCircuit(components, board, components_map)
    # csp_solution = CSPSolver(csp_circuit)
    # print("Backtrack: ", csp_solution.backtrack(False, True, False))
    # print("Final output: ", csp_circuit)
    #
    # print("---------------------------------------------------------------------")
    # # backtrack(MRV, Degree, LCV, Tiebreak=False):
    # csp_circuit = CSPCircuit(components, board, components_map)
    # csp_solution = CSPSolver(csp_circuit)
    # print("Backtrack: ", csp_solution.backtrack(False, False, True))
    # print("Final output: ", csp_circuit)
    #
    # print("---------------------------------------------------------------------")
    # # backtrack(MRV, Degree, LCV, Tiebreak=False):
    # csp_circuit = CSPCircuit(components, board, components_map)
    # csp_solution = CSPSolver(csp_circuit)
    # print("Backtrack: ", csp_solution.backtrack(True, False, True))
    # print("Final output: ", csp_circuit)
    #
    # print("---------------------------------------------------------------------")
    # # backtrack(MRV, Degree, LCV, Tiebreak=False):
    # csp_circuit = CSPCircuit(components, board, components_map)
    # csp_solution = CSPSolver(csp_circuit)
    # print("Backtrack: ", csp_solution.backtrack(False, True, True))
    # print("Final output: ", csp_circuit)

    print("---------------------------------------------------------------------")
    # backtrack(MRV, Degree, LCV, Tiebreak=False):
    csp_circuit = CSPCircuit(components, board, components_map)
    csp_solution = CSPSolver(csp_circuit)
    print("backtrack: ", csp_solution.backtrack(False, False, False))
    print("Final output: ", csp_circuit)
    csp_circuit.print_completed_board()

if __name__ == '__main__':
    main()



    # # converts text piece from user to map of numbers
    # # based on variable assignment
    # def map_piece_to_number(self, map):
    #
    #     output = { }
    #
    #     for region in map.keys():
    #         output[self.var_to_component_rev[region]] = []
    #         for other in map[region]:
    #             output[self.var_to_component_rev[region]].append(self.var_to_component_rev[other])
    #
    #     return output
    #
    # # string method for printing
    # # converts integer values to respective string values



    # generaate constraint map (pair of var to pair of domain)
    # def generate_constraint(self):
    #
    #     output = { }
    #
    #     #for each variable pair
    #     for v1 in self.variable:
    #         for v2 in self.variable:
    #             # avoid duplicates
    #             if v1 != v2 and (v2, v1) not in output:
    #                 # create a list to store constraints
    #                 output[(v1, v2)] = [ ]
    #                 # append possible pair of domain values
    #                 output[(v1, v2)].append((n, m))
    #
    #     return output