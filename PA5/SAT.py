import random
import copy
import Sudoku

class SAT:

    def __init__(self, puzzle):

        # sudoku problem
        self.puzzle = puzzle          # input puzzle

        self.variable = [ ]           # list or set of variables
        self.debug = len(set(self.variable))
        self.clause_list = [ ]             # list of CNFs

        self.unsatisfied_clause_list = [ ] # for walksat (smaller subset)
        self.potential_variables = set()

        self.gen_var_clause()         # generates variable and clause list
        self.threshold = 0.7          # threshold for picking random variable to flip
                                      # (picking up

        # Debugging
        print("CNF file: ", puzzle)
        print("Variable: ", self.variable)
        print("Clause list: ", self.clause_list)

        self.random_assignment(self.variable)     # randomly assigns truth values to variables

        # Debugging
        print("Randomly assigned: ", self.variable)

    # generates list of variables and clauses
    def gen_var_clause(self):

        # open and read CNF file
        file = open(self.puzzle, "r")

        for line in file:

            # append the set of clauses
            self.clause_list.append(set(line.split()))

            # append the variables to the list
            for item in line.strip().split():
                if "-" in item:
                    if item[1:] not in self.variable:
                        self.variable.append(item[1:])
                else:
                    if item not in self.variable:
                        self.variable.append(item)

    # randomly assigns truth values
    def random_assignment(self, variable):

        for i, var in enumerate(variable):
            flip = random.uniform(0, 1)

            if flip >= 0.5:
                if "-" in var:
                    variable[i] = self.flip_var(var)
                else:
                    variable[i] = self.flip_var(var)
            else:
                continue

    # flips variables
    def flip_var(self, variable):
        if "-" in variable:
            return variable[1:]
        else:
            return "-" + variable

    def max_variable_score(self):
        max_score, max_var = float('-inf'), None
        tied = [ ]

        for var in self.potential_variables:
            score = 0

            flipped_var = self.flip_var(var)

            for clause in self.unsatisfied_clause_list:

                if flipped_var in clause:
                    score += 1

            if score > max_score:
                max_score = score
                max_var = var
                tied = []
                tied.append(var)

            elif score == max_score:
                tied.append(var)

            else:
                continue

        if tied and len(tied) > 0:
            max_var = random.choice(tied)

        return self.flip_var(max_var)

        # # flip variable in assignment copy
        # variable_copy = copy.copy(self.potential_variables)
        #
        # if var in variable_copy:
        #     i = variable_copy.index(var)
        # else:
        #     i = variable_copy.index(self.flip_var(var))
        #
        # variable_copy[i] = self.flip_var(var)

    # checks that all clauses satisfied
    # def clause_satisfy(self, var=None):
    def clause_satisfy(self):
        self.unsatisfied_clause_list = [ ]
        self.potential_variables = set()
        # score = None
        #
        # if var:
        #     score = 0
        #
        #     # flip variable in assignment copy
        #     variable_copy = copy.copy(self.variable)
        #
        #     if var in variable_copy:
        #         i = variable_copy.index(var)
        #     else:
        #         i = variable_copy.index(self.flip_var(var))
        #     variable_copy[i] = self.flip_var(var)

        all_satisfy = True
        for clause in self.clause_list:
            satisfy = False
            for item in clause:
                if item in self.variable:
                    satisfy = True
            if not satisfy:
                self.unsatisfied_clause_list.append(clause)
                for var in clause:
                    self.potential_variables.add(var)
                all_satisfy = False
                #return False

        # if var:
        #     return score
        # else:
        #     return all_satisfy
        # # return True

        return all_satisfy

    def walksat(self, max_flip=50, max_tries=100000):

        # randomly generate truth assignment\
        self.random_assignment(self.variable)

        # 100,000
        for i in range(1, max_tries + 1):
            print("iteration: ", i)
            # for j in range(1, max_flip + 1):
            self.clause_satisfy()

            # unsatisfied list is empty (i.e. complete assignment)
            if len(self.unsatisfied_clause_list) == 0:
            #if self.clause_satisfy():
                print('all clauses satisfied')
                return self.variable

            # threshold is 0.7
            if random.uniform(0, 1) > self.threshold:
                rand_clause = random.choice(self.unsatisfied_clause_list)
                rand_var = random.choice(list(rand_clause))

                if rand_var in self.variable:
                    i = self.variable.index(rand_var)
                else:
                    i = self.variable.index(self.flip_var(rand_var))

                self.variable[i] = self.flip_var(rand_var)

            # else: highest score
            else:
                max_var = self.max_variable_score()
                print('max var', max_var)
                if max_var in self.variable:
                    i = self.variable.index(max_var)
                else:
                    i = self.variable.index(self.flip_var(max_var))

                self.variable[i] = self.flip_var(max_var)
            print("var list", self.variable)
            print('lenght of unsatisfied', len(self.unsatisfied_clause_list))
        # return truth assignment of alpha if found
        print("no satisfying assignment found")
        return

    def write_solution(self, filename):
        file = open(filename, "w")
        for var in self.variable:
            print(var, file=file)






    def GSAT(self, max_flip=50, max_tries=50):

        # 2,000

        # randomly generate truth assignment
        self.random_assignment(self.variable)

        for i in range(1, max_tries + 1):
            # 100,000
            # for j in range(1, max_flip + 1):

            if self.clause_satisfy():
                return self.variable

            # threshold is 0.9
            if random.uniform(0, 1) > self.threshold:

                rand_var = random.choice(self.variable)
                i = self.variable.index(rand_var)
                self.variable[i] = self.flip_var(rand_var)

                max_score = float('-inf')
                tied = [ ]

                i = 1
                for var in self.variable:

                    print(f'variable {i}')
                    score = self.variable_score(var)

                    if score > max_score:
                        max_score = score
                        tied = [ ]
                        tied.append(var)

                    elif score == max_score:
                        tied.append(var)

                    else:
                        continue
                    i += 1

            if tied and len(tied) > 0:

                rand_tied = random.choice(tied)
                i = self.variable.index(tied)
                self.variable[i] = self.flip_var(rand_tied)

        # return truth assignment of alpha if found
        return "no satisfying assignment found"

if __name__ == "__main__":

    print("Hello World")

    # # for each clause in the list
    # for item in self.clause_list:
    #     item = list(item)
    #     for i in range(1, len(item), 2):
    #         if item[i-1] not in variable_copy and item[i] not in variable_copy:
    #             continue
    #         else:
    #             score += 1
    #             # print(item, item[i-1], item[i], variable_copy)
    #             # print("early return", score)
    #             # return score
    #     # score += 1
    # # print('score', score)
    # return scor

    # checks that all clauses satisfied
    # def clause_satisfy(self):
    #
    #     for clause in self.clause_list:
    #         satisfy = False
    #         for item in clause:
    #             if item in self.variable:
    #                 satisfy = True
    #         if not satisfy:
    #             return False
    #
    #     return True