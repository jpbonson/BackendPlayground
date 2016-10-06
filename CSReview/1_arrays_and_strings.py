# 1. Implement an algorithm to determine if a string has all unique characters. What
# if you cannot use additional data structures?
def question1(some_input):
    """
    Test Cases:
    - "aaaaaa": False
    - "a": True
    - "": error
    - None: error
    - not a string: error
    - "abc": True
    - infinite string: it will be 'False' after some time
    - "thing\n": True (if special characters are considered different characters)
    - "thing\n\n": False

    Time Complexity: O(n**2)
    Space Complexity: O(1)
    """

    if not isinstance(some_input, basestring):
        raise ValueError("some message")
    if some_input is None:
        raise ValueError("some message")
    if len(some_input) == 0:
        raise ValueError("some message")

    characters = set()
    for char in some_input: #O(n)
        if char not in characters: # O(1) (worst: O(n))
            characters.add(char)
        else:
            return False
    return True

import string
def question1_alt(some_input):
    """
    Restriction:
    - The string contains only printable ASCII characters

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    characters_dict = {}
    for index, c in enumerate(string.printable): # O(1)
        characters_dict[c] = index

    checks = [False]*len(string.printable)
    for char in some_input: # O(n)
        if checks[characters_dict[char]]: # O(1)
            return False
        checks[characters_dict[char]] = True
    return True

# 2. Implement a function void reverse(char* str) in C or C++ which reverses a null-terminated
# string.
from collections import deque
def question2(some_input):
    """
    Test Cases:
    - "abc": "cba"
    - "a": "a"
    - "": ""
    - None: error
    - not a string: error
    - infinite string: will never finish executing, but it is impossible to reverse a infinite string anyway

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not isinstance(some_input, basestring):
        raise ValueError("some message")
    if some_input is None:
        raise ValueError("some message")

    result = deque()
    for char in some_input: # O(n)
        result.appendleft(char) # O(1)
    return ''.join(result) # O(n)

def question2_alt(some_input):
    """
    Restriction:
    - Do it in place

    Time Complexity: O(n)
    """
    some_input = list(some_input)

    start_pos = 0
    end_pos = len(some_input)-1

    while(start_pos < end_pos):
        temp = some_input[end_pos]
        some_input[end_pos] = some_input[start_pos]
        some_input[start_pos] = temp
        start_pos += 1
        end_pos -= 1
    return ''.join(some_input)

# 3. Given two strings, write a method to decide if one is a permutation of the other.
from itertools import permutations
from collections import defaultdict
def question3(some_input1, some_input2, easy_way=True):
    """
    Test Cases:
    - "abc", "bca": True
    - "", "abc": False
    - "", "": True
    - "aaaaaa", "aa": False
    - "aab", "abb": False
    - "12 34", " 1234": True
    - None: error
    - not a string: error

    Easy way:
    Time Complexity: O(n+p)
    Space Complexity: O(p)

    Hard way:
    Time Complexity: O(n+k)
    Space Complexity: O(k)

    Assumptions:
    - is case sensitive
    - whitespace is significant

    Alternative:
    - sort the strings and then compare if they are equal
    """
    if not isinstance(some_input1, basestring) or not isinstance(some_input2, basestring):
        raise ValueError("some message")
    if some_input1 is None or some_input2 is None:
        raise ValueError("some message")

    if len(some_input1) != len(some_input2):
        return False

    if easy_way:
        perms = permutations(some_input1) # O(n)
        perms_list = set([''.join(p) for p in perms]) # O(p)
        if some_input2 in perms_list: #O(1)
            return True
        else:
            return False
    else:
        counter1 = defaultdict(int)
        for c in some_input1: # O(n)
            counter1[c] += 1 # O(1)
        counter2 = defaultdict(int)
        for c in some_input2: # O(n)
            counter2[c] += 1 # O(1)

        if len(counter1.keys()) != len(counter2.keys()): # O(1)
            return False

        for key in counter1.keys(): # O(k)
            if key in counter2: # O(1)
                if counter1[key] != counter2[key]: # O(1)
                    return False
            else:
                return False

        return True

# 4. Write a method to replace all spaces in a string with'%20'. You may assume that
# the string has sufficient space at the end of the string to hold the additional
# characters, and that you are given the "true" length of the string. (Note: if implementing
# in Java, please use a character array so that you can perform this operation
# in place.)
def question4(some_input, easy_way=True):
    """
    Test Cases:
    - "Mr John Smith": "Mr%20Dohn%20Smith"
    - "": ""
    - None: error
    - not a string: error
    - "   ": "%20%20%20"

    Obs.: This problem doesn't translates to Python very well, since it isn't a strong typed language.
    """

    if not isinstance(some_input, basestring):
        raise ValueError("some message")
    if some_input is None:
        raise ValueError("some message")

    if easy_way:
        return some_input.replace(" ", "%20")
    else:
        test = some_input.replace(" ", "%20")
        some_input = list(some_input)
        for index, c in enumerate(some_input):
            if c == " ":
                some_input[index] = "%20"
        some_input = ''.join(some_input)
        assert some_input == test
        return some_input

