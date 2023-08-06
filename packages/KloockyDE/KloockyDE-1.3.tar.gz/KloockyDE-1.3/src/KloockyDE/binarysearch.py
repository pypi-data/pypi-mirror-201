def binarysearch(L, item, *args, **kwargs):
    """
    Searches list of numbers for item, returns index of item
        via binarysearch-algorithm
        list has to be sorted in ascending order
    :param      L: list : list of numbers in ascending order
    :param      item: number : searched number
    :return:    int : index of searched number in list
                None, if number is not in list or list is empty
    """
    if len(L) == 0:
        return None
    elif len(L) == 1:
        if L[0] == item:
            return 0
        else:
            return None
    elif len(L) >= 2:
        pivot = int(len(L) / 2)
        if item == L[pivot]:
            return pivot
        elif item < L[pivot]:
            return binarysearch(L[:pivot], item)
        elif item > L[pivot]:
            temp = binarysearch(L[pivot + 1:], item)
            if type(temp) == int:
                return temp + pivot + 1
            else:
                return temp