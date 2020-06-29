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

        # do more divide and conquer
        if len(a) > 1:
            a = self.sort_by_dim(a, dim)
        if len(b) > 1:
            b = self.sort_by_dim(b, dim)

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

    def calculate_distance(self, vector1, vector2):
        """Calculates distance between two vectors"""
        dist = [(a - b)**2 for a, b in zip(vector1, vector2)]
        dist = math.sqrt(sum(dist))
        return dist

    def brute_force_closest_pair(self, Px, Py):
        """
        Uses brute force iterations to find closest pairs
        by scanning through list linearly
        Input:
            Px: A copy of P sorted by x
            Py: A copy of P sorted by y
        Output:
            closest_pair = [p, q]
        """
        # base cases
        best_dist = None
        p = q = None
        if len(Px) < 3:
            return Px
        elif len(Px) < 4:
            for idx in range(len(Px)-1):
                x_dist = self.calculate_distance(Px[idx], Px[idx + 1]) 
                y_dist = self.calculate_distance(Py[idx], Py[idx + 1]) 
                if best_dist is None or x_dist < best_dist:
                    best_dist = x_dist
                    p = Px[idx]
                    q = Px[idx+1]
                if y_dist < best_dist:
                    best_dist = y_dist
                    p = Py[idx]
                    q = Py[idx+1]

        return [p, q]

    def closest_pair(self, Px, Py):
        """
        Output closest pair given sorted copies of points by x and y
        Assumptions: x and y are sorted
        """
        if Px is None or Py is None:
            print("invalid input")
            sys.exit(1)

        # base cases
        if len(Px) < 3:
            return Px
        elif len(Px) < 4:
            return self.brute_force_closest_pair(Px, Py)

        Qx, Rx = self.split_plane(Px)
        Qy, Ry = self.split_plane(Py)

        # Base case
        p1 = q1 = p2 = q2 = None

        [p1, q1] = self.closest_pair(Qx, Qy)
        [p2, q2] = self.closest_pair(Rx, Ry)

        dist_p1q1 = self.calculate_distance(p1, q1)
        dist_p2q2 = self.calculate_distance(p1, q1)

        if dist_p1q1 <= dist_p2q2:
            best_dist = dist_p1q1
            min_p1q1_p2q2 = [p1, q1]
        else:
            best_dist = dist_p2q2
            min_p1q1_p2q2 = [p2, q2]

        return min_p1q1_p2q2

    def closest_split_pair(self, Px, Py, dist):
        """
        find the closest pair split between Q and R if the pairs lie
        within set range (-dist, dist)
        Input:
            Px: a copy of P sorted by x
            Py: a copy of P sorted by y
            dist: shortest distance calculated and compared between
                either Q or R
        Output:
            [p, q]: closest pair.
        """
        best_pair = None

        Qx, Rx = self.split_plane(Px)
        Qy, Ry = self.split_plane(Py)

        x_bar = Qx[-1][0]
        Sy_boundary = [x_bar - dist, x_bar + dist]

        Sy = []

        for point in Py:
            if point[0] >= Sy_boundary[0] and \
                    point[0] <= Sy_boundary[1]:
                Sy.append(point)

        if len(Sy) < 2:
            return None

        best_dist = dist
        for i in range(len(Sy)):
            for j in range(min(7, len(Sy)-i-1)):
                p = Sy[i]
                q = Sy[i+j+1]
                tmp_dist = self.calculate_distance(p, q)
                if tmp_dist < best_dist:
                    best_dist = tmp_dist
                    best_pair = [p, q]

        return best_pair

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

        Px = self.sort_by_dim(plane, 0)
        Py = self.sort_by_dim(plane, 1)

        best_pair = self.closest_pair(Px, Py)
        best_split_pair = self.closest_split_pair(Px, Py,
                                    self.calculate_distance(best_pair[0],
                                    best_pair[1])
                                                  )

        if best_split_pair is not None:
            best_pair = best_split_pair

        return best_pair


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 closest_pair")
        sys.exit(1)

    unsorted_plane_coordinates = str(sys.argv[1])
    closest_pair = ClosestPair(unsorted_plane_coordinates)
    best_pair = closest_pair.find_closest_pair(closest_pair.plane)
    print(best_pair)
