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

        median_pivot, comp_count_median = \
            self.quicksort_choose_median_as_pivot(ul.copy())

        # TODO
#        print("final first pivot: ", first_pivot)
        print("first as pivot, counts: ", comp_count_first)

#        print("final last pivot: ", last_pivot)
        print("last as pivot, counts: ", comp_count_last)

#        print("final median pivot: ", median_pivot)
        print("median as pivot, counts: ", comp_count_median)

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
            which_as_pivot: Which element as pivot: "first" "last" ""
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

        START_IDX = 1
        idx_include_greater_than_pivot = START_IDX

        # TODO
#        print("before sorting: ", ul)

        # Swap pivot to first element to ensure same comparison counts
        tmp = ul[0]
        ul[0] = pivot
        ul[pivot_idx] = tmp
        pivot_idx = 0

        # TODO
#        print("swapped pivot: ", ul)

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
                self.quicksort_choose_last_as_pivot(ul[:new_pivot_idx])
            comp_count += tmp_count_left

        # Check right
        if new_pivot_idx < len(ul) - 1:
            ul[new_pivot_idx+1:], tmp_count_right = \
                self.quicksort_choose_last_as_pivot(ul[new_pivot_idx+1:])
            comp_count += tmp_count_right

        return ul, comp_count

    def quicksort_choose_median_as_pivot(self, ul):
        """
        Sort by using median element in list as the pivot
        Uses first, last, and median to figure out approx median
        Input:
            ul: unsorted list
        Output:
            sorted list, ul
            comp_count is the number of comparisons
                that the algorithm performed
        """

        if len(ul) < 2:
            return ul, 0

        median = [None] * 3
        median[0] = ul[0]
        median[2] = ul[len(ul)-1]

        if len(ul) % 2 != 0:
            middle_idx = math.ceil(len(ul)/2) - 1
        else:
            middle_idx = len(ul)/2 - 1

        middle_idx = int(middle_idx)

        median[1] = ul[middle_idx]

        for idx in range(len(median)):
            if idx == 0:
                minimum = median[idx]
                maximum = median[idx]
                continue
            if median[idx] < minimum:
                minimum = median[idx]
            if median[idx] > maximum:
                maximum = median[idx]

        # Evaluate which is median
        median_idx = 0
        if minimum != maximum:
            for idx in range(len(median)):
                if median[idx] > minimum and median[idx] < maximum:
                    median_idx = idx
                    break

        if median_idx == 1:
            median_idx = middle_idx
        elif median_idx == 2:
            median_idx = len(ul) - 1

        pivot_idx = median_idx
        pivot = ul[pivot_idx]

        START_IDX = 1
        idx_include_greater_than_pivot = START_IDX

        # TODO
#        print("before sorting: ", ul)

        # TODO
#        print("pivot list: ", median)
#        print("pivot: ", pivot)

        # Swap pivot to first element to ensure same comparison counts
        tmp = ul[0]
        ul[0] = pivot
        ul[pivot_idx] = tmp
        pivot_idx = 0

        # TODO
#        print("swapped pivot: ", ul)

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
                self.quicksort_choose_median_as_pivot(ul[:new_pivot_idx])
            comp_count += tmp_count_left

        # Check right
        if new_pivot_idx < len(ul) - 1:
            ul[new_pivot_idx+1:], tmp_count_right = \
                self.quicksort_choose_median_as_pivot(ul[new_pivot_idx+1:])
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
