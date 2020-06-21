"""
Copyright 2020 Dave Huh
"""

import math
import sys


class KaratsubaMultiplication:
    """
    Performs multiplication between two integers with
    Karatsuba's multiplication algorithm
    Uses fixed base of 10
    """

    def mult(self, intOne: int, intTwo: int):
        if intOne is None or intTwo is None or \
                not isinstance(intOne, int) or not isinstance(intTwo, int):
            print("invalid input")
            sys.exit(1)

        num_digits_int_one = len(str(abs(intOne)))
        num_digits_int_two = len(str(abs(intTwo)))
        
        if num_digits_int_one < 2 or num_digits_int_two < 2:
            return intOne*intTwo

        num_one_split_idx = math.floor(num_digits_int_one/2)
        num_two_split_idx = math.floor(num_digits_int_two/2)

        B = 10  # base
        m = 0  # initiate multiple

        '''if multiplication is too simple, just return naive multiplication'''
        if num_digits_int_one < m + 1 or num_digits_int_two < m + 1:
            return intOne*intTwo

        if num_digits_int_one > num_digits_int_two:
            m = num_one_split_idx + 1
            x_1 = int(str(intOne)[:m-1])
            x_0 = int(str(intOne)[m-1:num_digits_int_one])
            num_two_split_idx = num_digits_int_two - m - 1
            if num_two_split_idx == 0:
                y_1 = int(str(intTwo)[0])
            else:
                y_1 = int(str(intTwo)[:num_two_split_idx])
            y_0 = int(str(intTwo)[num_two_split_idx+1:num_digits_int_two])
        elif num_digits_int_two == num_digits_int_one:
            m = num_two_split_idx
            x_1 = int(str(intOne)[:m])
            x_0 = int(str(intOne)[m:num_digits_int_one])
            y_1 = int(str(intTwo)[:m])
            y_0 = int(str(intTwo)[m:num_digits_int_two])
            if num_digits_int_two % 2 != 0:  # need to shift bits if digits are odd
                m += 1
        else:
            m = num_two_split_idx + 1
            x_1 = int(str(intTwo)[:m-1])
            x_0 = int(str(intTwo)[m-1:num_digits_int_two])
            num_one_split_idx = num_digits_int_one - m - 1
            if num_one_split_idx == 0:
                y_1 = int(str(intOne)[0])
            else:
                y_1 = int(str(intOne)[:num_one_split_idx])
            y_0 = int(str(intOne)[num_one_split_idx+1:num_digits_int_one])

        z_2 = x_1*y_1
        z_0 = x_0*y_0
        z_1 = (x_1+x_0)*(y_1+y_0)-z_2-z_0
        star = z_2 * B**(2*m) + z_1*B**(m) + z_0

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
