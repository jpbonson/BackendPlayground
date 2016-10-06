# The *args and **keywordargs forms are used for passing lists of arguments and dictionaries of arguments, respectively. 
def printlist(*args):
    for x in args:
        print x
printlist(1, 2, 3, 4, 5)

def printdict(**kwargs):
    print repr(kwargs)
printdict(john=10, jill=12, david=15)


# Global Interpreter Lock (GIL)
# - In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads 
# from executing Python bytecodes at once. This lock is necessary mainly because CPython's memory management 
# is not thread-safe.
# - The GIL is controversial because it prevents multithreaded CPython programs from taking full advantage 
# of multiprocessor systems in certain situations.
# - CPython, the most widely used implementation of Python
# - The GIL in cPython does not protect your program state. It protects the interpreter's state.


# ord("a") is 97
# chr(97) is "a"


# bit manipulation in python
int('11', 2) # 3
int('0xff',16) # 255
a = 2 # 10
b = 3 # 11
a & b # 2
a | b # 3
a << 1 # 4
a >> 1 # 1
a ^ b # 1 (XOR)
~b # -4 (This is the same as -b-1)
a ^ int('11', 2) # logical negation
hex(15) # 0xf

# 1 byte = 8 bits

# Unicode string
# -*- coding: utf-8 -*-
s = "Flügel"
u = u"Flügel"
new_u = new_s.decode('utf_8')
# When strings contain non-ASCII characters, they can either be 8-bit strings (encoded strings), or they can be Unicode strings (decoded strings).
# To print or display some strings properly, they need to be decoded (Unicode strings).

# threads and process in python
# https://docs.python.org/2/library/threading.html (threads, semaphores, locks...)
# https://docs.python.org/2/library/multiprocessing.html (process, queue, pipes, lock...)
threading.Thread(group=None, target=None, name=None, args=(), kwargs={})
multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool # apply_async, map_async

# iPython notebook

if __name__ == "__main__":

# examples of array manipulation
a = [1,2,3,4,5]
a[:1] # [1]
a[1:] # [2,3,4,5]
a[1:3] # [2,3]
a[:-1] # [1,2,3,4]
a[-1:] # [5]
a[-1] # 5
range(1,5) = [1,2,3,4]
range(5) = [0,1,2,3,4]

# example with join and split
a = ['a', 'b', 'c']
''.join(a) # 'abc'
b = 'a b c'
b.split(' ') # ['a', 'b', 'c']

# String join is significantly faster then concatenation. Why? 
# Strings are immutable and can't be changed in place. To alter one, a new representation needs 
# to be created (a concatenation of the two).
# string1 += string2 vs ''.join(['string1', 'string2'])

# generator vs list comprehension
(x*2 for x in range(256)) # Generator expression
[x*2 for x in range(256)] # List comprehension
# - the list comprehension will create the entire list in memory first while the generator 
# expression will create the items on the fly, so you are able to use it for very large 
# (and also infinite!) sequences.
# - or using yield
# - Use list comprehensions when the result needs to be iterated over multiple times, or 
# where speed is paramount. Use generator expressions where the range is large or infinite.
# - use list comprehension if you want to store and use the generated results, and use list operations


# map/reduce/filter (python):
f = lambda x, y : x + y
f(1,1) # 2

Celsius = [39.2, 36.5, 37.3, 37.8]
Fahrenheit = map(lambda x: (float(9)/5)*x + 32, Celsius)
print Fahrenheit # [102.56, 97.700000000000003, 99.140000000000001, 100.03999999999999]

a = [1,2,3,4]
b = [17,12,11,10]
map(lambda x,y:x+y, a,b) # [18, 14, 14, 14]

fib = [0,1,1,2,3,5,8,13,21,34,55]
result = filter(lambda x: x % 2 == 0, fib)
print result # [0, 2, 8, 34]

reduce(lambda x,y: x+y, [47,11,42,13]) # 113
f = lambda a,b: a if (a > b) else b
>>> reduce(f, [47,11,42,102,13]) # 102

# shallow and deep copy
# A shallow copy constructs a new compound object and then (to the extent possible) inserts references into it to the objects found in the original.
# A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.
# http://stackoverflow.com/questions/17246693/what-exactly-is-the-difference-between-shallow-copy-deepcopy-and-normal-assignm
import copy
d = copy.copy(c)
d = copy.deepcopy(c)

# complexities:
# https://wiki.python.org/moin/TimeComplexity
# https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt
# https://wiki.python.org/moin/PythonSpeed

# comparable: def __eq__(self, other):

# convert list to set: O(n) (worst case)

# http://google.github.io/styleguide/pyguide.html