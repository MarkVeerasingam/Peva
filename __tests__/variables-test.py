from run import Run

# variables test:
Run.test(['var', 'x', 10], 10)
Run.test(('x'), 10)
Run.test(['var', 'y', 100], 100)
Run.test(('y'), 100)

Run.test(['var', 'isUser', 'true'], True)
Run.test(['var', 'z', ['*', 2, 2]], 4)
Run.test(('z'), 4)