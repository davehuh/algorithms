"""
Copyright 2020 Dave Huh
Third iteration of median maintenance
"""

import sys
import threading

from heapq import heappop, heappush

def read_file(file_name):
    """
    read file
    :param file_name: path to input file
    return numbers: a list of integers
    """
    numbers = []

    with open(file_name, 'r') as file:
        for num in file:
            num = int(num.strip())
            numbers.append(num)

    return numbers

def find_median(num, min_heap, max_heap):
    """
    find median
    :param num: new streaming number
    :param min_heap: min heap
    :param max_heap: max heap
    return median
    """
    median = -1

    heappush(min_heap, num)
    heappush(max_heap, -num)

    is_even = False
    if len(min_heap) % 2 == 0:
        k = len(min_heap) / 2
        is_even = True
    else:
        k = (len(min_heap) + 1) / 2

    min_meds = []
    max_meds = []
    while k > 1:
        min_med = heappop(min_heap)
        max_med = -heappop(max_heap)

        min_meds.append(min_med)
        max_meds.append(-max_med)

        k -= 1

    if is_even:
        median = min_heap[0]
    else:
        median = -max_heap[0]

    for idx, ele in enumerate(min_meds):
        heappush(min_heap, ele)
        heappush(max_heap, max_meds[idx])

    return median

def main():
    """
    main
    """
    numbers = read_file(sys.argv[1])

    min_heap, max_heap = [], []

    medians = 0

    for num in numbers:
        medians += find_median(num, min_heap, max_heap)

    print("answer:", medians % 10000)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 medianmaintenance_v3.py <file name>")
        sys.exit(1)

    STACK_SIZE = 67108864
    RECURSION_LIMIT = 10**6

    threading.stack_size(STACK_SIZE)
    sys.setrecursionlimit(RECURSION_LIMIT)

    thread = threading.Thread(target=main)
    thread.start()
