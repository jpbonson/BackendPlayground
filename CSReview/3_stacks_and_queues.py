class Node():
    def __init__(self, data):
        self.next = None
        self.data = data

class Stack():

    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data):
        temp = Node(data)
        temp.next = self.top
        self.top = temp
        self.size += 1

    def pop(self):
        if self.top is not None:
            item = self.top.data
            self.top = self.top.next
            self.size -= 1
            return item
        return None

    def peek(self):
        return self.top.data

    def __repr__(self):
        n = self.top
        data = []
        while n is not None:
            data.append(n.data)
            n = n.next
        return str(data)

class Queue():

    def __init__(self):
        self.first = None
        self.last = None

    def enqueue(self, data):
        if self.first is None:
            self.last = Node(data)
            self.first = self.last
        else:
            self.last.next = Node(data)
            self.last = self.last.next

    def dequeue(self):
        if self.first is not None:
            data = self.first.data
            self.first = self.first.next
            return data
        return None

# 1. Describe how you could use a single array to implement three stacks.
# A: Divide the array in three predefined sizes, so each stack starts at 0, s1, and s2
# Initialize all positions to some value, like None
# Use 'insert' and 'remove' to add and pop data from the stacks considering 0, s1, and s2 as the initial indeces
# Use auxiliar variables to keep track of the sizes of the stacks

# 2. How would you design a stack which, in addition to push and pop, also has a
# function min which returns the minimum element? Push, pop and min should
# all operate in O(1) time.
# A: Add an attribute to the class Node that will keep track of the min value of the nodes under it

# 3. Imagine a (literal) stack of plates. If the stack gets too high, it might topple.
# Therefore, in real life, we would likely start a new stack when the previous stack
# exceeds some threshold. Implement a data structure SetOf Stacks that mimics
# this. SetOfStacks should be composed of several stacks and should create a
# new stack once the previous one exceeds capacity. SetOf Stacks. push() and
# SetOfStacks. pop() should behave identically to a single stack (that is, popO
# should return the same values as it would if there were just a single stack).
# Extra: Implement a function popAt(int index) which performs a pop operation on
# a specific sub-stack.
class SetOfStacks():

    def __init__(self, limit):
        self.limit = limit
        self.stacks = [Stack()]

    def push(self, data):
        if self.stacks[-1].size == self.limit:
            self.stacks.append(Stack())
        self.stacks[-1].push(data)

    def pop(self):
        if len(self.stacks) == 1 and self.stacks[-1].size == 0:
            return None
        result = self.stacks[-1].pop()
        if self.stacks[-1].size == 0 and len(self.stacks) > 1:
            self.stacks.pop()
        return result

    def pop_at(self, index):
        if len(self.stacks)-1 < index:
            raise IndexError("some message")
        if self.stacks[index].size == 0:
            return None
        result = self.stacks[index].pop()
        if self.stacks[index].size == 0 and len(self.stacks) > 1:
            self.stacks.pop(index)
        return result

    def __repr__(self):
        return str(self.stacks)+", limit: "+str(self.limit)

def question3():
    """
    Assumption:
    - 'pop_at' doesn't need to rebalance all stacks
    """
    set_of_stacks = SetOfStacks(3)
    set_of_stacks.push(1)
    set_of_stacks.push(1)
    set_of_stacks.push(1)
    print str(set_of_stacks)
    set_of_stacks.push(1)
    print str(set_of_stacks)
    set_of_stacks.pop()
    print str(set_of_stacks)
    set_of_stacks.push(1)
    set_of_stacks.push(1)
    set_of_stacks.push(1)
    set_of_stacks.push(1)
    print str(set_of_stacks)
    set_of_stacks.pop_at(1)
    print str(set_of_stacks)

