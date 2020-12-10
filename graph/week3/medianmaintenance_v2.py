"""
Copyright 2020 Dave Huh
Median maintenance using two heaps
"""

import sys
import threading
from heapq import heapify, heappop

def build_stream(file_name):
    """
    build stream
    :param file_name: path of input file
    return stream
    """
    stream = []

    with open(file_name, 'r') as f:
        for line in f:
            stream.append(int(line))

    return stream


def find_medians(stream, k):
    """
    find median
    """
    sliced = stream[:k]
    heapify(sliced)
    neg_sliced = [-x for x in sliced]
    heapify(neg_sliced)

    iterations = -1
    if k % 2 == 0:
        iterations = k/2
    else:
        iterations = (k+1)/2
    iterations = int(iterations)

    max_med = -1
    min_med = -1

    for i in range(iterations):
        max_med = heappop(neg_sliced)
        min_med = heappop(sliced)

    if k % 2 == 0:
        median = min_med
    else:
        median = -max_med

    return median


def find_median(num, minheap, maxheap):
    """
    Finds median
    :param num: streamed number
    :param minheap: min heap
    :param maxheap: max heap
    return median
    """

    return minheap[0]

def main():
    """
    main
    """
    stream = build_stream(sys.argv[1])

    minheap, maxheap = [], []

    answer = 0
    for k in range(1, len(stream) + 1):
        answer += find_medians(stream, k)

    answer = answer % 10000
    print("answer:", answer)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 medianmaintenance_v2.py <file name>")
        sys.exit(1)

    STACK_SIZE = 67108864
    RECURSION_LIMIT = 10**6

    threading.stack_size(STACK_SIZE)
    sys.setrecursionlimit(RECURSION_LIMIT)

    thread = threading.Thread(target=main)
    thread.start()
