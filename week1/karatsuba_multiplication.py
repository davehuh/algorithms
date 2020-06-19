"""
CopintTworight 2020 Dave Huh
"""

import math
import sys


class KaratsubaMultiplication:
    """
    Performs multiplication between two integers with
    Karatsuba's multiplication algorithm
    Limitations, multiplying odd numbered digit integers will yield 
    incorrect output
    """

    def mult(self, intOne: int, intTwo: int):
        if intOne is None or intTwo is None or \
                not isinstance(intOne, int) or not isinstance(intTwo, int):
            print("invalid input")
            sys.exit(1)

        num_digits_int_one = len(str(abs(intOne)))
        num_digits_int_two = len(str(abs(intTwo)))
        
        if num_digits_int_one < 2 or num_digits_int_two < 2:
            star = intOne*intTwo
            print(star)
            return star 

        num_one_split_idx = math.ceil(num_digits_int_one/2)
        num_two_split_idx = math.ceil(num_digits_int_two/2)

        a = int(str(intOne)[:num_one_split_idx])
        b = int(str(intOne)[num_one_split_idx:num_digits_int_one])
        c = int(str(intTwo)[:num_two_split_idx])
        d = int(str(intTwo)[num_two_split_idx:num_digits_int_two])
#        x = int(10**(num_digits_int_one/2)*a+b)
#        y = int(10**(num_digits_int_two/2)*c+d)
#       x*y        
        star = 10**math.ceil((num_digits_int_one + num_digits_int_two)/2) * \
            self.mult(a, c) + \
            (10**(math.ceil(num_digits_int_one/2)) * (self.mult(a, d)) +
             10**(math.ceil(num_digits_int_two/2)) * self.mult(b, c)) + self.mult(b, d)

        print(a, b, c, d)
        print(star)
        return star


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 karatsuba_multiplication.py <X> <Y>")
        sys.exit(1)
    intOne = int(sys.argv[1])
    intTwo = int(sys.argv[2])
    output = KaratsubaMultiplication()
    output.mult(intOne, intTwo)
