def quicksort_list_asc(L, *args, **kwargs):
    """
    Sorts list of numbers in ascending order via quicksort-algorithm
    :param      L: list : list of numbers
    :return:    list : sorted list
    """
    if len(L) <= 1:
        return L
    else:
        pivot_index = int(len(L) / 2)
        pivot = L[pivot_index]
        left, right = [], []
        for x in range(len(L)):
            if x == pivot_index:
                pass
            elif L[x] <= pivot:
                left.append(L[x])
            elif L[x] > pivot:
                right.append(L[x])
        return quicksort_list_asc(left) + [pivot] + quicksort_list_asc(right)

def quicksort_list_desc(L, *args, **kwargs):
    """
    Sorts list of numbers in descending order via quicksort-algorithm
    :param      L: list : list of numbers
    :return:    list : sorted list
    """
    if len(L) <= 1:
        return L
    else:
        pivot_index = int(len(L) / 2)
        pivot = L[pivot_index]
        left, right = [], []
        for x in range(len(L)):
            if x == pivot_index:
                pass
            elif L[x] > pivot:
                left.append(L[x])
            elif L[x] <= pivot:
                right.append(L[x])
        return quicksort_list_desc(left) + [pivot] + quicksort_list_desc(right)