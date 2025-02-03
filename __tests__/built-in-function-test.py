from test_util import test
from run import Run

test(Run.peva,"""(+ 1 5)""",6)
test(Run.peva,"""(+ (+ 2 3) 5)""",10)
test(Run.peva,"""(+ (+ 2 3) 5)""",10)

test(Run.peva,"""(> 1 5)""", False)
test(Run.peva,"""(< 1 5)""", True)

test(Run.peva,"""(>= 5 5)""", True)
test(Run.peva,"""(<= 5 5)""", True)
test(Run.peva,"""(= 5 5)""", True)