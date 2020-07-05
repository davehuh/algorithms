"""
Copyright 2020 Dave Huh
"""

import sys
import math


class QuickSort:
    """
    QuickSort a list of numbers
    """

    def quicksort(self, ul):
        """
        A wrapper function for QuickSort using three pivot choices :
        First, Last and optimal random
        """
        # edge cases
        if ul is None or not isinstance(ul, list):
            print("invalid input")
            sys.exit(1)

        if len(ul) < 2:
            return ul

        ul = list(map(int, ul))

        first_pivot, comp_count_first = \
            self.quicksort_choose_first_as_pivot(ul.copy())

        last_pivot, comp_count_last = \
            self.quicksort_choose_last_as_pivot(ul.copy())

        # TODO
#        print("final first pivot: ", first_pivot)
        print("first as pivot, counts: ", comp_count_first)

        print("final last pivot: ", last_pivot)
        print("last as pivot, counts: ", comp_count_last)

        return last_pivot

    def calculate_index(self, ul, first_or_last: str):
        """
        Calculates proper index
        Input:
            ul: unsorted list
            first_or_last: determine whether first or last element
                            is used as pivot must be "first" or "last"
        Output:
            index
        """
        if not isinstance(first_or_last, str) and first_or_last != "first" \
                and first_or_last != "last":
            print("invalid parameter")
            sys.exit(1)
        elif first_or_last == "first":
            return 0
        else:
            return len(ul) - 1

    def quicksort_choose_first_as_pivot(self, ul):
        """
        Sort using first element in list as the pivot
        Input:
            ul: unsorted list
        Output:
            sorted list, ul
            comp_count is the number of comparisons
                that the algorithm performed
        """

        if len(ul) < 2:
            return ul, 0

        pivot_idx = 0
        pivot = ul[pivot_idx]
        START_IDX = 1
        idx_include_greater_than_pivot = START_IDX

        # TODO
#        print("before sorting: ", ul)

        for idx in range(START_IDX, len(ul)):
            if ul[idx] < pivot and idx != idx_include_greater_than_pivot:
                tmp = ul[idx_include_greater_than_pivot]
                ul[idx_include_greater_than_pivot] = ul[idx]
                ul[idx] = tmp
                idx_include_greater_than_pivot += 1
            elif ul[idx] < pivot:
                idx_include_greater_than_pivot += 1

        # TODO
#        print("after sorting: ", ul)

        new_pivot_idx = idx_include_greater_than_pivot - 1
        tmp = ul[new_pivot_idx]
        ul[new_pivot_idx] = pivot
        ul[pivot_idx] = tmp

        # TODO
#        print("after swapping pivot:", ul)

        comp_count = len(ul) - 1

        # Remaining partitions need sorting
        # Check left
        if new_pivot_idx > 1:
            ul[:new_pivot_idx], tmp_count_left = \
                self.quicksort_choose_first_as_pivot(ul[:new_pivot_idx])
            comp_count += tmp_count_left

        # Check right
        if new_pivot_idx < len(ul) - 1:
            ul[new_pivot_idx+1:], tmp_count_right = \
                self.quicksort_choose_first_as_pivot(ul[new_pivot_idx+1:])
            comp_count += tmp_count_right

        return ul, comp_count

    def quicksort_choose_last_as_pivot(self, ul):
        """
        Sort using last element in list as the pivot
        Input:
            ul: unsorted list
        Output:
            sorted list, ul
            comp_count is the number of comparisons
                that the algorithm performed
        """

        if len(ul) < 2:
            return ul, 0

        pivot_idx = len(ul) - 1
        pivot = ul[pivot_idx]
        START_IDX = 0
        END_IDX = len(ul) - 1
        idx_include_greater_than_pivot = START_IDX

        # TODO
        print("before sorting: ", ul)

        for idx in range(START_IDX, END_IDX):
            if ul[idx] < pivot and idx != idx_include_greater_than_pivot:
                tmp = ul[idx_include_greater_than_pivot]
                ul[idx_include_greater_than_pivot] = ul[idx]
                ul[idx] = tmp
                idx_include_greater_than_pivot += 1
            elif ul[idx] < pivot:
                idx_include_greater_than_pivot += 1

        # TODO
        print("after sorting: ", ul)

        new_pivot_idx = idx_include_greater_than_pivot
        tmp = ul[new_pivot_idx]
        ul[new_pivot_idx] = pivot
        ul[pivot_idx] = tmp

        # TODO
        print("after swapping pivot:", ul)

        comp_count = len(ul) - 1

        # Remaining partitions need sorting
        # Check left
        if new_pivot_idx > 1:
            ul[:new_pivot_idx], tmp_count_left = \
                self.quicksort_choose_last_as_pivot(ul[:new_pivot_idx])
            comp_count += tmp_count_left

        # Check right
        if new_pivot_idx < len(ul) - 1:
            ul[new_pivot_idx+1:], tmp_count_right = \
                self.quicksort_choose_last_as_pivot(ul[new_pivot_idx+1:])
            comp_count += tmp_count_right

        return ul, comp_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 quicksort.py <file name>")
        sys.exit(1)

    txtFile = open(sys.argv[1])
    content_list = txtFile.read().splitlines()
    sorted_list = QuickSort()
    sorted_list = sorted_list.quicksort(content_list)
