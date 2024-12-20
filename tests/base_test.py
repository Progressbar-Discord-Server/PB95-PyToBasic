import unittest
import ast
from src import statements
from src import expressions

class IndependentTests(unittest.TestCase):

    def test_assignments(self):

        tests = [ast.parse(command) for command in [
            "a = 10",
            "a = b",
            "a, b = 10, 20",
            "a, b = c, 20",
            "a = 10 + 5",
            "a = 10 - 5 * 2 + 7",
            "a = 10 - (5 + 2)",
            "a = 10 - 5 + 2",
            "a = 10 - (25 * 25)",
            "a = 10 * (25 / 100)",
            "a = 'string'",
            "a, b = 10, 'string'",
            "a, b = 'string', 'string'",
            "a = 5 == 5"
        ]]

        results = []
        for test in tests:
            for obj in test.body:
                if isinstance(obj, ast.Assign):
                    for inst in statements.assign(obj):
                        results.append(inst)

        self.assertEqual("LET a=10", results[0])
        self.assertEqual("LET a=b", results[1])

        self.assertEqual("LET a=10", results[2])
        self.assertEqual("LET b=20", results[3])

        self.assertEqual("LET a=c", results[4])
        self.assertEqual("LET b=20", results[5])

        self.assertEqual("LET a=10 + 5", results[6])
        self.assertEqual("LET a=10 - 5 * 2 + 7", results[7])
        self.assertEqual("LET a=10 - (5 + 2)", results[8])
        self.assertEqual("LET a=10 - 5 + 2", results[9])
        self.assertEqual("LET a=10 - 25 * 25", results[10])
        self.assertEqual("LET a=10 * (25 / 100)", results[11])

        self.assertEqual('LET a="string"', results[12])

        self.assertEqual('LET a=10', results[13])
        self.assertEqual('LET b="string"', results[14])

        self.assertEqual('LET a="string"', results[15])
        self.assertEqual('LET b="string"', results[16])

        self.assertEqual('LET a=5==5', results[17])

    def test_call(self):
        """If print works - all other calls should be working."""

        tests = [ast.parse(command) for command in [
            "print(100)",
            "print('100')",
            "print(a)",
            "print(50 + 50)",
        ]]

        results = []
        for test in tests:
            for obj in test.body:
                if isinstance(obj, ast.Expr):
                    if isinstance(obj.value, ast.Call):
                        results.append(expressions.call(obj.value))

        self.assertEqual("PRINT 100", results[0])
        self.assertEqual('PRINT "100"', results[1])
        self.assertEqual("PRINT a", results[2])
        self.assertEqual("PRINT (50 + 50)", results[3])

    def test_if_statement(self):
        test = "if a == b:\n" \
               "    if a == b:\n" \
               "        print(15)\n" \
               "    else:\n" \
               "        print(25)\n" \
               "else:\n" \
               "    if a == b:\n" \
               "        print(15)\n" \
               "    else:\n" \
               "        print(25)\n"
        expected = [
            "IF a==b THEN GOTO 4",
            "IF a==b THEN PRINT 15",
            "ELSE PRINT 25",
            "GOTO 3",
            "IF a==b THEN PRINT 15",
            "ELSE PRINT 25",
            "REM *ELSE EXIT*",
        ]

        tree = ast.parse(test)

        for obj in tree.body:
            if isinstance(obj, ast.If):
                for i, inst in enumerate(statements.create_if(obj)):
                    self.assertEqual(expected[i], inst)

    def test_for_loop(self):
        test = "for a in range(1, 11):\n" \
               "    print(a)\n"
        expected = [
            "FOR a=1 TO 10",
            "PRINT a",
            "NEXT a"
        ]

        tree = ast.parse(test)

        for obj in tree.body:
            if isinstance(obj, ast.For):
                for i, inst in enumerate(statements.create_for(obj)):
                    self.assertEqual(expected[i], inst)
    
    def test_while_loop(self):
        test = "while a == 5:\n" \
               "    print(a)"
        expected = [
            "IF a!=5 THEN GOTO 3",
            "PRINT a",
            "IF a==5 THEN GOTO -1",
            "REM *WHILE EXIT*"
        ]

        tree = ast.parse(test)

        for obj in tree.body:
            if isinstance(obj, ast.While):
                for i, inst in enumerate(statements.create_while(obj)):
                    self.assertEqual(expected[i], inst)

if __name__ == '__main__':
    unittest.main()
