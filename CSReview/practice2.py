def binary_search(array, item):
    if len(array) == 0:
        return None
    midpoint = len(array)/2
    if array[midpoint] == item:
        return item
    if item < array[midpoint]: # left
        return binary_search(array[:midpoint], item)
    else: # right
        return binary_search(array[midpoint+1:], item)

def merge_sort(array):
    if len(array) < 2:
        return array
    # split
    midpoint = len(array)/2
    left_part = merge_sort(array[:midpoint])
    right_part = merge_sort(array[midpoint:])

    # merge
    index_left = 0
    index_right = 0
    result = []
    while index_left < len(left_part) and index_right < len(right_part):
        if left_part[index_left] < right_part[index_right]:
            result.append(left_part[index_left])
            index_left += 1
        else:
            result.append(right_part[index_right])
            index_right += 1
    result += left_part[index_left:]
    result += right_part[index_right:]
    return result

def radix_sort(array):
    radix = 10
    finished = False
    placement = 1
    while not finished:
        finished = True
        buckets = defaultdict(list)

        # put in buckets by radix
        for value in array:
            tmp = value/placement #!
            key = tmp%radix
            buckets[key].append(value)
            if tmp > 0:
                finished = False

        # merge buckets
        index = 0
        for key in range(radix):
            for value in buckets[key]:
                array[index] = value
                index += 1

        placement *= radix
    return array

def quick_sort(array):
    less = []
    equal = []
    more = []
    if len(array) > 1:
        pivot = array[0]
        for value in array:
            if value < pivot:
                less.append(value)
            if value == pivot:
                equal.append(value)
            if value > pivot:
                more.append(value)
        return quick_sort(less) + equal + quick_sort(more)
    else:
        return array

def insertion_sort(array):
    for index, value in enumerate(array[1:]):
        position = index
        while position > 0 and value < array[position-1]: #!
            array[position] = array[position-1]
            position -= 1
        array[position] = value
    return array