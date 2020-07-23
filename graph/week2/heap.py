"""
Copyright 2020 Dave Huh
"""
import math


class heap:
    """
    implements min heap
    """
    def __init__(self, val):
        """
        Initializes heap
        """
        # tree
        self.tree = []
        if val is not None:
            self.tree.append(val)
            self.lastIdx = 0  # used to track last item entered

    def peak(self):
        """
        Returns root value
        """
        return self.tree[0]

    def insert(self, val):
        """
        inserts value to the last place in the heap
        """
        self.tree.append(val)
        self.lastIdx = len(self.tree) - 1
        self.bubbleUp()

    def remove(self):
        """
        Removes root node
        """
        lastElement = self.tree.pop()
        self.tree[0] = lastElement
        self.bubbleDown()

    def bubbleUp(self):
        """
        maintains heap. i.e. bubble up
        parent node is floor of (1 - index)/2
        """

        # Check last element with parent
        parentIdx = math.floor((self.lastIdx - 1) / 2)
        parent = self.tree[parentIdx]

        if self.lastIdx > 0 and self.tree[self.lastIdx] < parent:
            tmp = parent
            self.tree[parentIdx] = self.tree[self.lastIdx]
            self.tree[self.lastIdx] = tmp
            self.lastIdx = parentIdx
        else:
            return

        self.bubbleUp()

    def bubbleDown(self):
        """
        maintains heap. i.e. bubble down
        left child index is parent index * 2 + 1
        right child index is parent index * 2 + 2
        """
        if self.lastIdx == len(self.tree) - 1:
            return

        maxIdx = len(self.tree) - 1
        leftChildIdx = self.lastIdx * 2 + 1
        rightChildIdx = self.lastIdx * 2 + 2

        # find smaller of the two children
        if leftChildIdx > maxIdx:
            return

        if leftChildIdx <= maxIdx < rightChildIdx:
            # right child doesn't exist
            smallerChildIdx = leftChildIdx

        if self.tree[leftChildIdx] <= self.tree[rightChildIdx]:
            smallerChildIdx = leftChildIdx
        else:
            smallerChildIdx = rightChildIdx

        if self.tree[smallerChildIdx] < self.tree[self.lastIdx]:
            parent = self.tree[self.lastIdx]
            tmp = parent
            self.tree[self.lastIdx] = self.tree[smallerChildIdx]
            self.tree[smallerChildIdx] = tmp
            self.lastIdx = smallerChildIdx
        else:
            return

        self.bubbleDown()

    def __str__(self):
        return str(self.tree)


if __name__ == "__main__":
    heap = heap(10)
    heap.insert(4)
    heap.insert(15)

    heap.remove()

    heap.insert(20)
    heap.insert(0)
    heap.insert(30)

    heap.remove()
    heap.remove()

    heap.insert(2)
    heap.insert(4)
    heap.insert(-1)
    heap.insert(-3)

    print(heap)

