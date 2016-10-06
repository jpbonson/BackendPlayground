# Dynamic Programming

# Now that we have our recurrence equation, we can right way start coding the recursion. Wait.., does it 
# have over-lapping subproblems ?  YES. Is the optimal solution to a given input depends on the optimal 
# solution of its subproblems ? Yes... Bingo ! its DP :) So, we just store the solutions  to the subproblems 
# we solve and use them later on, as in memoization.. or we start from bottom and move up till the given n, as in dp.

# Dynamic programming is a method for efficiently solving a broad range of search and optimization problems 
# which exhibit the characteristics of overlappling subproblems and optimal substructure. 
# - A problem is said to have optimal substructure if the globally optimal solution can be constructed from 
# locally optimal solutions to subproblems.
# - eg.: Let's say we have a collection of objects called A. For each object o in A we have a "cost," c(o). 
# Now find the subset of A with the maximum (or minimum) cost, perhaps subject to certain constraints.

# Memoization is a term describing an optimization technique where you cache previously computed results, and return 
# the cached result when the same computation is needed again.
# Dynamic programming is a technique for solving problems recursively and is applicable when the computations of the 
# subproblems overlap.
# - Dynamic programming is typically implemented using tabulation, but can also be implemented using memoization. So as 
# you can see, neither one is a "subset" of the other.
# - When you solve a dynamic programming problem using tabulation you solve the problem "bottom up", i.e., by solving 
# all related sub-problems first, typically by filling up an n-dimensional table. Based on the results in the table, 
# the solution to the "top" / original problem is then computed.
# - If you use memoization to solve the problem you do it by maintaining a map of already solved sub problems. You do 
# it "top down" in the sense that you solve the "top" problem first (which typically recurses down to solve the 
# sub-problems).
# - If all subproblems must be solved at least once, a bottom-up dynamic-programming algorithm usually outperforms a 
# top-down memoized algorithm by a constant factor (No overhead for recursion and less overhead for maintaining table)
# - If some subproblems in the subproblem space need not be solved at all, the memoized solution has the advantage of 
# solving only those subproblems that are definitely required

# Steps for Solving DP Problems
# 1. Define subproblems
# 2. Write down the recurrence that relates subproblems
# 3. Recognize and solve the base cases

# Example
# Problem: given n, find the number of different ways to write
# n as the sum of 1, 3, 4
# Example: for n = 5, the answer is 6

# Example: The Knapsack Problem

import time

# Example of recursion WITHOUT overlappling subproblems
def factorial(n):
    if n == 0: return 1
    return n*factorial(n-1)

# Example of recursion WITH overlappling subproblems O(c**n)
def fib(n):
    if n == 0: return 0
    if n == 1: return 1
    return fib(n-1) + fib(n-2)

# Example of dynamic programming O(n)
def fib2(n):
    n2, n1 = 0, 1
    for i in range(n-2): 
        n2, n1 = n1, n1 + n2
    return n2+n1

# Example: coin change, using recursion
def make_change_recursion(coinValueList,change):
    minCoins = change
    if change in coinValueList:
        return 1
    else:
        for i in [c for c in coinValueList if c <= change]:
            numCoins = 1 + make_change_recursion(coinValueList,change-i)
            if numCoins < minCoins:
                minCoins = numCoins
    return minCoins

# Example: coin change, using dynamic programming (memoization)
def make_change_dp_mem(coinValueList,change,knownResults):
    minCoins = change
    if change in coinValueList:
        knownResults[change] = 1
        return 1
    elif knownResults[change] > 0:
        return knownResults[change]
    else:
        for i in [c for c in coinValueList if c <= change]:
            numCoins = 1 + make_change_dp_mem(coinValueList, change-i, knownResults)
            if numCoins < minCoins:
                minCoins = numCoins
                knownResults[change] = minCoins
    return minCoins

# Example: coin change, using dynamic programming (tabulation)
def make_change_dp_tab(coinValueList,change,minCoins):
    for cents in range(1, change+1):
        coinCount = cents
        for j in [c for c in coinValueList if c <= cents]:
            new_count = minCoins[cents-j]+1
            if new_count < coinCount:
                coinCount = new_count
        minCoins[cents] = coinCount
    return minCoins[change]

def test_make_change():
    change = 23
    times = []
    start = time.clock()
    assert make_change_recursion([1,5,10,25], change) == 5
    times.append(time.clock() - start)
    start = time.clock()
    assert make_change_dp_mem([1,5,10,25],change, [0]*(change+1)) == 5
    times.append(time.clock() - start)
    start = time.clock()
    assert make_change_dp_tab([1,5,10,25],change, [0]*(change+1)) == 5
    times.append(time.clock() - start)
    # print str(times) # [0.0003203808158823212, 4.194400653612562e-05, 2.097200326806281e-05]

######################

# 1. A child is running up a staircase with n steps, and can hop either 1 step, 2 steps, or
# 3 steps at a time. Implement a method to count how many possible ways the child
# can run up the stairs.
def question1(n):
    """
    Idea:
    - use recursion and/or dynamic programming

    ways_for_steps[1] = 1
    ways_for_steps[2] = 2
    ways_for_steps[3] = 4
    ways_for_steps[4] = 7
    """
    def recursion(n): # O(3**n)
        if n < 0:
            return 0
        if n == 0:
            return 1
        return recursion(n-1) + recursion(n-2) + recursion(n-3)
    return recursion(n)

