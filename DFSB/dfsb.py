import sys, time
from collections import defaultdict
from copy import deepcopy
import queue, signal


class csp:
    def __init__(self, variables, domains, neighbours):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.assignment = defaultdict(lambda: None)
        self.length = len(self.domains[self.variables[0]])
        self.arc_count = 0
        self.num_assignments = 0
        self.arc_prunned = 0

    # function defined for assigning a value to a variable
    def assign(self, var, val):
        self.assignment[var] = val
        return (self.assignment)

    #function selects an unassigned variable, takes one
    #argument mrv if the value is 1 then selects a variable with
    #minimum remaining value else selects a first encountered unassigned variable
    def select_unassigned_variable(self, mrv):
        if mrv:
            min_val_count = self.length
            min_var = self.variables[0]
            for var in self.variables:
                if self.assignment[var] is None:
                    length = len(self.domains[var])
                    if length < min_val_count:
                        min_var = var
                        min_val_count = length
            return min_var

        for v in self.variables:
            if self.assignment[v] is None:
                return v

    # checks if the assignment is consistent
    def consistent(self, var1, val):
        for var in self.neighbours[var1]:
            if self.assignment[var] == val:
                return False
        return True

    # removes an assignment
    def unassign(self, var):
        self.assignment[var] = None

    # implements arc consistency
    def ac_3(self, v):
        q = queue.Queue()
        for var in self.neighbours[v]:
            q.put((var, v))
        while not q.empty():
            var1, var2 = q.get()
            if self.remove_inconsistent_values(var1, var2):
                self.arc_prunned += 1
                for variable in self.neighbours[var1]:
                    q.put((variable, var1))

    # removes inconsistent values from a variable domain
    def remove_inconsistent_values(self, neighbor, var) :
        ret = False
        for value in self.domains[neighbor] :
            if self.assignment[var] == value :
                self.domains[neighbor].remove(value)
                ret = True
            if self.assignment[var] is None :
                if (value in self.domains[var] and len(self.domains[var]) == 1):
                    self.domains[neighbor].remove(value)
                    ret = True
        return ret

    # checks if the assignment is complete
    def goal_test(self):
        for var in self.variables:
            if self.assignment[var] is None:
                return False
        return True

    #If the lcv=1 then orders domain of a variable by
    #least constrained value else returns domain
    def order_domain_value(self, var, lcv):
        domain = self.domains[var]
        if lcv:
            domain_count = []
            for x in domain:
                domain_count.append(0)
            for (i, val) in zip(range(len(domain)), domain):
                for neighbour in self.neighbours[var]:
                    if self.assignment[neighbour] is None and val in self.domains[neighbour]:
                        domain_count[i] += 1
            self.domains[var] = [x for (y, x) in sorted(zip(domain_count, domain))]
        return self.domains[var]

    ''' This function implements both dfsb and dfsb++ depending on arguments passed
     if lcv, mrv and ac3 are passed as 1 then it performs dfsb++ and
     if they are zero it performs simple dfsb'''

    def rec_backtracking(self,lcv,mrv,ac3,start_time):
        if time.time() > start_time + 60:
            print("Reached time limit of 60 seconds")
            print("Searched nodes:", self.num_assignments)
            exit()
        if (self.goal_test()):
            return True
        print(len([var for var in self.variables if self.assignment[var] is None]))
        var = self.select_unassigned_variable(mrv)
        for val in self.order_domain_value(var,lcv):
            if self.consistent(var, val):
                self.assignment[var] = val
                self.num_assignments += 1
                domain_copy = deepcopy(self.domains)
                if ac3 == 1:
                    self.ac_3(var)
                result = self.rec_backtracking(lcv,mrv,ac3,start_time)
                if result == True:
                    return True
                self.unassign(var)
                self.domains = domain_copy
        return False

    #Implemented to check if there are any conflicts
    def no_of_conflicts(self):
        count = 0
        for var in self.variables:
            if not self.consistent(var, self.assignment[var]):
                count += 1
        return count

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ("Illegal use of Arguments : Expected format --> python dfsb.py <input_file> <mode_flag>")
    else:
        input = sys.argv[1]
        mode =  int(sys.argv[3])
        if mode != 0 and mode != 1:
            print("Illegal usage of mode")
            exit()
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
                domains[var] = deepcopy(values)

            #print("domains", domains)
            for key in variables:
                neighbours[key] = set()
            i = 1
            while (i <= count-1):
                k_v = alist[i].split("\t")
                neighbours[k_v[0]].add(k_v[1])
                neighbours[k_v[1]].add(k_v[0])
                i += 1
           
            start_time = time.time()
            out = csp(variables, domains, neighbours)
            #simple DFSB
            if mode == 0:
                out.rec_backtracking(0,0,0, start_time)
            #DFSB++
            if mode == 1:
                print(out.rec_backtracking(1,1,1,start_time))
            print(out.assignment)
            print("Searched nodes:", out.num_assignments)
            print(out.arc_count)
            print("Number of conflicts:",out.no_of_conflicts())
            print("Arc prunned:", out.arc_prunned)
            print("--- %s seconds ---" % (time.time() - start_time))
            
