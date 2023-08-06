from typing import Union
from operator import add, sub, mul, truediv
import math

class Calculator:
    def __init__(self):
        self.result = 0
        '''
            creating variable result variable during creation of class instance        
        '''
    def add(self, input_value: Union[int, float]) -> Union[int,float]:
        '''
            Adition: this function is adding existing result and input_value
            -----
            >>> x = calculator.add(8)
            >>> x
            8
        '''
        if not math.isfinite(self.result):
            raise ValueError("Result is not a finite number")
        self.result = add(self.result, input_value)
        return self.result
    
    def substract(self, input_value: Union[int, float]) -> Union[int,float]:
        '''            
            Substraction: this function is substracting input value from existing result
            -----
            >>> calculator.result = 7
            >>> x = calculator.substract(4)
            >>> x
            3
'''
        if not math.isfinite(self.result):
            raise ValueError("Result is not a finite number")
        self.result = sub(self.result, input_value)
        return self.result

    def multiply(self, input_value: Union[int,float]) -> Union[int,float]:
        '''            
            Multiplication: this function is multiplying existing result and input_value
            -----
            >>> calculator.result = 4
            >>> x = calculator.multiply(2)
            >>> x
            8
        '''
        if not math.isfinite(self.result):
            raise ValueError("Result is not a finite number")
        self.result = mul(self.result, input_value)
        return self.result
    
    def divide(self, input_value: Union[int, float]) -> Union[int,float]:
        '''            
            Division: this function is dividing existing result by input_value
            -----
            >>> calculator.result = 79
            >>> calculator.divide(8)
            9.875
        '''
        if input_value == 0:
            raise ValueError ('division from 0 is infinity')
        if not math.isfinite(self.result):
            raise ValueError("Result is not a finite number")
        self.result = truediv(self.result, input_value)
        return self.result

    def n_root(self, input_value: Union[int, float]) -> int:
        '''            
            Rooting: this function is calculate input_value root for existing result
            -----
            >>> calculator.result = 256
            >>> calculator.n_root(8)
            2.0
            
        '''
        if not math.isfinite(self.result):
            raise ValueError("Result is not a finite number")
        self.result **= (1/input_value)
        return self.result

    def reset(self):
        '''            
            Reseting: this function resets result value
        '''
        self.result = 0
