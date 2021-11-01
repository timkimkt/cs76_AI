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


    def gen_var_clause(self):

        # read file
        file = open(self.puzzle, "r")

        for line in file:

            self.clause_list.append(set(line.split()))
            for item in line.strip().split():
                if "-" in item:
                    if item[1:] not in self.variable:
                        self.variable.append(item[1:])
                else:
                    if item not in self.variable:
                        self.variable.append(item)

            # # Debug:
            # #print(len(line))
            #
            # # adds variables to the list
            # # if len(line) == 38:
            # if len(line) == 38 or len(line) == 36:
            #     for var in line.split():
            #         self.variable.append(var)
            #
            # # creation of list of set of clauses
            # # elif len(line) == 11 or len(line) == 37:
            # elif len(line) == 11 or len(line) == 37 or len(line) == 10:
            #     temp = set()
            #     for c in line.strip().split():
            #         temp.add(c)

            # self.clause.append(temp)

    # sat helper scores the variable

    # checks that all clauses satisfied
    def clause_satisfy(self):

        #
        for clause in self.clause_list:
            satisfy = False
            for item in clause:
                if item in self.variable:
                    satisfy = True
            if not satisfy:
                return False

        return True





            # item = list(item)
            # for i in range(1, len(item), 2):
            #     if item[i-1] not in self.variable and item[i] not in self.variable:
            #         print("unsatisfied:  items", item, "variable", self.variable)
            #         return False
            #     else:
            #         print("satisfied:  items", item, "variable", self.variable)

        # return True


    # def clause_satisfy2(self):
    #     satisfied = True
    #
    #     for item in self.clause:
    #         item = list(item)
    #         for i in range(1, len(item), 2):
    #             if item[i-1] not in self.variable and item[i] not in self.variable:
    #                 self.unsatisfied_clause.append(item)
    #                 satisfied = False
    #
    #     return satisfied

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


    def flip_var(self, variable):
        if "-" in variable:
            return variable[1:]
        else:
            return "-" + variable

    def variable_score(self, var):
        score = 0

        # flip variable in assignment copy
        variable_copy = copy.copy(self.variable)
        #print('before', variable_copy)
        if var in variable_copy:
            i = variable_copy.index(var)
        else:
            i = variable_copy.index(self.flip_var(var))
        variable_copy[i] = self.flip_var(var)

        for clause in self.clause_list:
            satisfy = False
            for item in clause:
                if item in variable_copy:
                    satisfy = True

            if not satisfy:
                #print(clause, "does not satisfy", variable_copy)
                continue
            else:
                #print(clause, "Satisfies", variable_copy)
                score += 1
        #print("flipped", var, "to ", variable_copy[i], "score", score)
        print('score', score)
        return score



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
        # return score

    # input: set of clause (alpha)
    # MAX_FLIPS, MAX_TRIES
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

    def walksat(self, max_flip=50, max_tries=100000):

        # randomly generate truth assignment

        self.random_assignment(self.variable)

        # 100,000
        for i in range(1, max_tries + 1):
            print("iteration: ", i)
            # # 100,000
            # for j in range(1, max_flip + 1):

            # no. of unsatisfied

            # unsatifised list is empty --> return assignment
            if self.clause_satisfy():
                print('all clauses satisfied')
                return self.variable

            # # threshold is 0.7
            # #print("random num", random.uniform(0, 1))
            if random.uniform(0, 1) > self.threshold:
                rand_var = random.choice(self.variable)
                i = self.variable.index(rand_var)
                self.variable[i] = self.flip_var(rand_var)
                print('random flip')

            # else: highest score
            for clause in self.clause_list:
                satisfied = False
                for item in clause:
                    if item in self.variable:
                        satisfied = True
                if not satisfied:
                    self.unsatisfied_clause_list.append(clause)
            #print("unsatisfied clauses:", self.unsatisfied_clause_list)
            # pick random clause from unsatisfied

            rand_clause = random.choice(self.unsatisfied_clause_list)


            max_score = float('-inf')
            tied = [ ]

            i = 1
            for var in rand_clause:
                var = var[1:] if "-" in var else var


                #print(f'rand cluase variable {i}', var, rand_clause)

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
                if rand_tied in self.variable:
                    i = self.variable.index(rand_tied)
                else:
                    i = self.variable.index(self.flip_var(rand_tied))

                self.variable[i] = self.flip_var(rand_tied)

        # return truth assignment of alpha if found
        print("no satisfying assignment found")
        return

    def write_solution(self, filename):
        file = open(filename, "w")
        for var in self.variable:
            print(var, file=file)

    def WalkSAT(self):
        pass


if __name__ == "__main__":

    print("Hello World")