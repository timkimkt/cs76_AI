# Name: Tim (Kyoung Tae) Kim
# Year: '22
# Class: COSC 76
# Assignment: PA 5
# Date: Nov 1, 2021

import random
import copy
import Sudoku

class SAT:

    def __init__(self, puzzle):

        # sudoku problem
        self.puzzle = puzzle                 # input cnf file

        self.variable = [ ]                  # list of variables
        self.clause_list = [ ]               # list of set of clauses

        self.unsatisfied_clause_list = [ ]   # list of unsatisfied clauses
        self.potential_variables = set()     # list of variables in unsatisfied clauses

        self.gen_var_clause()         # generates variable and clause list
        self.threshold = 0.9          # threshold for picking random variable to flip

        # Print statements
        print("CNF file: ", puzzle)
        print("Variable: ", self.variable)
        print("Clause list: ", self.clause_list)

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

    def max_variable_score(self, variables):
        max_score, max_var = float('-inf'), None
        tied = [ ]

        # for given variables
        for var in variables:
            score = 0
            flipped_var = self.flip_var(var)

            # check if flipped var satisfies the currently unsatisfied clause
            for clause in self.unsatisfied_clause_list:
                if flipped_var in clause:
                    score += 1

            # keep track of max score and var
            if score > max_score:
                max_score, max_var = score, self.flip_var(flipped_var)
                tied = [ ]
                tied.append(max_var)

            # add to tied list if score is same
            elif score == max_score:
                tied.append(self.flip_var(flipped_var))

            else:
                continue

        # pick randomly from tied
        if len(tied) > 0:
            max_var = random.choice(tied)

        return max_var

    # checks that all clauses satisfied
    def clause_satisfy(self):

        # reset list of unsatisfied clause and their variables
        self.unsatisfied_clause_list = [ ]
        self.potential_variables = [ ]

        for clause in self.clause_list:
            satisfy = False
            for item in clause:
                if item in self.variable:
                    satisfy = True
            if not satisfy:
                if clause not in self.unsatisfied_clause_list:
                    self.unsatisfied_clause_list.append(clause)

                for item in clause:
                    if item not in self.variable:
                        flipped_var = self.flip_var(item)
                        if flipped_var not in self.potential_variables:
                            self.potential_variables.append(flipped_var)



    def gsat(self, max_tries=100000):

        # randomly generate truth assignment
        self.random_assignment(self.variable)

        # 100,000
        for i in range(1, max_tries + 1):
            print("iteration: ", i)
            self.clause_satisfy()

            # unsatisfied list is empty (i.e. complete assignment)
            if len(self.unsatisfied_clause_list) == 0:
                print(f'All clauses satisfied for {self.puzzle}')
                return self.variable

            # threshold for random choice is 0.9
            if random.uniform(0, 1) > self.threshold:

                # choose random variable and flip
                rand_var = random.choice(self.variable)
                i = self.variable.index(rand_var)
                self.variable[i] = self.flip_var(rand_var)

            else:

                # pick variable with the highest score (randomly among tied)
                max_var = self.max_variable_score(self.variable)
                i = self.variable.index(max_var)
                self.variable[i] = self.flip_var(max_var)

            print('[GSAT] Length of unsatisfied: ', len(self.unsatisfied_clause_list))

        print(f"No satisfying assignment found for {self.puzzle}")
        return False

    def walksat(self, max_tries=100000):

        # randomly generate truth assignment
        self.random_assignment(self.variable)

        for i in range(1, max_tries + 1):
            print("iteration: ", i)
            self.clause_satisfy()

            # unsatisfied list is empty (i.e. complete assignment)
            if len(self.unsatisfied_clause_list) == 0:
                print(f'All clauses satisfied for {self.puzzle}')
                return self.variable

            # threshold for random choice is 0.8
            if random.uniform(0, 1) > self.threshold:

                rand_var = random.choice(self.potential_variables)
                i = self.variable.index(rand_var)
                self.variable[i] = self.flip_var(rand_var)

            else:

                max_var = self.max_variable_score(self.potential_variables)

                i = self.variable.index(max_var)
                self.variable[i] = self.flip_var(max_var)

            print('[WSAT] Length of unsatisfied: ', len(self.unsatisfied_clause_list))

        print(f"No satisfying assignment found for {self.puzzle}")
        return False

    def write_solution(self, filename):
        file = open(filename, "w")
        for var in self.variable:
            print(var, file=file)


if __name__ == "__main__":

    print("Hello World")