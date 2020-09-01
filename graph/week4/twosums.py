"""
Copyright 2020 Dave Huh
Computes two-sum algorithm
"""

import sys
from concurrent import futures


class TwoSums:
    def __init__(self, nums):
        if not nums:
            print("invalid input")
            sys.exit(1)

        self.hash = {}
        for num in nums:
            if num in self.hash:
                self.hash[num] += 1
            else:
                self.hash[num] = 1

    def countTOccurrences(self, interval):
        if not interval or len(interval) != 2:
            print("invalid input")
            sys.exit(1)

        output = 0
        visited = {}
        interval = range(interval[0], interval[1] + 1)
#        with futures.ProcessPoolExecutor() as pool:
#        for num in pool.map(self.hash):
        for num in self.hash:
            visited[num] = True
            intervalCopy = []
            for t in interval:
                key = t - num
                if key in visited:
                    continue
                if key in self.hash:
                    output += 1
                    continue
                intervalCopy.append(t)
            interval = intervalCopy

        return output

    def counter(self, interval):

        raise NotImplementedError


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 twosums.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    nums = list(map(int, textFile.read().splitlines()))

    twoSums = TwoSums(nums)
    # tInterval = [3, 10]  # 8
    # tInterval = [0, 4]  # 2
    # tInterval = [3, 4]  # 2

    tInterval = [-10000, 10000]

    count = twoSums.countTOccurrences(tInterval)
    print("answer: ", count)
