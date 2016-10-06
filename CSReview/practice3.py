def binary_search(array, value):
    if len(array) == 0:
        return None
    midpoint = len(array)/2
    if array[midpoint] == value:
        return value
    if value < array[midpoint]:
        return binary_search(array[:midpoint], value)
    else:
        return binary_search(array[midpoint+1:], value)

def merge_sort(array):
    if len(array) <= 1:
        return array
    midpoint = len(array)/2
    left = merge_sort(array[:midpoint])
    right = merge_sort(array[midpoint:])

    left_index = 0
    right_index = 0
    results = []
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            results.append(left[left_index])
            left_index += 1
        else:
            results.append(right[right_index])
            right_index += 1
    results += left[left_index:]
    results += right[right_index:]
    return results

def quick_sort(array):
    low = []
    equal = []
    high = []
    if len(array) <= 1:
        return array
    pivot = array[0]
    for value in array:
        if value < pivot:
            low.append(value)
        if value == pivot:
            equal.append(value)
        if value > pivot:
            high.append(value)
        return quick_sort(low)+equal+quick_sort(high)

def insertion_sort(array):
    for index in range(1, len(array)):
        value = array[index]
        pointer = index
        while pointer > 0 and value < array[pointer-1]:
            array[pointer] = array[pointer-1] # !
            pointer -= 1
        array[pointer] = value

def radix_sort(array):
    placement = 1
    radix = 10
    finished = False
    while not finished:
        finished = True

        buckets = defaultdict(list)

        # put in buckets
        for value in array:
            temp = value/placement
            key = temp%radix
            buckets[key].append(value)
            if temp > 0:
                finished = False

        # reorganize buckets in array
        index  = 0
        for key in range(radix):
            for value in buckets[key]:
                array[index] = value
                index += 1

        placement *= radix
