from run import Run
from test_util import test

test(Run.peva,"""
    (begin
      (var x 0)
      (for (set x 0) (< x 5) (set x (+ x 1))
        x)
      x)
    """, 5)

# Test for increment (++)
test(Run.peva, """
    (begin
      (var x 0)
      (for (set x 0) (< x 5) (++ x)
        x)
      x)
    """, 5)

# Test for decrement (--)
test(Run.peva, """
    (begin
      (var x 5)
      (for (set x 5) (> x 0) (-- x)
        x)
      x)
    """, 0)