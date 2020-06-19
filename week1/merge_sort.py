'''
Copyright 2020 Dave Huh
'''

import sys
import math

class MergeSort:
    """Performs merge sort of given array"""

    def mergeSort(self, ul):
        # edge cases
        if ul is None or not isinstance(ul, list):
            print("invalid input")
            sys.exit(1)

        if len(ul) < 2:
            return ul

        ul = list(map(int, ul))

        split_index = math.floor(len(ul)/2)
        a = ul[:split_index]
        b = ul[split_index:len(ul)]
        output = [None]*len(ul)
        print(a, b)

        i = 0
        j = 0
        for idx in range(len(output)):
            if i >= len(a)-1 and j <= len(b)-1:
                output[idx:] = self.mergeSort(b)
                break
            if j >= len(b)-1 and i <= len(a)-1:
                output[idx:] = self.mergeSort(a)
                break
            
            #split
            if len(a) > 1:
                output[idx:]


            if a[i] < b[j]:
                output[idx] = a[i]
                i += 1
            elif a[i] == b[j]:
                output[idx] = a[i]
                output[idx+1] = b[j]
                i += 1
                j += 1
                idx += 1
            else:
                output[idx] = b[j]
                j += 1

        print(output)
        return output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 merge_sort.py <Array>")
        sys.exit(1)
    unsorted_array = str(sys.argv[1]).split(sep=',')
    sorted_list = MergeSort()
    sorted_list.mergeSort(unsorted_array)
