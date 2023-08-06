def heapsort(A):
    """
    Sorts list of comparable items in ascending order via heapsort-algorithm
    :param      A: list : list of comparable items
    :return:    list : sorted list
    """
    heap = [0]
    parent = lambda x : int(x / 2)
    left = lambda x : 2 * x
    right = lambda x : (2 * x) + 1
    def heapifyUp(i_):
        i = i_
        while i > 1 and heap[parent(i)] > heap[i]:
            heap[i], heap[parent(i)] = heap[parent(i)], heap[i]
            i = parent(i)
    def heapifyDown(i_):
        i = i_
        n = len(heap) - 1
        while left(i) <= n:
            if right(i) > n:
                m = left(i)
            else:
                if heap[left(i)] < heap[right(i)]:
                    m = left(i)
                else:
                    m = right(i)
            if heap[i] <= heap[m]:
                break
            heap[i], heap[m] = heap[m], heap[i]
            i = m
    def insert(e):
        heap.append(e)
        heapifyUp(len(heap) - 1)
    def deleteMin():
        e = heap[1]
        heap[1] = heap[-1]
        heap.pop()
        heapifyDown(1)
        return e
    for i in range(len(A)):
        insert(A[i])
    sortiert = []
    for i_ in range(len(heap)):
        if len(heap) >= 2:
            x = deleteMin()
            sortiert.append(x)
    return sortiert