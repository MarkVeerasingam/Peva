import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.pevaParser import parse
from peva import Peva
from peva import Environment

def test(peva, code, expected):
    """
    Parses the code (wrapped in a (begin ...)) and asserts that evaluating it
    with the given peva interpreter instance produces the expected result.
    """
    # Wrap the provided code in a (begin ...) expression
    expression = parse("(begin " + code + ")")
    result = peva.eval(expression)
    assert result == expected, f"Test failed: {code} -> {result} != {expected}"