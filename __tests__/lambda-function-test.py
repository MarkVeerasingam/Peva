from run import Run
from test_util import test

test(Run.peva,
     """
    (begin
        (def onClick (callback)
        (begin
            (var x 10)
            (var y 20)
            (callback (+ x y))))

        (onClick (lambda (data) (* data 10)))
    )
    """, 300)

# immeditatley-invoked lambda expression - IILE:
test(Run.peva,
    """
    ((lambda (x) (* x x)) 2)
    """, 4)

# save a lambda function to a variable:
test(Run.peva,
    """
    (begin
        (var square (lambda (x) (* x x)))
        (square 2)
    )
    """, 4)