def bubblesort_list(L, asc=True, *args, **kwargs):
    """
    Sorts list of numbers via bubblesort-algorithm
        ascending/descending via parameter asc
    :param      L: list : list of numbers
    :param      asc: bool : decides wether returned list is sorted ascending (when True) or descending (when False)
    :return:    list : sorted list
    """
    A = L.copy()
    if len(A) <= 1:
        return A
    elif asc:
        for x in range(len(A)):
            for i in range(len(A) - x):
                if i == (len(A) - x - 1):
                    pass
                elif A[i + 1] < A[i]:
                    A[i], A[i+1] = A[i+1], A[i]
        return A
    elif not asc:
        for x in range(len(A)):
            for i in range(len(A) - x):
                if i == (len(A) - x - 1):
                    pass
                elif A[i + 1] > A[i]:
                    A[i], A[i+1] = A[i+1], A[i]
        return A