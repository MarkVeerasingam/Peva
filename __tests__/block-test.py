from run import Run
import test_util as testUtil

Run.test(
    ['begin', 
     ['var', 'x', 10],
     ['var', 'y', 20],
     ['+', ['*', 'x', 'y'], 30]
    ], 230)

# evaluating a block in its own environment
Run.test(
    ['begin', 
     ['var', 'x', 10],
     ['begin',
        ['var', 'x', 20],
        'x'
    ],
    'x'
    ], 10)

# access of variables from the outer environment
Run.test(
    ['begin', 
     ['var', 'value', 10],
     ['var', 'result', 
      ['begin',
        ['var', 'x', ['+', 'value', 10]],
        'x'
    ]],  
    'result'
    ], 20)

# assignment will be represented as the "set" instruction  
Run.test(
    ['begin', 
    ['var', 'data', 10],
    ['begin',
        ['set', 'data', 100]
    ],  
    'data'
    ], 100)

testUtil.test(Run.peva, 
              """
              (begin
                (var x 10)
                (var y 20)
                (+ (* x 10) y))
              """, 120) 