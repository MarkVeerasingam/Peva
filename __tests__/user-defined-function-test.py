from test_util import test
from run import Run

test(Run.peva,"""
    (begin
        (def square (x) (* x x))
        (square 2)
     )
     """, 4)

test(Run.peva,"""
    (begin
        (def calc(x y) 
            (begin
                (var z 30)
                (+ (* x y) z)
            )
        )
        (calc 10 20)
    )
    """, 230)

# closure test
test(Run.peva,"""
    (begin
        (var value 100)
        (def calc (x y)
            (begin 
                (var z (+ x y))
                (def inner (foo)
                    (+ (+ foo z) value))
                inner
                )
            )
        (var fn (calc 10 20))
        (fn 30)
    )
    """, 160)

# recursive functions
test(Run.peva,
    """
    (begin
      (def factorial (x)
        (if (= x 1)
          1
          (* x (factorial (- x 1)))))

      (factorial 5)
    )
    """, 120)