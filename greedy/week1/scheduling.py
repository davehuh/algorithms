"""
Copyright 2020 Dave Huh
Use greedy algorithm to minimize cost of scheduling jobs
"""

import sys
from functools import reduce
import operator
import pandas as pd
import numpy as np


class Schedule:
    def __init__(self, numJobs, jobs):
        """
        Input:
            jobs is a list of two columns where first column represent weight
            and second column represent length
            numJobs: number of jobs total
        """
        self.numJobs = numJobs
        self.jobs = pd.DataFrame(jobs)
        self.jobs = self.jobs.rename(columns={0: "weight", 1: "length"})

    def computeScheduling(self, priorities):
        """
        Compute cost of scheduling
        """
        indexes = priorities.keys()
        cost = 0
        cumulativeLength = 0

        for i in indexes:
            job = self.jobs[i]
            weight = job[0]
            length = job[1]
            cumulativeLength += length
            cost += weight * cumulativeLength

        return cost

    def computeMinCostByDifference(self):
        """
        Computes minimal cost by sorting priorities determined by taking
        differences between weight and length

        Output:
            computedCost : minimal computed cost of scheduling
        """
        priorities = self.jobs
        priorities["cost"] = priorities["weight"] - priorities["length"]
        priorities = priorities.sort_values(by=['cost', 'weight'],
                                            ascending=False)
        priorities["cumsum_length"] = priorities["length"].cumsum()
        priorities["computedCost"] = priorities["weight"] * \
            priorities["cumsum_length"]

        computedCost = priorities["computedCost"].sum()
        return computedCost

    def computeMinCostByRatio(self):
        """
        Computes priority of jobs by comparing the ratio
        between weight and length

        Input:
            jobs: list of jobs with weight and length

        """
        priorities = self.jobs
        priorities["cost"] = priorities["weight"] / priorities["length"]
        priorities = priorities.sort_values(by='cost',
                                            ascending=False)
        priorities["cumsum_length"] = priorities["length"].cumsum()
        priorities["computedCost"] = priorities["weight"] * \
            priorities["cumsum_length"]

        computedCost = priorities["computedCost"].sum()
        return computedCost


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scheduling.py <file name>")
        sys.exit(1)

    textFile = open(sys.argv[1])
    textFile = textFile.read().splitlines()
    numberJobs = textFile.pop(0)
    allJobs = [list(map(int, ele.split(" "))) for ele in textFile]

    schedule = Schedule(numberJobs, allJobs)
    suboptimalMinCost = schedule.computeMinCostByDifference()
    optimalMinCost = schedule.computeMinCostByRatio()
    print(suboptimalMinCost)
    print(optimalMinCost)
