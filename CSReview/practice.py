from collections import defaultdict, deque
import sys

## MapReduce ###########################################################################

from mrjob.job import MRJob

class MRTest(MRJob): # word count

    def mapper(self, key, line):
        for word in line.split():
            yield word, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRTest.run()

## Binary Search ########################################################################

def binary_search(array, value):
    """
    Time Complexity: O(log n)
    Space Complexity: O(log n)
    """
    if len(array) == 0:
        return None
    midpoint = len(array)/2
    if array[midpoint] == value:
        return value
    if value < array[midpoint]: # left search #!
        return binary_search(array[:midpoint], value) #!
    else: # right search
        return binary_search(array[midpoint+1:], value) #!

## Sorting ###########################################################################

def merge_sort(array):
    """
    Time Complexity: O(n*log n) (average, worst, best)
    Space Complexity: O(n*log n) (can be O(n) and O(1))
    """
    if len(array) < 2: #!
        return array

    # split
    midpoint = len(array)/2
    array_left = merge_sort(array[:midpoint]) #!
    array_right = merge_sort(array[midpoint:]) #!

    # merge
    index_left = 0
    index_right = 0
    result = []
    while index_left < len(array_left) and index_right < len(array_right):
        if array_left[index_left] < array_right[index_right]:
            result.append(array_left[index_left])
            index_left+=1
        else:
            result.append(array_right[index_right])
            index_right+=1
    result += array_left[index_left:]
    result += array_right[index_right:]
    return result

def radix_sort(array): #!
    """
    Time Complexity: O(radix*n)
    Space Complexity: O(radix+n)
    """
    radix = 10
    finished = False
    count = 1
    while not finished:
        finished = True
        buckets = defaultdict(list) #!

        # put in buckets by radix
        for value in array:
            result = value/count #!
            key = result%radix #!
            buckets[key].append(value)
            if result > 0: #!
                finished = False

        # merge buckets
        index = 0
        for key in range(radix):
            for value in buckets[key]:
                array[index] = value
                index +=1

        count *= radix
    return array

def quick_sort(array): #!
    """
    Time Complexity: O(n*log n) average, O(n**2) worst case
    Space Complexity: O(n*log n) (can be O(log n) if in place)
    """
    less = []
    equal = []
    more = []
    if len(array) > 1: #!
        pivot = array[0]
        for value in array:
            if value < pivot:
                less.append(value)
            if value == pivot:
                equal.append(value)
            if value > pivot:
                more.append(value)
        return quick_sort(less) + equal + quick_sort(more)
    return array

def insertion_sort(array): #!
    """
    Time Complexity: O(n**2) worst and average, O(n) best case
    Space Complexity: O(1)
    """
    for index in range(1, len(array)):
        value = array[index]
        position = index
        while position > 0 and value < array[position-1]:
            array[position] = array[position-1]
            position -= 1
        array[position] = value
    return array

def bucket_sort(array): # for anagrams
    """
    Time Complexity: O(k+n)
    Space Complexity: O(k+n)
    """
    buckets = defaultdict(list)
    for value in array:
        key = sorted(value)
        key = ''.join(key)
        buckets[key].append(value)

    index = 0
    for key, values in buckets.iteritems():
        for value in values:
            array[index] = value
            index += 1

    return array

## Trees ###########################################################################

class TreeNode:
    def __init__(self, data, parent = None):
        self.left = None
        self.right = None
        self.data = data
        self.parent = parent # useful for 'remove'
        # self.height # if is an AVL tree

def insert(node, data): # without rotations
    if node is None:
        return
    if data < node.data: # left
        if node.left is None:
            node.left = TreeNode(data, node)
        else:
            insert(node.left, data)
    else: # right
        if node.right is None:
            node.right = TreeNode(data, node)
        else:
            insert(node.right, data)

def remove(node, data): # without rotations
    # if node have:
    #   - 0 children: set its reference as None in the parent
    #   - 1 children: set its reference as its child in the parent
    #   - 2 children: substitute node for the leftest node is the right children
    pass

def search_recursively(node, data):
    if node is None:
        return None
    if node.data == data:
        return data
    if data < node.data:
        search_recursively(node.left, data)
    else:
        search_recursively(node.right, data)

def search_iteratively(node, data):
    current_node = node
    while current_node is not None:
        if current_node.data == data:
            return current_node
        if data < node.data:
            current_node = current_node.left
        else:
            current_node = current_node.right
    return None

def inorder(node):
    if node is None:
        return
    inorder(node.left)
    print str(node.data)
    inorder(node.right)

