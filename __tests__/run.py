import sys
import os
import importlib

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from peva import Peva

class Run:
    peva = Peva()

    # this is a helper function used to simply the assert testing done in the other "..-test.py" files
    @staticmethod
    def test(expression, expected):
        result = Run.peva.eval(expression)
        assert result == expected, f"Test failed: {expression} -> {result} != {expected}"

if __name__ == '__main__':
    test_dir = os.path.dirname(__file__)
    test_files = [f[:-3] for f in os.listdir(test_dir) if f.endswith('-test.py')]

    Run.peva.eval(['print', '"hello, world"'])

    for test_file in test_files:
        print(f"Running {test_file}...")
        importlib.import_module(test_file)  # Import executes the test file automatically

    print("All assertions passed!!")
