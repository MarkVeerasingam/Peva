from run import Run
from test_util import test

test(Run.peva,"""
    (begin
      (var x 10)
      (switch ((= x 10) 100)
              ((> x 10) 200)
              (else 100))
    )
    """, 100)