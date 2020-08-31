"""
Copyright 2020 Dave Huh
Computes medians in incoming stream of integers
"""

import sys
import heapq


class MedianMaintenance:
    def __init__(self):
        self.lowMaxHeap = []  # max heap of low numbers
        self.highMinHeap = []  # min heap of high numbers

    def computeMedians(self, nums):
        """
        For every line of input, compute medians and output to a list
        """
        if not nums:
            print("invalid input")
            sys.exit(1)

        output = []

        for num in nums:
            # initialize
            if not self.lowMaxHeap:
                heapq.heappush(self.lowMaxHeap, -num)

            elif num > -self.lowMaxHeap[0]:
                heapq.heappush(self.highMinHeap, num)
            elif num < -self.lowMaxHeap[0]:
                heapq.heappush(self.lowMaxHeap, -num)

            # special case that requires swaps between heaps
            elif -self.lowMaxHeap[0] > num:
                tmp = -heapq.heappop(self.lowMaxHeap)
                heapq.heappush(self.lowMaxHeap, -num)
                heapq.heappush(self.highMinHeap, tmp)

            # length check
            if len(self.lowMaxHeap) > len(self.highMinHeap) + 1:
                tmp = -heapq.heappop(self.lowMaxHeap)
                heapq.heappush(self.highMinHeap, tmp)
            elif len(self.lowMaxHeap) + 1 < len(self.highMinHeap):
                tmp = heapq.heappop(self.highMinHeap)
                heapq.heappush(self.lowMaxHeap, -tmp)

            # append median to output
            if len(self.lowMaxHeap) == len(self.highMinHeap) or \
                    len(self.lowMaxHeap) > len(self.highMinHeap):
                output.append(-self.lowMaxHeap[0])
            else:
                output.append(self.highMinHeap[0])

#            or \
#                    len(self.lowMaxHeap) <= len(self.highMinHeap):
#            elif not self.highMinHeap:
#                heapq.heappush(self.highMinHeap, num)

        return output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 medianmaintenance.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    nums = list(map(int, textFile.read().splitlines()))
    medians = MedianMaintenance()
    medians = medians.computeMedians(nums)
    answer = sum(medians) % 10000
    print(answer)
