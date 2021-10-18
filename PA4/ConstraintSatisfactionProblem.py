class ConstraintSatisfactionProblem():
    def __init__(self, variable, domain):
        self.variable = variable
        self.domain = domain
        self.constraint = self.generate_constraint()
        self.assignment = { }


    def generate_constraint(self):

        # self.constraint
        output = { }

        # assume variable is an array of integer
        # for each pair of variables
        for i in range(1, len(self.variable)):
            for j in range(0, i):
                # create a list to store constraints
                output[(j, i)] = [ ]
                # append possible pair of domain values
                # switched pairs can also work
                for m in range(1, len(self.domain)):
                    for n in range(0, m):
                        output[(j, i)].append((n, m))
                        output[(j, i)].append((m, n))

        return output

    def constraint_satisfy(self, state):

        #state = list(state)
        curr_var = state[0]
        # for v in range(curr_var, len(self.variable)):

        for i in range(curr_var-1, -1, -1):

            print("looking at", i, curr_var)
            # check if domain pair is in constraint for given variables
            if (state[i+1], state[curr_var+1]) not in self.constraint[(i, curr_var)]:
                print("Not found: ", (state[i+1], state[curr_var+1]))
                return False

        return True

    # (index_altered, var1, var2, etc)
    def get_successors(self, state):

        # list of successors
        successors = [ ]
        state = list(state)
        curr_domain = state[0]

        # return empty list if out of variables
        if state[0] + 1 < len(self.variable):
            next_var = state[0] + 1
        else:
            # reached leaf node
            return [ ]

        new_state = [next_var] + state[1:]
        for d in self.domain:
            # add one since first element is next_var
            new_state[next_var+1] = d
            print('new state', new_state)

            if self.constraint_satisfy(new_state):
                successors.append(tuple(new_state))

        return successors

def main():
    csp_problem = ConstraintSatisfactionProblem([0, 1, 2], [0, 1, 2])
    print("Constraints generated: ", csp_problem.constraint)
    print("Number of constraints: ", len(csp_problem.constraint))
    print("Successor generated: ", csp_problem.get_successors((0, 1, 0, 0)))


if __name__ == '__main__':
    main()
