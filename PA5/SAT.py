import random
import copy
import Sudoku

class SAT:

    def __init__(self, puzzle):

        # sudoku problem
        self.puzzle = puzzle
        self.variable = [ ] # list or set of variables (first line)
        self.clause = [ ] # constraint list is clause list (create rules) # list of set
        #self.clause = { }
        self.gen_var_clause()
        self.threshold = 0.9

        # dictionary
        print("CNF file: ", puzzle)
        print("Variable: ", self.variable)
        print("Clause: ", self.clause)

        self.random_assignment(self.variable)
        print("Randomly assigned: ", self.variable)

        # set should convey rule - split line put into list
        # read file nad loop through variables

    def gen_var_clause(self):

        # read file
        file = open(self.puzzle, "r")
        curr_var = None

        for line in file:
            if len(line) == 38:
                for var in line.split():
                    self.variable.append(var)
                    curr_var = var[:2]
                #self.clause[curr_var] = [ ]
                #self.clause["-"+curr_var] = [ ]

            elif len(line) == 11 or len(line) == 37:
                temp = set()
                for c in line.strip().split():
                    temp.add(c)
                #self.clause[curr_var].append(temp)
                #self.clause["-"+curr_var].append(temp)

                self.clause.append(temp)


        # generate variables
        # firstline = f.readline()
        # print("first", len(firstline), firstline)
        # for var in firstline.split():
        #     print("var,", var)
        #     self.variable.append(var)
        #
        # for line in f.read().splitlines():
        #     print("rest", len(line), line)
        #     temp = set()
        #     temp.add(line[0:4])
        #     temp.add(line[4:9])
        #     self.clause.append(temp)

    # sat helper scores the variable

    # checks that all clauses satisfied
    def clause_satisfy(self):

        # for v in self.variable:
        #     for item in self.clause[v[:3]]:
        #         item = list(item)
        #         if item[0] not in self.variable and item[1] not in self.variable:
        #             # if "-" in item[0] and "-" in item[0]:
        #             return False
        for item in self.clause:
            item = list(item)
            if item[0] not in self.variable and item[1] not in self.variable:
            # if "-" in item[0] and "-" in item[0]:
                return False

        return True


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

    def clause_score(self, rand_var):
        score = 0
        variable_copy = copy.copy(self.variable)
        i = variable_copy.index(rand_var)
        variable_copy[i] = self.flip_var(rand_var)

        for item in self.clause:
        # for item in self.clause[rand_var[:-1]]:
            item = list(item)
            if item[0] not in variable_copy and item[1] not in variable_copy:
            # if "-" in item[0] and "-" in item[0]:
                return score
            score += 1
        return score


    # input: set of clause (alpha)
    # MAX_FLIPS, MAX_TRIES
    def GSAT(self, max_flip=10, max_tries=10):

        # 100,000
        for i in range(1, max_tries + 1):

            # randomly generate truth assignment
            self.random_assignment(self.variable)

            # 100,000
            for j in range(1, max_flip + 1):
                if self.clause_satisfy():
                    print("satisfie: ", self.variable)
                    return self.variable


                # threshold is 0.9
                if random.uniform(0, 1) > self.threshold:
                    #print('stop1')
                    self.flip_var(random.choice(self.variable))
                    continue

                else:
                    #print('stop2')

                    max_score = float('-inf')
                    tied = [ ]

                    for var in self.variable:
                        #print('stop3')

                        score = self.clause_score(var)

                        if score > max_score:
                            max_score = score
                            tied = [ ]
                            tied.append(var)

                        elif score == max_score:
                            tied.append(var)

                        else:
                            continue

                if tied and len(tied) > 0:
                    self.flip_var(random.choice(tied))
                    continue

                # get satisfy and unsatisfy

                # if not all saitsfy
                # check if random > heurisitc
                    # get random and flip it
                # if it is less
                    # otherwise se set

                # if truth satisfies alpha
                # create dictionary from variables to index to assignment
                ## can also do when print out

                # any(clause[v]==assignment[v] for v in assignment)

                # p is a propositional variable such that its
                # truth assignment gives largest increase in total number
                # of clauses of alpha that are satisfied by T
                #
                # random_truth with the truth assignment of p reversed

        # return truth assignment of alpha if found
        return "no satisfying assignment found"

    def write_solution(self, filename):
        file = open(filename, "w")
        for var in self.variable:
            print(var, file=file)

    def WalkSAT(self):
        pass


if __name__ == "__main__":

    print("Hello World")