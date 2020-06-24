"""
Copyright 2020 Dave Huh
"""

import sys
import math


class CountInversions:
    """divide and conquer approach to count inversions
    """

    def countInversions(self, ul):
        """
        Assumptions: No ties
        """
        # edge cases
        if ul is None or not isinstance(ul, list):
            print("Invalid input")
            sys.exit(1)

        if len(ul) < 2:
            return 0

        ul = list(map(int, ul))

        # Split
        splitPoint = math.floor(len(ul)/2)
        left = ul[:splitPoint]
        right = ul[splitPoint:]
        output = [None]*len(ul)

        # Sort left and count inversions
        if len(left) > 1:
            left = self.countInversions(ul)
        if len(right) > 1:
            right = self.countInversions(ul)

        # Merge
        i = 0
        j = 0
        inversions = 0
        for idx in range(len(output)):
            if i > len(left) - 1 and j > len(right) - 1:
                break
            if i > len(left) - 1 or len(left) < 1:
                output[idx:] = left[i:]
                break
            if left[i] < right[j]:
                output[idx] = left[i]
                i += 1
            else:
                output[idx] = right[j]
                inversions += 1
                j += 1

        print(output, inversions)
        
        return inversions



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 count_inversions.py <Array>")
        sys.exit(1)

    unsorted_array = str(sys.argv[1]).split(sep=',')
    inversionCounts = CountInversions()
    inversionCounts.countInversions(unsorted_array)
