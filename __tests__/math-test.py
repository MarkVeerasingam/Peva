from run import Run

# math test:
Run.test((['+', ['+', 3, 2], 5]), 10)
Run.test((['-', 10, 5]), 5)
Run.test(['-', ['*', 6, 5], ['-', 10, 5]], 25)
Run.test((['*', ['*', 3, 2], 5]),30)
Run.test((['/', ['*', 6, 5], 5]),6)
