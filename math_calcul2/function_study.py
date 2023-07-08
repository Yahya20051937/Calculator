from math_calcul2.organizing_function import organize_calcul_list
from math_calcul2.helping_function2 import get_divisor
from functions.Df_function2 import check_first_second_degree
from functions.my_functions import set_function


class Function:
    def __init__(self, expression):
        self.expression = organize_calcul_list(expression, variable=True)
        print(self.expression)

    @property
    def get_df(self):
        Df = sorted(set(range(-100, 100)))
        divisors = get_divisor(self.expression)    # now we have to solve the equation (divisor = 0) and get the value of x to delete it from df
        for divisor in divisors:
            condition1, condition2, a = check_first_second_degree(set_function(divisor))   # if condition one is true then this expression represents a first degree equation, if the condition2 is also true, then the function represents a second degree equation
            if condition1:
                if condition2:
                    pass
                else:
                    pass
        return Df

    def get_image(self, x):
        return self

    def draw_cf(self):
        
        pass
