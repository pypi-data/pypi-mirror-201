def minsearch(L, *args, **kwargs):
    """
    Searches for smallest number in given list, returns index of first appearance of that number
        via minsearch-algorithm
        list can be unsorted
    :param      L: list : list of numbers
    :return:    int : index of first appearance of smallest number
                None, if List is empty
    """
    if len(L) == 0:
        return None
    elif len(L) == 1:
        return 0
    else:
        m = 0
        for i in range(len(L)):
            if i == 0:
                pass
            elif L[i] < L[m]:
                m = i
        return m

def maxsearch(L, *args, **kwargs):
    """
    Searches for biggest number in given list, returns index of first appearance of that number
        via maxsearch-algorithm
        list can be unsorted
    :param      L: list : list of numbers
    :return:    int : index of first appearance of biggest number
                None, if List is empty
        """
    if len(L) == 0:
        return None
    elif len(L) == 1:
        return 0
    else:
        m = 0
        for i in range(len(L)):
            if i == 0:
                pass
            elif L[i] > L[m]:
                m = i
        return m