# 5. Implement a method to perform basic string compression using the counts
# of repeated characters. For example, the string aabcccccaaa would become
# a2blc5a3. 
# Warning: If the "compressed" string would not become smaller than the original
# string, your method should return the original string.
def question5(some_input):
    """
    Test Cases:
    - "aabcccccaaa": "a2blc5a3"
    - "abc": "abc"
    - "aaa": "a3"
    - "": ""
    - None: error
    - not a string: error
    - "ababababab": "ababababab"
    - "122333": "122333"

    Time Complexity: O(n+r)
    Space Complexity: O(r)

    Improvement:
    - check if the compression will be smaller than the original string before compressing
    """
    if not isinstance(some_input, basestring):
        raise ValueError("some message")
    if some_input is None:
        raise ValueError("some message")

    if len(some_input) <= 2: # O(1)
        return some_input

    result = [some_input[0]] # O(1)
    current_char_count = 1
    for c in some_input[1:]: # O(n)
        if c == result[-1]: # O(1)
            current_char_count += 1
        else:
            result.append(str(current_char_count)) # O(1)
            current_char_count = 1
            result.append(c) # O(1)
    result.append(str(current_char_count)) # O(1)

    result = ''.join(result) # O(r)
    if len(result) < len(some_input):
        return result
    else:
        return some_input

# 6. Given an image represented by an NxN matrix, where each pixel in the image is
# 4 bytes, write a method to rotate the image by 90 degrees. Can you do this in
# place?
def question6(some_input):
    """
    Test Cases:
    - None: error
    - not a matrix of integers NxN: error
    - [[1]] = [[1]]
    - [[1, 2], [3, 4]] = [[3, 1], [4, 2]]
    - [[1, 2, 3], [4, 5, 6], [7, 8, 9]] = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    Time Complexity: O(n**2)
    Space Complexity: O(1) # it is in place
    """

    if some_input is None:
        raise ValueError("some message")
    if not isinstance(some_input, list):
        raise ValueError("some message")
    if len(some_input) == 0:
        raise ValueError("some message")
    if not isinstance(some_input[0], list):
        raise ValueError("some message")
    if len(some_input[0]) == 0:
        raise ValueError("some message")
    if len(some_input) != len(some_input[0]):
        raise ValueError("some message")
    if not isinstance(some_input[0][0], int):
        raise ValueError("some message")

    n = len(some_input[0])
    for layer in range(n/2):
        first = layer
        last = n - 1 - layer
        for index in range(first, last):
            offset = index - first
            temp = some_input[first][index]
            some_input[first][index] = some_input[last-offset][first]
            some_input[last-offset][first] = some_input[last][last - offset]
            some_input[last][last - offset] = some_input[index][last]
            some_input[index][last] = temp
    return some_input

# 7. Write an algorithm such that if an element in an MxN matrix is 0, its entire row
# and column are set to 0.
def question7(some_input):
    """
    Test Cases:
    - None: error
    - not a matrix: error
    - [[1]] = [[1]]
    - [[0]] = [[0]]
    - [[1, 2], [3, 4]] = [[1, 2], [3, 4]]
    - [[1, 2], [0, 4]] = [[0, 2], [0, 0]]
    - [[1, 2, 3], [4, 5, 6], [7, 8, 9]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    - [[1, 2, 0], [4, 5, 6], [7, 8, 9]] = [[0, 0, 0], [4, 5, 0], [7, 8, 0]]
    - [[0, 2, 0], [4, 5, 6], [7, 8, 9]] = [[0, 0, 0], [0, 5, 0], [0, 8, 0]]

    Improvement:
    - if a column already was tagged to set to zero, don't need to check this column anymore
    - obs.: it doesn't apply to lines

    Time Complexity: O(mn+l+cm)
    Space Complexity: O(l+c)
    """

    if some_input is None:
        raise ValueError("some message")
    if not isinstance(some_input, list):
        raise ValueError("some message")
    if len(some_input) == 0:
        raise ValueError("some message")
    if not isinstance(some_input[0], list):
        raise ValueError("some message")
    if len(some_input[0]) == 0:
        raise ValueError("some message")

    zeros_lines = set()
    zeros_cols = set()
    for line_index, line in enumerate(some_input): # O(m)
        for col_index, value in enumerate(line): # O(n)
            if value == 0:
                zeros_lines.add(line_index)
                zeros_cols.add(col_index)

    for line_index in zeros_lines: # O(l)
        some_input[line_index] = [0] * len(some_input[0])

    for col_index in zeros_cols: # O(c)
        for line in some_input: # O(m)
            line[col_index] = 0

    return some_input

