import heapq as hq

from Q1.classes.median_maintenance import MedianMaintenance


class HeapMedianMaintenance(MedianMaintenance):
    """
    HeapMedianMaintenance is a class that implements the heap median heap algorithm.
    This class contains two lists, which are actually mein heaps, lower_half and upper_half.
    But we use a simple trick and convert the lower half to max heap by just storing the negative of
    that item in this list. Now because of this, each item which was bigger, will become at the top
    of the heap, because its negative is lowest among other heap elements. So by this way, we always
    have the highest element of lower half and lowest element of upper half.
    """

    def __init__(self):
        self.__lower_half = []
        self.__upper_half = []
        self.__medians = []

    def print(self):
        print('lower: ', self.__lower_half)
        print('higher: ', self.__upper_half)

    def insert_number(self, item) -> None:
        if len(self.__lower_half) <= len(self.__upper_half):
            hq.heappush(self.__lower_half, -item)
        else:
            hq.heappush(self.__upper_half, item)
        self.__balance_if_needed()
        self.__medians.append(self.get_median())

    def __balance_if_needed(self) -> None:
        if len(self.__upper_half) == 0 or len(self.__lower_half) == 0:
            return
        lower_max = - self.__lower_half[0]
        upper_min = self.__upper_half[0]
        if lower_max > upper_min:
            hq.heappop(self.__lower_half)
            hq.heappop(self.__upper_half)
            hq.heappush(self.__upper_half, lower_max)
            hq.heappush(self.__lower_half, -upper_min)

    def get_median(self) -> int:
        return - self.__lower_half[0]

    def get_median_list(self):
        return self.__medians.copy()
