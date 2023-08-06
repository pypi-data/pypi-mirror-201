def linearsearch(L, item, *args, **kwargs):
    """
    Searches list of numbers for item, returns index of first appearance of item
        via linearsearch-algorithm
        list can be unsorted
    :param      L: list : list of numbers
    :param      item: number : searched number
    :return:    int : index of first appearance of searched number in list
                None, if number is not in list or list is empty
    """
    if len(L) == 0:
        return None
    else:
        for i in range(len(L)):
            if L[i] == item:
                return i
        return None