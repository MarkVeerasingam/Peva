class Transformer:
    """
    Translates 'def'-expression (function decleration) into 
    a variable decleration with a lambda expression.
    """
    def transformDefToLambda(defExp):
        """
        Transforms a 'def' (function declaration) into a variable declaration with a lambda expression.
        For example:
          (def foo (x) (+ x 10))
        becomes:
          (var foo (lambda (x) (+ x 10)))
        """
        [_tag, name, params, body] = defExp
        return ['var', name, ['lambda', params, body]]
    
    """
    transforms 'switch' to nested 'if'--expression
    """
    def transformSwitchToIf(switchExp):
        """
        Transforms a 'switch' expression into nested 'if' expressions.
        
        Suppose the switch expression is of the form:
            ['switch',
                [cond1, block1],
                [cond2, block2],
                [else, block_else]
            ]
        The transformed nested if expression would look like:
            ['if', cond1, block1,
                ['if', cond2, block2, block_else]]
        
        This implementation processes the cases in reverse order.
        """
        [_tag, *cases] = switchExp

        # Start with the default value if one exists.
        nested_if = None
        for cond, block in reversed(cases):
            if cond == 'else':
                nested_if = block
            else:
                # Build a new if-expression where the "else" branch is the nested_if built so far.
                nested_if = ['if', cond, block, nested_if]
        return nested_if
    

    def transformForToWhile(forExp):
        """
        Transforms a for-loop expression into a while-loop expression.
        
        A for-loop is expected to have the following form:
            (for init condition modifier body)
            
        We transform it into a begin expression that first performs the init,
        and then enters a while-loop where the condition is tested, and inside the
        loop a begin expression executes the body and the modifier.
        
        The transformed expression looks like:
            (begin
                init
                (while condition
                    (begin
                        body
                        modifier)))
        """
        # ['for', init, condition, modifier, body]
        [_tag, init, condition, modifier, body] = forExp
        return['begin', init, ['while', condition, ['begin', body, modifier]]]