def question1_alt(n):
    def recursion(n, saved_states):
        if n < 0:
            return 0
        if n == 0:
            return 1
        if saved_states[n] != -1:
            return saved_states[n]
        else:
            saved_states[n] = (recursion(n-1, saved_states) + 
                recursion(n-2, saved_states) + 
                recursion(n-3, saved_states))
            return saved_states[n]
    saved_states = [-1] * (n+1)
    return recursion(n, saved_states)

# 2. Imagine a robot sitting on the upper left comer of an X by Y grid. The robot can only
# move in two directions: right and down. How many possible paths are there for the
# robot to go from (0, 0) to (X, Y) ?
def question2(X, Y):
    """

    """
    def recursion(X, Y, paths, current_path):
        if X == 0 and Y == 0:
            paths.append(list(current_path))
            current_path.pop()
            return 1
        if X < 0 or Y < 0:
            current_path.pop()
            return 0
        return recursion(X-1, Y, paths, current_path+[(X-1, Y)]) + recursion(X, Y-1, paths, current_path+[(X, Y-1)])
    paths = []
    return (recursion(X, Y, paths, [(X, Y)]), paths)

# 3. A magic index in an array A[l.. .n-l] is defined to be an index such that A[i] =
# i. Given a sorted array of distinct integers, write a method to find a magic index, if
# one exists, in array A.
# FOLLOW UP
# What if the values are not distinct?
# A.: Use a binary search tree
def question3(array):
    """
    [-1,1,3,5,7]
    [0,1,2,3,4]
    """
    def recursion(array, start, end):
        if len(array) == 0:
            return None
        mid = (start+end)/2
        if array[mid] == mid:
            return array[mid]
        if mid < array[mid]:
            return recursion(array, start, mid-1)
        else:
            return recursion(array, mid+1, end)
    return recursion(array, 0, len(array)-1)

# 4. Write a method to return all subsets of a set.
def question4(some_set):
    def recursion(some_set):
        if len(some_set) == 0:
            return [[]]
        return [[some_set[0]] + x for x in recursion(some_set[1:])] + recursion(some_set[1:])
    return recursion(some_set)

# 5. Write a method to compute all permutations of a string
def question5(some_string):
    """
    - with or without repetition?
    - order matters
    """
    def recursion(some_string, found_perm):
        if len(some_string) == 0:
            return [""]
        permutations = []
        first_char =  some_string[0]
        remainder = some_string[1:]
        perm_remainder = recursion(remainder, found_perm)
        for perm in perm_remainder:
            for index in range(len(perm)+1):
                new_perm = perm[:index]+first_char+perm[index:]
                if new_perm not in found_perm:
                    permutations.append(new_perm)
                    found_perm[new_perm] = True
                else:
                    break
        return permutations
    found_perm = {}
    return recursion(some_string, found_perm)

# 6. Implement an algorithm to print all valid (i.e., properly opened and closed) combinations
# ofn-pairs of parentheses.
# A.: recursion

# 7. Implement the "paint fill" function that one might see on many image editing
# programs. That is, given a screen (represented by a two-dimensional array of colors),
# a point, and a new color, fill in the surrounding area until the color changes from the
# original color.
# A.: recursion + check if a point haven't been painted already

# 8. Given an infinite number of quarters (25 cents), dimes (10 cents), nickels (5 cents)
# and pennies (1 cent), write code to calculate the number of ways of representing n
# cents.
next_demon = {25:10, 10:5, 5:1, 1:1}
def question8(cents): # wrong
    def recursion(cents):
        if cents < 0:
            return 0
        if cents == 0:
            return 1
        return recursion(cents-1) + recursion(cents-5) + recursion(cents-10) + recursion(cents-25)
    return recursion(cents)

# public int makeChange(int n, int denom) {
# 2 int next_denom = 0;
# 3 switch (denom) {
# 4 case 25:
# 5 next_denom = 10;
# 6 break;
# 7 case 10:
# 8 next_denom = 5;
# 9 break;
# 10 case 5:
# 11 next_denom = 1;
# 12 break;
# 13 case 1:
# 14 return 1;
# 15 }
# 16
# 17 int ways = 0;
# 18 for (int i = 0; i * denom <= n; i++) {
# 19 ways += makeChange(n - i * denom, next_denom);
# 26 }
# 21 return ways;
# 22 }
# System.out.writeln(makeChange(100, 25));

# 9. Write an algorithm to prim all ways of arranging eight queens on an 8x8 chess
# board so that none of them share the same row, column or diagonal. In this case,
# "diagonal" means all diagonals, not just the two that bisect the board.
# ...

# 10. You have a stack of n boxes, with widths w., heights l\ and depths dr The boxes
# cannot be rotated and can only be stacked on top of one another if each box in the
# stack is strictly larger than the box above it in width, height, and depth. Implement
# a method to build the tallest stack possible, where the heigh t of a stack is the sum of
# the heights of each box.
# ...

# 11. Given a boolean expression consisting of the symbols 0,1, &, /, and A, and a desired
# boolean result value result, implement a function to count the number of ways of
# parenthesizing the expression such that it evaluates to resuL t.
# ...

if __name__ == "__main__":
    test_make_change()
    result = question1(5)
    result = question1_alt(5)
    result = question2(2, 2)
    result = question4([1,2,3])
    result = question5("casa")
    result = question8(6)
    result = question3([-2,-1,0,2,4])
    print str(result)