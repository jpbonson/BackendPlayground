def bubble_sort(array):
    """
    In bubble sort, we start at the beginning of the array and swap the first two elements if
    the first is greater than the second. Then, we go to the next pair, and so on, continuously
    making sweeps of the array until it is sorted.

    Time Complexity: O(n**2) average and worst, O(n) best case
    Space Complexity: O(1) (in place)
    """
    for _ in array:
        for index in range(len(array)-1):
            if array[index] > array[index+1]:
                tmp = array[index]
                array[index] = array[index+1]
                array[index+1] = tmp
    return array

def insertion_sort(array):
    """
    It always maintains a sorted sublist in the lower positions of the list. Each new item is then 
    inserted back into the previous sublist such that the sorted sublist is one item larger.

    - One of the principal advantages of the insertion sort is that it works very efficiently for lists that 
    are nearly sorted initially. Furthermore, it can also work on data sets that are constantly being added to.

    Example:
    {18,  6,  9,  1,  4, 15, 12,  5,  6,  7, 11}
    { 6, 18,  9,  1,  4, 15, 12,  5,  6,  7, 11}
    { 6,  9, 18,  1,  4, 15, 12,  5,  6,  7, 11}
    { 1,  6,  9, 18,  4, 15, 12,  5,  6,  7, 11}
    { 1,  4,  6,  9, 18, 15, 12,  5,  6,  7, 11}
    { 1,  4,  6,  9, 15, 18, 12,  5,  6,  7, 11}
    { 1,  4,  6,  9, 12, 15, 18,  5,  6,  7, 11}
    { 1,  4,  5,  6,  9, 12, 15, 18,  6,  7, 11}
    { 1,  4,  5,  6,  6,  9, 12, 15, 18,  7, 11}
    { 1,  4,  5,  6,  6,  7,  9, 12, 15, 18, 11}
    { 1,  4,  5,  6,  6,  7,  9, 11, 12, 15, 18}

    Time Complexity: O(n**2) average and worst, O(n) best case
    Space Complexity: O(1) (in place)

    """
    for index in range(1,len(array)):
        value = array[index]
        position = index
        while position > 0 and value < array[position-1]:
            array[position] = array[position-1]
            position -= 1
        array[position] = value
    return array

def selection_sort(array):
    """
    Selection sort is the child's algorithm: simple, but inefficient. Find the smallest element
    using a linear scan and move it to the front (swapping it with the front element). Then,
    find the second smallest and move it, again doing a linear scan. Continue doing this
    until all the elements are in place.
    
    Time Complexity: O(n**2) (average and worst case)
    Space Complexity: O(1)
    """
    pass

def merge_sort(array): # nice one!
    """
    The Merge Sort use the Divide-and-Conquer approach to solve the sorting problem. 
    First, it divides the input in half using recursion. After dividing, it sort the halfs and merge 
    them into one sorted output.

    - very good overall
    - python uses a hybrid version of merge sort with insertion sort
        - timsort: same complexity as merge sort, but best case is O(n)

    Example:
    {18, 6, 9, 1, 4, 15, 12, 5, 6, 7, 11}
    {18, 6, 9, 1, 4} {15, 12, 5, 6, 7, 11}
    {18, 6} {9, 1, 4} {15, 12, 5} {6, 7, 11}
    {18} {6} {9} {1, 4} {15} {12, 5} {6} {7, 11}
    {18} {6} {9} {1} {4} {15} {12} {5} {6} {7} {11}
    {18} {6} {9} {1, 4} {15} {5, 12} {6} {7, 11}
    {6, 18} {1, 4, 9} {5, 12, 15} {6, 7, 11}
    {1, 4, 6, 9, 18} {5, 6, 7, 11, 12, 15}
    {1, 4, 5, 6, 6, 7, 9, 11, 12, 15, 18}
    
    Time Complexity: O(n*log n) (average and worst case) (Each recursive call has O(n) runtime, and a total of O(log n) recursions are required)
    Space Complexity: O(n) (or O(1) if using linked lists)
    """
    if len(array) < 2:
        return array

    mid = len(array)/2
    right_part = merge_sort(array[mid:])
    left_part = merge_sort(array[:mid])

    right_index = 0
    left_index = 0
    result = []
    while right_index < len(right_part) and left_index < len(left_part):
        if right_part[right_index] > left_part[left_index]:
            result.append(left_part[left_index])
            left_index += 1
        else:
            result.append(right_part[right_index])
            right_index += 1
    result += right_part[right_index:]
    result += left_part[left_index:]
    return result