# 8. Assume you have a method isSubstring which checks if one word is a
# substring of another. Given two strings, s1 and s2, write code to check if s2 is
# a rotation of s1 using only one call to isSubstring (e.g.,"waterbottle"is a rotation
# of "erbottlewat")
def question8(some_input1, some_input2):
    """
    Test Cases:
    - None: error
    - not a string: error
    - "", "": True
    - "", "water": False
    - "taxis", "water": False
    - "waterbottle", "erbottlewat": True
    - "w", "water": False
    - "babababababa", "babababababa": True
    - "babababababaxx", "babaxxbabababa": True
    - "aaa", "aaa": True

    Notes:
    - order matters

    Time Complexity: O(2n)
    Space Complexity: O(2n)
    """

    if not isinstance(some_input1, basestring) or not isinstance(some_input2, basestring):
        raise ValueError("some message")
    if some_input1 is None or some_input2 is None:
        raise ValueError("some message")

    # if not the same size, False
    if len(some_input1) != len(some_input2): # O(1)
        return False

    if len(some_input1) == 0: # O(1)
        return True

    temp = some_input1+some_input1
    if some_input2 in temp:
        return True
    return False

# implement a hash table using arrays
class HashTable():
    def __init__(self, size = 10):
        self.size = size
        self.table = [[] for x in range(size)]

    def hash_function(self, x):
        return x % self.size

    def insert(self, key, value):
        self.table[self.hash_function(key)].append((key,value))

    def get(self, key):
        list_index = self.hash_function(key)
        for value in self.table[list_index]:
            if value[0] == key:
                return value[1]
        return None

    def remove(self, key):
        list_index = self.hash_function(key)
        to_remove = None
        for value in self.table[list_index]:
            if value[0] == key:
                to_remove = value
                break
        if to_remove is not None:
            self.table[list_index].remove(to_remove)
            return True
        else:
            return False

def test_hash_table():
    table = HashTable()
    table.insert(41,'apple')
    table.insert(93,'banana')
    table.insert(13,'tangerine')
    print str(table.table)
    print str(table.get(13))
    print str(table.get(51))
    print str(table.remove(13))
    print str(table.remove(51))
    print str(table.table)
    # ways of increasing the hash in case it is too full (via max or via a load factor) to avoid collisions
    # 1. double the table
    #   - Hash-tables could not claim "amortized constant time insertion" if, for instance, the resizing was 
    #   by a constant increment. In that case the cost of resizing (which grows with the size of the hash-table) 
    #   would make the cost of one insertion linear in the total number of elements to insert. Because resizing 
    #   becomes more and more expensive with the size of the table, it has to happen "less and less often" to 
    #   keep the amortized cost of insertion constant.
    # 2. open adressing
    #   - An open-addressing hash table indexes into an array of pointers to pairs of (key, value). You use the key's 
    #   hash value to work out which slot in the array to look at first. If more than one key in the hash table has the 
    #   same hash, then you use some scheme to decide on another slot to look in instead.

    # - The downside of chained hashing is having to follow pointers in order to search linked lists. The upside is that 
    # chained hash tables only get linearly slower as the load factor (the ratio of elements in the hash table to the 
    # length of the bucket array) increases, even if it rises above 1.
    # - Open-addressing is usually faster than chained hashing when the load factor is low because you don't have to follow 
    # pointers between list nodes. It gets very, very slow if the load factor approaches 1, because you end up usually 
    # having to search through many of the slots in the bucket array before you find either the key that you were looking 
    # for or an empty slot. Also, you can never have more elements in the hash table than there are entries in the bucket 
    # array.

    # load factor: measure of how full the hash table is allowed to get before its capacity is automatically increased.
if __name__ == "__main__":
    result = question1("thing\n")
    result = question2("abc")
    result = question3("abc", "bca")
    result = question3("12 34", " 1234", easy_way=False)
    result = question4("Mr John Smith", easy_way=False)
    result = question5("aabcccccaaa")
    result = question6([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = question7([[0, 2, 3], [4, 5, 0], [7, 8, 9]])
    result = question8("waterbottle", "erbottlewat")
    result = question1_alt("thing\n\n")
    result = question2_alt("abcd")
    # print str(result)
    test_hash_table()