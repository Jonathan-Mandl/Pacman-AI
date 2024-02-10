import unittest
import ex1
import search
from ex1_check import run_problem


def solve_problems(problem, algorithm):
    for row in problem:
        print(row),
    print

    try:
        p = ex1.create_pacman_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.breadth_first_graph_search(p)), targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        return len(solution), solution
    else:
        return None, None


class TestPacmanSolver(unittest.TestCase):

    def test_case_1(self):
        problem = (
            (10, 10, 10, 11),
            (10, 99, 10, 50),
            (10, 10, 10, 10),
            (77, 10, 10, 10),
        )
        expected_solution = (6, ['U', 'U', 'U', 'R', 'R', 'R'])

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs[0], expected_solution[0])
        self.assertEqual(result_astar[0], expected_solution[0])

    def test_case_2(self):
        problem = (
            (11, 10, 50, 10),
            (10, 99, 99, 11),
            (20, 10, 10, 10),
            (77, 10, 10, 10),
        )
        expected_solution_gbfs = (11, ['R', 'L', 'U', 'R', 'R', 'R', 'U', 'U', 'L', 'L', 'L'])
        expected_solution_astar = (11, ['R', 'L', 'U', 'R', 'R', 'R', 'U', 'U', 'L', 'L', 'L'])

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs[0], expected_solution_gbfs[0])
        self.assertEqual(result_astar[0], expected_solution_astar[0])

    def test_case_3(self):
        problem = (
            (11, 10, 10, 21),
            (10, 10, 40, 10),
            (10, 50, 77, 10),
            (31, 10, 10, 11),
        )
        expected_solution_gbfs = (None, None)
        expected_solution_astar = (None, None)

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs, expected_solution_gbfs)
        self.assertEqual(result_astar, expected_solution_astar)

    def test_case_4(self):
        problem = (
            (10, 10, 10, 30, 99, 10),
            (10, 11, 11, 10, 10, 10),
            (77, 10, 11, 10, 10, 10),
            (10, 10, 10, 99, 10, 10),
            (99, 10, 11, 10, 10, 10),
            (10, 10, 21, 10, 10, 10),
        )
        expected_solution_gbfs = (25,
                                  ['U', 'U', 'D', 'D', 'D', 'U', 'R', 'R', 'R', 'R', 'D', 'R', 'L', 'U', 'L', 'L', 'D',
                                   'D', 'D', 'L', 'U', 'U', 'U', 'U', 'R'])
        expected_solution_astar = (25,
                                   ['R', 'R', 'L', 'L', 'D', 'U', 'R', 'R', 'R', 'R', 'D', 'R', 'L', 'U', 'L', 'L', 'D',
                                    'D', 'D', 'L', 'U', 'U', 'U', 'U', 'R'])

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs[0], expected_solution_gbfs[0])
        self.assertEqual(result_astar[0], expected_solution_astar[0])

    def test_case_5(self):
        problem = (
            (11, 10, 11, 99, 10, 99, 20, 99),
            (10, 99, 10, 77, 99, 99, 99, 99),
            (10, 99, 10, 10, 10, 99, 10, 10),
            (10, 10, 10, 10, 10, 99, 99, 10),
            (99, 30, 10, 99, 10, 10, 99, 11),
            (10, 10, 99, 99, 10, 99, 99, 10),
            (99, 10, 10, 99, 11, 10, 99, 10),
            (99, 10, 11, 99, 99, 10, 10, 10),
        )

        expected_solution_gbfs = (33,
                                  ['D', 'U', 'L', 'U', 'L', 'L', 'D', 'D', 'D', 'R', 'D', 'D', 'D', 'D', 'R', 'L', 'U',
                                   'U', 'U', 'U', 'R', 'R', 'R', 'D', 'D', 'D', 'R', 'D', 'R', 'R', 'U', 'U', 'U'])
        expected_solution_astar = (33,
                                   ['L', 'D', 'U', 'U', 'L', 'L', 'D', 'D', 'D', 'R', 'D', 'D', 'D', 'R', 'D', 'L', 'U',
                                    'U', 'U', 'R', 'U', 'R', 'R', 'D', 'D', 'D', 'R', 'D', 'R', 'R', 'U', 'U', 'U'])
        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs[0], expected_solution_gbfs[0])
        self.assertEqual(result_astar[0], expected_solution_astar[0])


    def test_case_6(self):
        problem = (
            (10, 21, 10, 11, 11, 10, 11, 99),
            (10, 99, 99, 10, 10, 99, 10, 10),
            (10, 99, 77, 10, 99, 99, 99, 99),
            (10, 10, 10, 10, 10, 10, 99, 99),
            (11, 10, 10, 99, 10, 10, 10, 99),
            (10, 99, 99, 10, 99, 99, 10, 99),
            (99, 30, 99, 10, 10, 10, 11, 99),
            (99, 10, 99, 10, 99, 10, 40, 99),
        )

        expected_solution_gbfs = (52,
                                  ['D', 'R', 'R', 'R', 'D', 'R', 'L', 'U', 'L', 'L', 'L', 'D', 'L', 'L', 'U', 'U', 'U',
                                   'U', 'R', 'R', 'R', 'D', 'D', 'D', 'R', 'D', 'R', 'R', 'D', 'D', 'D', 'L', 'U', 'R',
                                   'U', 'U', 'L', 'U', 'L', 'L', 'L', 'L', 'L', 'U', 'U', 'U', 'R', 'R', 'R', 'R', 'R',
                                   'R'])
        expected_solution_astar = (52,
                                   ['R', 'D', 'R', 'R', 'D', 'R', 'L', 'U', 'L', 'L', 'L', 'D', 'L', 'L', 'U', 'U', 'U',
                                    'U', 'R', 'R', 'R', 'D', 'D', 'D', 'R', 'D', 'R', 'R', 'D', 'D', 'D', 'L', 'U', 'R',
                                    'U', 'U', 'L', 'U', 'L', 'L', 'L', 'L', 'L', 'U', 'U', 'U', 'R', 'R', 'R', 'R', 'R',
                                    'R'])

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs[0], expected_solution_gbfs[0])
        self.assertEqual(result_astar[0], expected_solution_astar[0])

    def test_case_7(self):
        problem = (
            (10, 10, 10, 10),
            (10, 77, 11, 20),
            (10, 99, 10, 10),
            (10, 10, 10, 10),
        )
        expected_solution_gbfs = (7, ['L', 'D', 'D', 'U', 'U', 'R', 'R'])
        expected_solution_astar = (7, ['L', 'D', 'D', 'U', 'U', 'R', 'R'])

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs[0], expected_solution_gbfs[0])
        self.assertEqual(result_astar[0], expected_solution_astar[0])

    def test_case_8(self):
        problem = (
            (11, 10, 10, 10, 10),
            (99, 77, 10, 10, 10),
            (10, 10, 10, 10, 10),
            (10, 10, 10, 31, 10),
            (10, 10, 10, 10, 10),
        )
        expected_solution_gbfs = (None, None)
        expected_solution_astar = (None, None)

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs, expected_solution_gbfs)
        self.assertEqual(result_astar, expected_solution_astar)

    def test_case_9(self):
        problem = (
            (51, 99, 10),
            (11, 99, 10),
            (11, 11, 77),
        )
        expected_solution_gbfs = (None, None)
        expected_solution_astar = (None, None)

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs, expected_solution_gbfs)
        self.assertEqual(result_astar, expected_solution_astar)


    def test_case_10(self):
        problem = (
            (10, 10, 11, 10, 10, 10, 10, 11, 10, 10),
            (10, 10, 10, 10, 99, 10, 10, 10, 10, 10),
            (10, 77, 10, 10, 10, 10, 10, 10, 10, 10),
            (10, 10, 10, 10, 10, 10, 30, 10, 10, 10),
            (10, 10, 10, 10, 10, 10, 10, 10, 10, 10),
            (11, 10, 10, 10, 10, 21, 10, 10, 10, 11),
            (10, 10, 10, 10, 10, 99, 10, 10, 10, 10),
            (10, 10, 10, 10, 40, 10, 10, 10, 10, 10),
            (10, 10, 10, 10, 10, 10, 10, 10, 10, 10),
            (10, 10, 10, 11, 10, 10, 51, 10, 10, 10),
        )
        expected_solution_gbfs = (None, None)
        expected_solution_astar = (None, None)

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs, expected_solution_gbfs)
        self.assertEqual(result_astar, expected_solution_astar)


    def test_case_11(self):
        problem = (
            (30, 10, 10, 10, 10, 10, 10, 10),
            (40, 77, 11, 10, 10, 10, 10, 10),
            (10, 99, 10, 10, 99, 10, 10, 10),
            (10, 10, 10, 10, 10, 10, 10, 10),
            (10, 10, 10, 10, 10, 10, 10, 10),
            (10, 99, 10, 10, 10, 10, 10, 10),
            (10, 10, 10, 10, 10, 10, 10, 10),
            (10, 10, 10, 10, 10, 10, 10, 11),
        )
        expected_solution_gbfs = (12, ['R', 'D', 'D', 'D', 'D', 'D', 'D', 'R', 'R', 'R', 'R', 'R'])
        expected_solution_astar = (12, ['R', 'D', 'D', 'D', 'D', 'D', 'D', 'R', 'R', 'R', 'R', 'R'])

        result_gbfs = solve_problems(problem, "gbfs")
        result_astar = solve_problems(problem, "astar")

        self.assertEqual(result_gbfs[0], expected_solution_gbfs[0])
        self.assertEqual(result_astar[0], expected_solution_astar[0])


if __name__ == '__main__':
    unittest.main()