import random
def quick_sort(array):
    """
    Quicksort is admirably known as the algorithm that sorts an array
    while preparing to sort it. For contrast, recall that merge sort
    first partitions an array into smaller pieces, then sorts each piece,
    then merge the pieces back. Quicksort actually sorts the array
    during the partition phase.
    Quicksort works by selecting an element called a pivot and splitting
    the array around that pivot such that all the elements in, say, the
    left sub-array are less than pivot and all the elements in the right
    sub-array are greater than pivot. The splitting continues until the
    array can no longer be broken into pieces. That's it. Quicksort is
    done.

    Example:
    {18, 6, 9, 1, 4, 15, 12, 5, 6, 7, 11}
    {6, 9, 1, 4, 12, 5, 6, 7, 11} {15} {18}
    {6, 9, 1, 4, 5, 6, 7, 11} {12} {15} {18}
    {1, 4} {5} {6, 9, 6, 7, 11} {12} {15} {18}
    {1} {4} {5} {6} {6} {9, 7, 11} {12} {15} {18}
    {1} {4} {5} {6} {6} {7} {9, 11} {12} {15} {18}
    {1} {4} {5} {6} {6} {7} {9} {11} {12} {15} {18}
    
    Time Complexity: O(n*log n) average case, O(n**2) worst case
    Space Complexity: O(log n)
    """
    def swap(array, x, y):
        array[x], array[y] = array[y], array[x]

    def partition(array, first_index, last_index) :
        pivot = first_index + random.randrange(last_index - first_index + 1)
        swap(array, pivot, last_index)
        for i in range(first_index, last_index):
            if array[i] <= array[last_index]:
                swap(array, i, first_index)
                first_index += 1
        swap(array, first_index, last_index)
        return first_index

    def _quicksort(array, first_index, last_index):
        if first_index < last_index:
            pivot = partition(array, first_index, last_index)
            _quicksort(array, first_index, pivot-1)
            _quicksort(array, pivot+1, last_index)
 
    _quicksort(array, 0, len(array)-1)
    return array

