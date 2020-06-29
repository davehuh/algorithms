"""
Copyright 2020 Dave Huh
"""

import sys
import math
import ast


class ClosestPair:
    """
    Identify closet pair points in a plane
    """

    def __init__(self, ul):
        """
        initialize unsorted plane
        """
        if ul is None:
            print("invalid input")
            sys.exit(1)

        self.plane = []
        try:
            self.plane = ast.literal_eval(ul)
        except:
            print("invalid input")
            sys.exit(1)

    def split_plane(self, plane):
        """
        Splits plane (list of 2D coordinates)
        Input: list of coordinates in 2D plane
        Output: Q: left half of array of coordinates
                R: right half of array of coordinates
        """
        split_point = math.floor(len(plane)/2)

        Q = plane[:split_point]
        R = plane[split_point:]

        return Q, R

    def sort_by_dim(self, ul, dim=1):
        """
        Sorts a list of coordinates by dimension.
        Outputs a sorted copy
        """
        if not isinstance(dim, int):
            return ul

        X = [None]*len(ul)

        # primitive case
        if len(ul) < 2:
            return ul, ul

        split_index = math.floor(len(ul)/2)
        a = ul[:split_index]
        b = ul[split_index:]
#        print('a: ', a, '  b: ', b)

        # do more divide and conquer
        if len(a) > 1:
            a = self.sort_by_dim(a, dim)
        if len(b) > 1:
            b = self.sort_by_dim(b, dim)

#        print('ul: ', ul)

        # merge to generate X
        a_i = 0
        b_i = 0
        for idx in range(len(X)):
            # primitive cases
            if a_i > len(a) - 1 and b_i > len(b) - 1:
                break
            if a_i > len(a) - 1 or len(a) < 1:
                X[idx:] = b[b_i:]
                break
            if b_i > len(b) - 1 or len(b) < 1:
                X[idx:] = a[a_i:]
                break
           
            # value comparisons
#            print(a[a_i][0], b[b_i][0])
            if a[a_i][dim] < b[b_i][dim]:
                X[idx] = a[a_i]
                a_i += 1
            elif a[a_i][dim] == b[b_i][dim]:
                X[idx] = a[a_i]
                X[idx+1] = a[a_i]
                a_i += 1
                b_i += 1
                idx += 1
            else:
                X[idx] = b[b_i]
                b_i += 1

        return X


    def find_closest_pair(self, plane):
        """
        A wrapper function to find closest pair coordinates in a 2D plane
        Assumptions: no ties in x-coordinates and y-coordinates
        Input: unsorted list of coordinates
        Output: cloest pair coordinates
        """
        # edge cases
        if plane is None:
            print("invalid input")
            sys.exit(1)

        # primitive cases
        if len(plane) < 3:
            return plane

        Q, R = self.split_plane(plane)
        # TODO delete
        Qx = self.sort_by_dim(Q, 0)
        Qy = self.sort_by_dim(Q, 1)
        Rx = self.sort_by_dim(R, 0)
        Ry = self.sort_by_dim(R, 1)

        print('Q: ', Qx, Qy)
        print('R: ', Rx, Ry)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 closest_pair")
        sys.exit(1)

    unsorted_plane_coordinates = str(sys.argv[1])
    closest_pair = ClosestPair(unsorted_plane_coordinates)
    best_pair = closest_pair.find_closest_pair(closest_pair.plane)
