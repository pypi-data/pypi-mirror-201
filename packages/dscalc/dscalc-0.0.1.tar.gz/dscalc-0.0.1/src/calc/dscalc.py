class DSCalc:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def process_func(self, func):
        '''
        This function calculates the resut based on the function argument
        Different types of func available in the Calc class are:
        'sum': sum of two values 
        'subtract': difference between two values 
        'multiply': product of two values 
        'divide': divisin of first value by the second one 
        '''
        if func == 'sum':
            return self.a + self.b
        elif func == 'subtract':
            return self.a - self.b
        elif func == 'multiply':
            return self.a * self.b
        elif func == 'divide':
            return self.a / self.b if b!=0 else 'Not divisible'