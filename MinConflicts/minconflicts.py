import sys,time,random,queue
from functools import reduce
from collections import defaultdict
class minconflicts:

    def __init__(self, variables, domains, neighbours):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.assignment = {}
        self.length = len(self.domains[self.variables[0]])
        self.counter = 0
        self.num_explored = 0

    # assigns values to variables
    def assign(self, var, val):
        self.assignment[var] = val
        return (self.assignment)

    # checks if an assignment is consistent or not
    def consistent(self, var, val):
        for var in self.neighbours[var]:
            if var in self.assignment.keys():
                if self.assignment[var] == val:
                    return False
        return True

    #for final check on number of conflicts
    def nconflicts(self):
        count = 0
        for var in self.variables:
            if var in self.assignment.keys():
                if not self.consistent(var, self.assignment[var]):
                    count += 1
        return count

    # number of conflicts on each variable
    def var_nconflicts(self, var):
        count = 0
        if var in self.assignment.keys():
            if not self.consistent(var, self.assignment[var]):
                count += 1
        return count

    # unassign a value
    def unassign(self, var):
        self.assignment[var] = -1

    # Return a list of variables in current assignment that are in conflict
    def conflicted_vars(self):
        return [var for var in self.variables
                if self.var_nconflicts(var) > 0]

    # Implements min_conflicts
    def min_conflicts(self, steps):
        start_time = time.time()
        for var in self.variables:
            val = random.randint(0,3)
            self.assign(var, str(val))
        for i in range(steps):
            if time.time() > start_time + 60:
                print("Reached time limit of 60 seconds")
                print("Searched nodes:", self.num_explored)
                exit()
            conflicted = self.conflicted_vars()
            print(len(conflicted))
            if not conflicted:
                return self.assignment
            var = random.choice(conflicted)
            val = self.min_conflicts_value(var)
            #print(val)
            self.assign(var, val)
            self.num_explored += 1
        return None

    # Returns a minumum conflicted value
    def min_conflicts_value(self, var):
        found = 0
        min = 10000
        for val in self.domains[var]:
            self.assign(var,val)
            count = self.var_nconflicts(var)
            if count < min :
                min_value = val
                min = count
                found = 1
            elif count == min :
                found += 1
                if random.randrange(found) == 0:
                    min_value = val
        return min_value


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Illegal use of Arguments :")
    else:
        input = sys.argv[1]
        output = sys.argv[2]
        constraints = []
        i = 1
        with open(input) as files:
            alist = [line.rstrip() for line in files]
            csp_inputs = (alist[0]).split("\t")
            n = int(csp_inputs[0])
            m = int(csp_inputs[1])
            k = int(csp_inputs[2])
            count = (len(alist))
            neighbours = {}
            variables = []
            domains = dict()

            for i in range(n):
                variables.append(str(i))
            #print(variables)

            values = list(map(str,range(k)))
            for var in variables:
                domains[var] = values

            #print("domains", domains)

            for key in variables:
                neighbours[key] = set()
            i = 1
            while (i <= count-1):
                k_v = alist[i].split("\t")
                neighbours[k_v[0]].add(k_v[1])
                neighbours[k_v[1]].add(k_v[0])
                i += 1
            #print(neighbours)
        out = minconflicts(variables, domains, neighbours)
        assignment = {}
        start_time = time.time()
        a = out.min_conflicts(1000000)
        print("--- %s seconds ---" % (time.time() - start_time))
        print("min_conflicts")
        print(a)
        print("Number of conflicts",out.nconflicts())
        print ("Num of search steps:",out.num_explored)
        with open(output, 'w') as f:
            for key in out.assignment.keys():
                f.write(str(out.assignment[key]))
                f.write("\n")


