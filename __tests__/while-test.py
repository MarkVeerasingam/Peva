from run import Run

Run.test(
    ['begin',
        ['var', 'counter', 0], 
        ['var', 'result', 0], 

        ['while', ['<', 'counter', 10],
            # result++
            # todo: implemetn ['++' <Exp>] 
            ['begin',
                ['set', 'result', ['+', 'result', 1]],
                ['set', 'counter', ['+', 'counter', 1]],
            ],
        ],
        'result'
    ]
    ,10
)