"""
    Peva:
    A dynamic interpreted programming language with simple s-expressive syntax (lisp inspired), with OOP support.
    Inspired by 'Eva' - the same language, only difference is the underlying language is javascript, taught by Dmitry Soshnikov.
    Dmitry Soshnikov works: http://dmitrysoshnikov.com/
"""

"""
    #####################################################
    Expression Format:
    (+ 5 10)            # addition
    (set x 15)          # assignment
    (if (> x 10)        # if
        (print "ok")
        (print "err")    
    )
"""
"""
    #####################################################
    Function decleration:
    (def foo (bar)
            (+ bar 10))
"""            
"""
    #####################################################
    Lambda expression:
    (lambda (x) (* x x) 10)
"""

import re
from Enviroment import Environment 
from transform import Transformer

"""
Peva Interpreter.
"""
class Peva:
    """
    Creates an Eva instance with the global environment.
    """
    def __init__(self, enviroment = None, _transformer = Transformer):
        if enviroment is None:
            enviroment = GlobalEnvironment
        self.enviroment = enviroment
        self._transformer = _transformer
    
    """
    Evaluates an expression in the given environment.
    """ 
    def eval(self, exp, env = None):
        # By checking if env is None before setting env = self.enviroment, 
        # it ensures that when a local environment is provided (like one created for a begin block) 
        # it is respected during evaluation.
        if env is None:
            env = self.enviroment

        # self evaluating expression
        if self._isNumber(exp):
            return exp
        
        if self._isString(exp):
            return exp
        
        # Variable Declerations: (var foo 10)
        if (exp[0] == 'var'):  
            [_, name, value] = exp
            # recursivley evalte the expression value decleration
            return env.define(name, self.eval(value, env))
        
        #################################################
        # Variable Update: (set foo 10)
        if (exp[0] == 'set'):  
            [_, name, value] = exp
            # recursivley evalte the expression value decleration
            return env.assign(name, self.eval(value, env))
        
        #################################################
        # Variable Access: (foo)
        if (self._isVariableName(exp)):
            return env.lookup(exp)
        
        #################################################
        # if-expression:
        if(exp[0] == 'if'):
            [_tag, condition, consequent, alternate] = exp

            if(self.eval(condition, env)):
                return self.eval(consequent, env)
            
            return self.eval(alternate, env)
        
        #################################################
        # while-expression:
        if(exp[0] == 'while'):
            [_tag, condition, body] = exp
            result = None
            while(self.eval(condition, env)):
                result = self.eval(body, env)
            return result

        #################################################
        # Block: sequence of expressions
        if(exp[0] == 'begin'):
            blockEnv = Environment({}, env)
            return self._evalBlock(exp, blockEnv)
        
        #################################################
        # Function decleration: (def square (x) (* x x))
        #
        # syntactic sugar for: (var square (lambda (x) (* x x)))
        if(exp[0] == 'def'):
            [_tag, name, params, body] = exp
            
            # JIT-Transpile to a variable decleration
            # we create a variable expression node, just on time here
            varExp = self._transformer.Transformer.transformDefToLambda(exp)
            return self.eval(varExp, env)
        
        #################################################
        # Switch-expressions: (switch (cond1, block1) .. )
        #
        # syntactic sugar for: nested if-expressions
        if (exp[0] == 'switch'):
            ifExp = self._transformer.Transformer.transformSwitchToIf(exp)
            return self.eval(ifExp, env)
        
        #################################################
        # for-loop: (for init condition modifier body)
        #
        # syntactic sugar for: (begin init (while conidition (begin body modifier)))
        if (exp[0] == 'for'):
            whileExp = self._transformer.Transformer.transformForToWhile(exp)
            return self.eval(whileExp, env)
        
        #################################################
        # Lambda Function: (lambda) (x) (* x x))
        if(exp[0] == 'lambda'):
            [_tag, params, body] = exp

            return {
                'params': params,
                'body': body,
                'env': env # closure!
            }

        #################################################
        # Function Calls:
        #
        # (print "Hello World")
        # (+ x 5)
        # (> foo bar)
        if (isinstance(exp, list)): # check if exp is a list (expects an operation or function call)
            fn = self.eval(exp[0], env) # get the func name
            args = [self.eval(arg, env) for arg in exp[1:]]  # recursivley evalte each argument from the list. [1:] to sip operator
        
            # 1. Native Functions:
            if callable(fn):  # check if fn is callable (i.e., a function)
                return fn(*args) # return the result of calling the function with arguments
            
            # 2. User-Defined functions:
            activationRecord = {}  
            
            # retrieves from fn dict ({'param': param}) - declared in function decleration 'def'
            for index, param in enumerate(fn['params']):
                activationRecord[param] = args[index]

            activationEnv = Environment(
                activationRecord,
                fn['env'] # static-scope
            )

            return self._evalBody(fn['body'], activationEnv)
            
    def _isNumber(self, exp):
        return isinstance(exp, (int, float))

    def _isString(self, exp):
        # return an exp is a string starts and ends with double quotes
        return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'
    
    def _isVariableName(self, exp):
        # Regex for valid variable names (start with letter or underscore)
        return isinstance(exp, str) and bool(re.match(r'^[+\-*/><=a-zA-Z_][+\-*/><=a-zA-Z0-9_]*$', exp))
    
    def _evalBlock(self, block, env):
        result = None
        # Unpack the first element as _tag, and the evaluate the last expression in the block
        [_tag, *expressions] = block 

        # track the result variable which will be updated on each evaulation of each sub-expression
        for exp in expressions:
            result = self.eval(exp, env)
        return result
    
    def _evalBody(self, body, env):
        if(body[0] == 'begin'):
            return self._evalBlock(body, env)
        return self.eval(body, env)
    
"""
Default Global Enviorment
"""
GlobalEnvironment = Environment({
    'null': None,
    'true': True,
    'false': False,
    'VERSION': '0.1',

    # Math operations
    '+': lambda op1, op2: op1 + op2,
    '-': lambda op1, op2=None: -op1 if op2 is None else op1 - op2,
    '*': lambda op1, op2: op1 * op2,
    '/': lambda op1, op2: op1 / op2,

    # Comparison operations
    '>': lambda op1, op2: op1 > op2,
    '<': lambda op1, op2: op1 < op2,
    '<=': lambda op1, op2: op1 <= op2,
    '>=': lambda op1, op2: op1 >= op2,
    '=': lambda op1, op2: op1 == op2,  
    
    # Print operation
    'print': lambda *args: print(*args)
})
