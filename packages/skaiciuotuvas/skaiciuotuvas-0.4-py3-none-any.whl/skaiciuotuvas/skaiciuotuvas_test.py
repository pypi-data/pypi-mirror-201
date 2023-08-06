import os
from skaiciuotuvas import Calculator
import unittest
from hypothesis import given
from hypothesis.strategies import floats
import doctest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_addition(self):
        '''
            >>> x=0
            >>> x
            0
            
        '''
        self.assertEqual(self.calc.add(2), 2)
        self.assertEqual(self.calc.add(2.0), 4.0)
    
    def test_subtraction(self):
        self.calc.result = 3
        self.assertEqual(self.calc.substract(2), 1)
        self.assertEqual(self.calc.substract(2.0), -1.0)
    
    def test_multiplication(self):
        self.calc.result = -4.156
        self.assertEqual(self.calc.multiply(2), -8.312)
        self.assertEqual(self.calc.multiply(2.0), -16.624)
        
    def test_division(self):
        self.calc.result = 0.5
        with self.assertRaises(ValueError):
            self.calc.divide(0)
        
        self.assertEqual(self.calc.divide(2), 0.25)
        self.assertEqual(self.calc.divide(2.0), 0.125)
        
    def test_n_root(self):
        self.calc.result = 196546.586914
        self.assertEqual(self.calc.n_root(8), 4.5886315653701715)
        self.assertEqual(self.calc.n_root(9.789), 1.168408113648194)
    
    def test_mypy(self):
        # Run mypy type checking
        # `--ignore-missing-imports` flag is used to ignore import errors since we are not importing some modules in this file.
        self.assertEqual(os.system('mypy skaiciuotuvas.py'), 0)
    
    def test_pyflakes(self):
        # Run pyflakes to check for any syntax or name errors
        self.assertEqual(os.system('pyflakes skaiciuotuvas.py'), 0)
    
    @given(floats(min_value=-10000, max_value=10000), floats(min_value=-10000, max_value=10000))
    def test_addition_hypothesis(self, x, y):
        self.calc.reset()        
        self.assertEqual(self.calc.add(x), x)
        self.assertEqual(self.calc.add(y), x+y)
        
if __name__ == '__main__':
    print(os.system('doctest -v skaiciuotuvas.py'))
    unittest.main()
    
