from copy import deepcopy
import random

class Cell:

    def __init__(self, v = 0, o = []):
        self.v = v
        self.o = o

    def __str__(self):
        # return "{0}".format(self.v)
        return "<{0}>".format(self.v) if self.is_hardcoded() else "{0}{1}".format(self.v, self.o) 

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other): 
            return self.v == other.v and self.o == other.o

    def is_hardcoded(self):
        return True if 0 == len(self.o) else False

    def get_next(self):
        if 0 == len(self.o):
            return None

        nxt = self.o.pop(0)
        
        return Cell(nxt)

# make sure the hard-coded cells are unique
# returns true if the rule imposing is possible
def impose_rule(cls):
    fcs = [cell for cell in cls if not cell.is_hardcoded()]
    if 0 == len(fcs):
        # nothing to do...
        return True

    hcs = [cell for cell in cls if cell.is_hardcoded()]

    for hc in hcs:
        for fc in fcs:
            if hc.v in fc.o:
                fc.o.remove(hc.v)

    broken_cells = [cell for cell in cls if (cell.is_hardcoded() and 0 == cell.v)]
    return 0 == len(broken_cells)

class Board:
    def __init__(self, data):
        self.sol_depth = 0

        self.d = [[i] * 9 for i in range(9)]

        all_ops = list([i for i in range(1,10)])
        for i in range(9):
            for j in range(9):
                self.d[i][j] = Cell(0,all_ops.copy())      

        for i, c in enumerate(data):
            self.d[i//9][i%9] = self.d[i//9][i%9] if '?' == c else Cell(int(c))

            
    def __str__(self):
        res = ""
        for r, row in enumerate(self.d):
            res += ' '.join([str(elem) for elem in row[0:3]]) +  ' | ' \
                + ' '.join([str(elem) for elem in row[3:6]]) +  ' | ' \
                + ' '.join([str(elem) for elem in row[6:9]]) + "\n" 
            if 2 == r or 5 == r:
                res += "------------|-------------|-------------\n"
        return res


    def __repr__(self):
        return self.__str__()


    def rows_counter(self, start=0, amt = 0):
        cur = start
        while cur < (9 if 0 == amt else start+amt):
            yield self.d[cur]
            cur += 1


    def columns_counter(self, start=0, amt = 0):
        cur = start
        while cur < (9 if 0 == amt else start+amt):
            yield [r[cur] for r in self.rows_counter()]
            cur += 1

    
    def boxes_counter(self):
        for i in range(0,3):
            for j in range(0,3):
                box = []
                for row in self.rows_counter(3*i, 3):
                    box.append(row[3*j+0])
                    box.append(row[3*j+1])
                    box.append(row[3*j+2])
                
                yield box


    def solved(self):
        for row in self.rows_counter():
            broken_cells = [cell for cell in row if (cell.is_hardcoded() and 0 == cell.v)]
            if 0 != len(broken_cells):
                exit()

            solved_cells = [cell for cell in row if (cell.is_hardcoded() and 0 != cell.v)]
            if 9 != len(solved_cells):
                return False

        return True
            

    #  returns true, if there is no conflict
    def sync_cells(self):
        for row in self.rows_counter():
            if not impose_rule(row):
                return False

        for col in self.columns_counter():
            if not impose_rule(col):
                return False

        for box in self.boxes_counter():
            if not impose_rule(box):
                return False

        for row in self.rows_counter():
            for cell in row:
                if 1 == len(cell.o):
                    # print("Nailed {0} in {1}".format(cell,row))
                    cell.v = cell.o[0]
                    cell.o = []
                    if not self.sync_cells():
                        return False
        
        return True


    def solve(self):
        self.sol_depth += 1

        if not self.sync_cells():
            # print("Deadend @{0}".format(self.sol_depth))
            self.sol_depth -= 1
            return

        # print("Solving @{0}".format(self.sol_depth))
        # print(self)

        if self.solved():
            print("### SOLVED @{0} ###".format(self.sol_depth))
            print(self)
            self.sol_depth -= 1
            return

        # UF pick the shortest cell
        for r, row in enumerate(self.rows_counter()):
            for c, cell in enumerate(row):
                if cell.is_hardcoded():
                    continue

                nxt = deepcopy(self)
                nxt.d[r][c] = cell.get_next()
                # print("Let's try {0} at [{1}:{2}]".format(nxt.d[r][c].v,r,c))

                nxt.solve()

        self.sol_depth -= 1
        return


def main():
        b = Board("\
??????4??\
?9?7????5\
17?9?4???\
24?3??8??\
8???????3\
??3??2?91\
???5?6?32\
5????7?1?\
??1??????\
")
        b.solve()
        
if __name__ == '__main__':
    main()