def quick_sort_simple(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return quick_sort_simple(less)+equal+quick_sort_simple(greater) # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array

def heap_sort(array):
    """
    Approach:
    Heap sort happens in two phases. In the first phase, the array
    is transformed into a heap. A heap is a binary tree where
    1) each node is greater than each of its children
    2) the tree is perfectly balanced
    3) all leaves are in the leftmost position available.
    In phase two the heap is continuously reduced to a sorted array:
    1) while the heap is not empty
    - remove the top of the head into an array
    - fix the heap.

    pseudo-code:
        Heap h = new Heap();
        for (int i = 0; i < data.Length; i++)
           h.Add(data[i]);
        int[] result = new int[data.Length];
        for (int i = 0; i < data.Length; i++)
           data[i] = h.RemoveLowest();
    
    - Heap sort has the disadvantage of not being stable
    - Heaps, also known as priority queues

    Time Complexity: O(n*log n) (average and worst case)
    Space Complexity: O(1) (or O(n), depeding on how the heap is created)
    """
    def swap(array, x, y):
        tmp = array[x]
        array[x] = array[y]
        array[y] = tmp

    def moveDown(array, first, last):
        largest = 2 * first + 1
        while largest <= last:
            # right child exists and is larger than left child
            if ( largest < last ) and ( array[largest] < array[largest + 1] ):
                largest += 1
     
            # right child is larger than parent
            if array[largest] > array[first]:
                swap( array, largest, first )
                # move down to largest child
                first = largest;
                largest = 2 * first + 1
            else:
                return # force exit

    # convert array to heap
    length = len(array)-1
    leastParent = length/2
    for index in reversed(range(0, leastParent+1)):
        moveDown(array, index, length)
     
    # flatten heap into sorted array
    for i in range ( length, 0, -1 ):
        if array[0] > array[i]:
            swap( array, 0, i )
            moveDown( array, 0, i - 1 )

    return array
  
def bucket_sort(array):
    """
    Bucket sort, or bin sort, is a sorting algorithm that works by distributing the elements of an array 
    into a number of buckets. Each bucket is then sorted individually, either using a different sorting algorithm, 
    or by recursively applying the bucket sorting algorithm.

    Time Complexity: O(n+k) average, and O(n**2) worst
    Space Complexity: O(n)
    """
    # http://www.geekviewpoint.com/python/sorting/bucketsort
    # https://www-927.ibm.com/ibm/cas/hspc/student/algorithms/BucketSort.html
    # a type of bucket sort (counting sort): http://www.javacodex.com/Sorting/Bucket-Sort

    # modified bucket sort for anagrams:
    buckets = defaultdict(list)
    for value in array:
        sorted_value = sorted(value)
        buckets[''.join(sorted_value)].append(value)
    results1 = []
    results2 = []
    for key, bucket in buckets.iteritems():
        if len(bucket) == 1:
            results1 += bucket
        else:
            results2 += bucket
    return results1 + results2

from collections import defaultdict
def radix_sort(array): # nice one!
    """
    Radix sort is a sorting algorithm for integers (and some other data types) that takes
    advantage of the fact that integers have a finite number of bits. In radix sort, we iterate
    through each digit of the number, grouping numbers by each digit. For example, if we
    have an array of integers, we might first sort by the first digit, so that the Os are grouped
    together. Then, we sort each of these groupings by the next digit. We repeat this process
    sorting by each subsequent digit, until finally the whole array is sorted.

    The runtime is O(n * k), where k is the size of the key. (32-bit integers, taken 4 bits at a time, would 
    have k = 8.) The primary disadvantage is that some types of data may use very long keys (strings, for instance), 
    or may not easily lend itself to a representation that can be processed from least significant to most-significant. 
    (Negative floating-point values are the most commonly cited example.)

    Note that this recursive sorting algorithm has particular application to parallel computing, 
    as each of the bins can be sorted independently.

    For decimal values, the number of buckets is 10, as the decimal
    system has 10 numerals/cyphers (i.e. 0,1,2,3,4,5,6,7,8,9). Then
    the keys are continuously sorted by significant digits.
    
    Time Complexity: O(nk) (eg.: k is the length of the longest number)
    Space Complexity: O(n+k)
    """
    RADIX = 10
    max_length = False
    placement = 1
     
    while not max_length:
        max_length = True
        buckets = defaultdict(list)
     
        # split array between lists
        for value in array:
            tmp = value/placement
            buckets[tmp % RADIX].append(value)
            if max_length and tmp > 0:
                max_length = False
     
        # empty lists into array
        index = 0
        for key in range(RADIX):
            for value in buckets[key]:
                array[index] = value
                index += 1
     
        # move to next digit
        placement *= RADIX
    return array

def test_sorts():
    def test(sorting):
        try:
            result = sorting([3,7,9,1,5,2,4,6,10,8])
            expected = range(1, 11)
            assert result == expected
            result = sorting([3,7,9,1])
            expected = [1,3,7,9]
            assert result == expected
            result = sorting([5,6,7,8])
            expected = [5,6,7,8]
            assert result == expected
        except AssertionError as e:
            print "result: "+str(result)
            print "expected: "+str(expected)
            raise e
    test(bubble_sort)
    test(insertion_sort)
    test(merge_sort)
    test(heap_sort)
    test(quick_sort)
    test(quick_sort_simple)
    # test(bucket_sort)
    test(radix_sort)

################

def binary_search(array, item):
    """
    Time Complexity: O(log n)
    Space Complexity: O(log n)
    """
    if len(array) == 0:
        return False
    else:
        midpoint = len(array)/2
        if array[midpoint] == item:
            return True
        if item < array[midpoint]:
            return binary_search(array[:midpoint], item)
        else:
            return binary_search(array[midpoint+1:], item)

def test_binary_search():
    testlist = [0, 1, 2, 8, 13, 17, 19, 32, 42]
    assert binary_search(testlist, 3) == False
    assert binary_search(testlist, 13) == True

################

# 1. You are given two sorted arrays, A and B, where A has a large enough buffer at the
# end to hold B. Write a method to merge B into A in sorted order.
def question1(array1, array2):
    """
    Inputs:
    [1,2,3,4], [5,6,7,8] = [1,2,3,4,5,6,7,8]
    [1,3,5], [2,4] = [1,2,3,4,5]
    [1,2,4], [2,4] = [1,2,2,4]
    [1,2,3], [] = [1,2,3]

    Assumption:
    - in place
    - dont know where the last element in A is (bad assumption, it was easy to discover it)

    Improvement:
    - if started at the end of arrays, and knowing where the last element is, it would be possible to solve it in O(n1+n2)

    Time Complexity: O(n1**2+n2)
    Space Complexity: O(1)
    """
    if len(array2) == 0:
        return array1
    array1 = array1 + [None] * len(array2)
    counter1 = 0
    counter2 = 0
    done = False
    while array1[counter1] is not None and counter1+1 < len(array1):
        if array1[counter1] <= array2[counter2]:
            # iterate until an element in B is bigger than in A
            # or A finishes
            counter1 += 1
        else:
            # move to create space for the B element in A
            for index in reversed(range(counter1, len(array1)-1)):
                if array1[index] is not None:
                    array1[index+1] = array1[index]
            array1[counter1] = array2[counter2]
            counter1 += 1
            counter2 += 1
    # just add the remaing B elements
    for value in array2[counter2:]:
        array1[counter1] = value
        counter1 += 1
    return array1

# 2. Write a method to sort an array of strings so that all the anagrams are next to each
# other.
from collections import defaultdict
def question2(array):
    """
    Questions
    - are there only anagrams in the array?
    - unrelated anagrams should be next to each other, or just the related ones?

    Assumption:
    - there is a mix of anagrams and non-anagrams, all anagrams should be together (related or not)
    - it doesnt need to be in place

    Idea:
    - create a hash map with lists where the keys are the sorted words, then transform the hash map into a list
    (modified bucket sort)

    How to find out if it is an anagram:
    - sort the strings and compare
    """
    buckets = defaultdict(list)
    for value in array:
        sorted_value = sorted(value)
        buckets[''.join(sorted_value)].append(value)
    results1 = []
    results2 = []
    for key, bucket in buckets.iteritems():
        if len(bucket) == 1:
            results1 += bucket
        else:
            results2 += bucket
    return results1 + results2

# 3. Given a sorted array of n integers that has been rotated an unknown number of
# times, write code to find an element in the array. You may assume that the array was
# originally sorted in increasing order.
def question3(array):
    """
    Input:
    - [3,4,5,1,2], 4

    Ideas:
    - rotate the array so it starts by the lesser element, and then run a binary search O(n+log n)
    - adapt binary search so it takes in considering if the part of the array we are searching is the rotation point O(log n)
        - be careful with duplicates
    """
    pass

# 4. Imagine you have a 20 GB file with one string per line. Explain how you would sort
# the file.
# Assumpton: alphabetical order
# - too much to put everything on memory
# - divide and sort by buckets? like, "bucket with strings that start with 'a'"
# - then just join the buckets
# - how to define the best bucket criteria? run a counter over the lines, for the first letters?
# steps:
# - run through the file, and go creating the new bucket files on HD, appending the strings to the files
# - run a sorting algorithm in each bucket
# - join buckets
# alternative:
# - divide file into buckets, don't care about the keys, only that they are fixed-size
# - merge each file to each other until got a final file

# 5. Given a sorted array of strings which is interspersed with empty strings, write a
# method to find the location of a given string.
def question5(array):
    """
    Inputs:
    - ['aba', 'blah', '', 'coat', 'dino', '', ''], 'dino'

    Idea:
    - binary search, but ignore node if it is empty (by 'ignore': find the nearest node that is not empty)
    """
    pass

# 6. Given an MxN matrix in which each row and each column is sorted in ascending
# order, write a method to find an element.
def question6(array):
    """
    Inputs:
    [[1,2],
     [3,4]]

    Idea:
    - binary search every line to find the element O(m*log n)
    - alternative: binary search both lines and columns at the same time
        - use the diagonals to divide the matrix in 4 quadrants, and the search the upper-right and the lower-left ones
    """
    pass

# 8. Imagine you are reading in a stream of integers. Periodically, you wish to be able to
# look up the rank of a number x (the number of values less than or equal to x). Implement
# the data structures and algorithms to support these operations. That is, implement
# the method track(int x), which is called when each number is generated,
# and the methodgetRankOf'Number (int x), which returns the number of values
# less than or equal to x (not including x itself).
def question8(array):
    """
    Inputs:
    - 

    Assumption:
    - 

    Idea:
    - use a binary search tree with counters in the nodes
    - or a sorted list that store the values and the counters
    """
    pass

if __name__ == "__main__":
    test_sorts()
    test_binary_search()
    result = question1([1,3,5], [2,4])
    result = question2(['casa', 'coice', 'saca', 'comida', 'caas', 'idacom', 'blah'])
    print str(result)