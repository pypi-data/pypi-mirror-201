def maxsort_list(L, *args, **kwargs):
    """
    Sorts list of numbers in ascending order via maxsort-algorithm
    :param      L: list : list of numbers
    :return:    list : sorted list
    """
    def maxsearch(L):
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
    if len(L) <= 1:
        return L
    A = L.copy()
    for x in range(len(A)):
        i = len(A) - x - 1
        if i == 0:
            pass
        else:
            maximum = maxsearch(A[:i+1])
            A[maximum], A[i] = A[i], A[maximum]
    return A

def minsort_list(L, *args, **kwargs):
    """
    Sorts list of numbers in descending order via minsort-algorithm
    :param      L: list : list of numbers
    :return:    list : sorted list
    """
    def minsearch(L):
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
    if len(L) <= 1:
        return L
    A = L.copy()
    for x in range(len(A)):
        i = len(A) - x - 1
        if i == 0:
            pass
        else:
            minimum = minsearch(A[:i + 1])
            A[minimum], A[i] = A[i], A[minimum]
    return A