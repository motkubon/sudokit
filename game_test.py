import unittest
from game import Cell, Board, impose_rule





class TestCellMethods(unittest.TestCase):

    def test_compare_cells(self):
        self.assertTrue(Cell(1,[2,3,4]) == Cell(1,[2,3,4]))
        self.assertTrue(Cell(1,[2,3,4]) != Cell(7,[2,3,4]))
        self.assertTrue(Cell(1,[2,3,4]) != Cell(1,[3,4]))

    def test_modify_cells(self):
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
        self.assertEqual(b.d[0][0].v, b.d[0][1].v, "Identical")
        b.d[0][0].v = -1
        self.assertNotEqual(b.d[0][0].v, b.d[0][1].v, "Identical")

        self.assertEqual(b.d[0][0].o[0], b.d[0][1].o[0], "Identical")
        b.d[0][0].o[0] = -2
        self.assertNotEqual(b.d[0][0].o[0], b.d[0][1].o[0], "Not identical anymore")


    def test_get_next(self):
        c = Cell(0,[2,3,4,5,6,7,8,9])
        c1 = c.get_next()
        
        # c wasn't affected
        self.assertEqual(c, Cell(0,[3,4,5,6,7,8,9]))

        # c1 is sc's next, and hard-coded
        self.assertEqual(c1, Cell(2,[]))

    def test_rule(self):
        batch = [Cell(1), Cell(5), Cell(0,[1,2,3,4,5,6])]
        impose_rule(batch)

        self.assertEqual(batch[2].v, 0, "The value didn't change")
        self.assertEqual(batch[2].o, [2,3,4,6], "The options were reduced")

    def test_rule_enforcement(self):
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
        b.sync_cells()
        self.assertEqual(Cell(0,[3,6]), b.d[0][0])
        self.assertEqual(Cell(8,[]), b.d[6][1])


if __name__ == '__main__':

    unittest.main()