def preorder(node):
    if node is None:
        return
    print str(node.data)
    inorder(node.left)
    inorder(node.right)

def postorder(node):
    if node is None:
        return
    inorder(node.left)
    inorder(node.right)
    print str(node.data)

## Graphs ###########################################################################

class GraphNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.visited = False

def depth_first_search(node, visit):
    if node is None:
        return
    visit(node)
    node.visited = True
    for child in node.children:
        if not child.visited:
            depth_first_search(child, visit)

def breath_first_search(node, visit):
    queue = deque()
    deque.appendleft(node)
    node.visited = True
    while len(deque) != 0:
        current_node = deque.pop()
        visit(current_node)
        for child in current_node.children:
            if not child.visited:
                deque.appendleft(child)
                child.visited = True

class DjkstraNode():
    def __init__(self, label):
        self.shortest_distance = sys.maxint
        self.distances = {}
        self.label = label

def djkstra(nodes, initial_node, goal_node): # untested
    initial_node.shortest_distance = 0
    unvisited_nodes = list(nodes)
    while len(unvisited_nodes) > 0:
        # get nearest unvisited node by shortest_distance
        node = sorted(unvisited_nodes, key = lambda x: x.shortest_distance)[0]
        # update its neighboors shortest_distance
        for neighboor in node.distances.keys():
            if neighboor in unvisited:
                new_distance = node.shortest_distance + neighboor.distances[node.label]
                if new_distance < neighboor.shortest_distance:
                    neighboor.shortest_distance = new_distance
        # remove node from unvisited
        unvisited_nodes.remove(node)
    return goal_node.shortest_distance

def greedy_coloring():
    # Use DFS + available colors:
    #   - at each node, paint it with one of the available color and go the next node
    #   - if can't color without conflict, return to previous node and attempt another available color
    pass

def maximum_flow():
    # Use DFS or BFS:
    # 1. Find an augmenting path (one were all the forward edges are not full, and all backwards edges are not empty)
    # 2. Compute the bottleneck capacity
    # 3. Augment each edge and the total flow
    # Obs.: The balance between how much is entering and leaving a node must be kept
    pass

## HashTable ###########################################################################

class HashTable():
    def __init__(self, size):
        self.size = size
        self.buckets = [[]] * size # if open-addressing, self.buckets = [None] * size

    def hashing(self, key):
        return key % self.size

    def insert(self, key, value):
        hashed_key = self.hashing(key)
        self.buckets[hashed_key].append((key, value))

    def remove(self, key_to_remove):
        hashed_key = self.hashing(key_to_remove)
        for index, pair in enumerate(self.buckets[hashed_key]):
            key, value = pair
            if key == key_to_remove:
                return self.buckets[hashed_key].pop(index)
        return None

    def get(self, key_to_get):
        hashed_key = self.hashing(key_to_get)
        for index, pair in enumerate(self.buckets[hashed_key]):
            key, value = pair
            if key == key_to_get:
                return value
        return None

## LinkedLists ###########################################################################

# - Tip: "Runner" technique, use two points instead of one (one slow, and one fast)

class LinkedListNode():
    def __init__(self, data):
        self.next = None
        self.data = data

def insert(start_node, data):
    temp = start_node
    while temp.next is not None:
        temp = temp.next
    temp.next = LinkedListNode(data)

def get(start_node, data):
    temp = start_node
    while temp is not None:
        if temp.data == data:
            return data
        temp = temp.next
    return None

def remove(start_node, data):
    temp = start_node
    if temp.data == data:
        return start_node.next
    while temp.next is not None:
        if temp.next.data == data:
            temp.next = temp.next.next
            return start_node
        temp = temp.next
    return start_node

## Stacks ###########################################################################

class StackNode():
    def __init__(self, data):
        self.next = None
        self.data = data

class Stack():
    def __init__(self, data):
        self.top = None
        self.size = 0

    def insert(self, data):
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def peck(self):
        if self.top is None:
            return None
        return self.top.data

    def remove(self):
        if self.top is None:
            return None
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data

## Queues ###########################################################################

class QueueNode():
    def __init__(self, data):
        self.next = None
        self.data = data

class Queue():
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0

    def insert(self, data):
        temp = QueueNode(data)
        if self.size == 0:
            self.first = temp
            self.last = temp
        else:
            temp = QueueNode(data)
            self.last.next = temp
            self.last = temp
        self.size += 1

    def remove(self):
        if self.size == 0:
            return None
        data = self.first.data
        self.first = self.first.next
        self.size -= 1
        return data