# 4. In the classic problem of the Towers of Hanoi, you have 3 towers and N disks of
# different sizes which can slide onto any tower. The puzzle starts with disks sorted
# in ascending order of size from top to bottom (i.e., each disk sits on top of an
# even larger one). You have the following constraints:
# (1) Only one disk can be moved at a time.
# (2) A disk is slid off the top of one tower onto the next tower.
# (3) A disk can only be placed on top of a larger disk.
# Write a program to move the disks from the first tower to the last using stacks.
from collections import deque
def question4(n):
    """ -> [], [], []
    Test Cases:
    - [2,1], [], [] -> [2], [1], [] -> [], [1], [2] -> [], [], [2,1]
    - [3,2,1], [], [] -> [3,2], [], [1] -> [3], [2], [1] -> [3], [2,1], [] -> [], [2,1], [3] -> 
        [1], [2], [3] -> [1], [], [3,2] -> [], [], [3,2,1]
    - [4,3,2,1], [], [] -> [4,3,2], [1], [] -> [4,3], [1], [2] -> [4,3], [], [2,1] -> [4], [3], [2,1] -> 
        [4,1], [3], [2] -> [4,1], [3,2], [] -> [4], [3,2,1], [] -> [], [3,2,1], [4] -> ...

    Notes:
    - Remember that the labels of Tower 2 and Tower 3 aren't important. They're equivalent
    towers. So, moving disks to Tower 3 with Tower 2 serving as a buffer is equivalent to
    moving disks to Tower 2 with Tower 3 serving as a buffer.
    - It is a natural recursive algorithm.
    """
    def moveDisks(n, origin, buffer_stack, destination):
        if n <= 0: # base case
            return
        moveDisks(n - 1, origin, destination, buffer_stack)
        if len(origin) > 0:
            value = origin.pop()
            destination.append(value)
            # print "from: "+str(origin)+" to "+str(destination)+", n: "+str(n)
        moveDisks(n - 1, buffer_stack, origin, destination)

    stack1 = deque(reversed(range(1, n+1)))
    # print "start: "+str(stack1)
    stack2 = deque()
    stack3 = deque()
    moveDisks(n, stack1, stack2, stack3)
    return str(stack1)+", "+str(stack2)+", "+str(stack3)

# 5. Implement a MyQueue class which implements a queue using two stacks.
# A:
# inputs: abcde
# stack1: [last] edcba [first]
# stack2: [last] abcde [first]
# Improvement: lazy reversion of elements

# 6. Write a program to sort a stack in ascending order (with biggest items on top).
# You may use at most one additional stack to hold items, but you may not copy
# the elements into any other data structure (such as an array). The stack supports
# the following operations: push, pop, peek, and isEmpty.
# A: Use the origin stack as a buffer and use a temporary variable
# stack1: [last] [2,3,1], stack2: [last] [], temp: None
# stack1: [last] [3,1], stack2: [last] [2], temp: None
# stack1: [last] [1], stack2: [last] [2], temp: 3
# stack1: [last] [2,1], stack2: [last] [], temp: 3
# stack1: [last] [2,1], stack2: [last] [3], temp: None
# stack1: [last] [1], stack2: [last] [2,3], temp: None
# stack1: [last] [], stack2: [last] [1,2,3], temp: None

# 7. An animal shelter holds only dogs and cats, and operates on a strictly "first in,
# first out" basis. People must adopt either the "oldest" (based on arrival time) of
# all animals at the shelter, or they can select whether they would prefer a dog or
# a cat (and will receive the oldest animal of that type). They cannot select which
# specificanimal they would like. Create the data structures to maintain this system
# and implement operations such as enqueue, dequeueAny, dequeueDog and
# dequeueCat.You may use the built-in LinkedList data structure.
class Shelter():

    COUNTER = 0

    def __init__(self):
        self.cats = deque()
        self.dogs = deque()

    def enqueue(self, animal_type):
        if animal_type == 'cat':
            self.cats.append(Shelter.COUNTER)
        if animal_type == 'dog':
            self.dogs.append(Shelter.COUNTER)
        Shelter.COUNTER += 1

    def dequeueAny(self):
        if self.cats[0] <= self.dogs[0]:
            return self.cats.popleft()
        else:
            return self.dogs.popleft()

    def dequeueCat(self):
        return self.cats.popleft()

    def dequeueDog(self):
        return self.dogs.popleft()

    def __str__(self):
        return "cats: "+str(self.cats)+", dogs: "+str(self.dogs)

def question7():
    shelter = Shelter()
    print str(shelter)
    shelter.enqueue('cat')
    shelter.enqueue('cat')
    shelter.enqueue('dog')
    shelter.enqueue('dog')
    shelter.enqueue('cat')
    shelter.enqueue('dog')
    print str(shelter)
    print str(shelter.dequeueAny())
    print str(shelter.dequeueCat())
    print str(shelter.dequeueDog())
    print str(shelter)

if __name__ == "__main__":
    # question3()
    # print str(question4(2))
    question7()