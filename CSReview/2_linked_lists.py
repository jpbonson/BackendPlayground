class Node():
    """
    Singly linked list

    Improvement:
    - "Runner" technique, use two points instead of one (one slow, and one fast)

    Note:
    - Usually linked list problems rely on recursion
    - Remember that recursive algorithms take at least 0(n) space, where n is the depth of the recursive call.
    """
    def __init__(self, data):
        self.next = None
        self.data = data

def append_to_tail(head, data):
    end = Node(data)
    n = head
    while n.next is not None:
        n = n.next
    n.next = end

def delete_node(head, data):
    if head.data == data:
        return head.next
    n = head
    while n.next is not None:
        if n.next.data == data:
            n.next = n.next.next
            return head
        n = n.next
    return head

def linked_list_to_array(node):
    data = []
    n = node
    data.append(n.data)
    while n.next is not None:
        n = n.next
        data.append(n.data)
    return data

def create_linked_list(array):
    if not isinstance(array, list) or len(array) == 0:
        raise ValueError("some message")
    head = Node(array[0])
    for value in array[1:]:
        append_to_tail(head, value)
    return head        

def test_linked_list():
    head = Node(1)
    append_to_tail(head, 2)
    append_to_tail(head, 3)
    assert linked_list_to_array(head) == [1,2,3]
    head = delete_node(head, 3)
    assert linked_list_to_array(head) == [1,2]
    append_to_tail(head, 4)
    append_to_tail(head, 5)
    assert linked_list_to_array(head) == [1,2,4,5]
    head = delete_node(head, 1)
    assert linked_list_to_array(head) == [2,4,5]
    head = delete_node(head, 4)
    assert linked_list_to_array(head) == [2,5]
    head = create_linked_list([1,2,3])
    assert linked_list_to_array(head) == [1,2,3]

# 1. Write code to remove duplicates from an unsorted linked list.
# Extra: How would you solve this problem if a temporary buffer is not allowed?
def question1(head):
    """
    Test Cases:
    - None: error
    - [1,2,3,4,5]: [1,2,3,4,5]
    - [3,1,4,2,5]: [3,1,4,2,5]
    - [1,2,2,3]: [1,2,3]
    - [4,4,2,1]: [4,2,1]
    - [3,6,7,5,5]: [3,6,7,5]
    - [5,5,5,5,5]: [5]
    - [3,3,2,2]: [3,2]

    Assumption:
    - list of anything

    Extra:
    - To implement the extra, for each node remove all the future nodes that have the same data (O(n**2))

    Time Complexity: O(n)
    Space Complexity: O(e)
    """
    if head is None or not isinstance(head, Node):
        raise ValueError("some message")

    exists = set()
    n = head
    exists.add(n.data)
    while n.next is not None:
        if n.next.data not in exists:
            exists.add(n.next.data)
            n = n.next
        else:
            n.next = n.next.next
    return linked_list_to_array(head)        

# 2. Implement an algorithm to find the kth to last element of a singly linked list.
def question2(k, head):
    """
    Test Cases:
    - None or not a linked list: error
    - 0, [0,1,2,3,4,5]: 5
    - 1, [0,1,2,3,4,5]: 4
    - 10, [0,1,2]: return nothing

    Assumption:
    - the list size is unknown

    Alternative:
    - use two pointers, a regular pointer and a 'delayed pointer', that starts after k positions (space: O(1))

    Time Complexity: O(n)
    Space Complexity: O(n) # due to it being recursive
    """
    def to_the_kth_element(k, node):
        if node.next is not None:
            index, data = to_the_kth_element(k, node.next)
            if data is not None:
                return (index, data)
            else:
                index += 1
                if k == index:
                    data = node.data
                return (index, data)
        else:
            data = None
            if k == 0:
                data = node.data
            return (0, data)

    if head is None or not isinstance(head, Node):
        raise ValueError("some message")

    return to_the_kth_element(k, head)

def question2_alt(k, head):
    n = head
    delayed = head
    position = 0
    while n.next is not None:
        if position >= k:
            delayed = delayed.next
        n = n.next
        position += 1
    return delayed.data

# 3. Implement an algorithm to delete a node in the middle of a singly linked list,
# given only access to that node.
def question3():
    """
    Test Cases:
    - c, [a,b,c,d,e]: [a,b,d,e]

    Assumption:
    - the node indeed exists and is not the start nor the end of the list
    """
    def execute(node):
        node.data = node.next.data
        node.next = node.next.next

    head = create_linked_list([0,1,2,3,4])
    node = head.next.next
    execute(node)
    return linked_list_to_array(head)

# 4. Write code to partition a linked list around a value x, such that all nodes less than
# x come before all nodes greater than or equal to x.
def question4(x, head):
    """
    Test Cases:
    - 2, [0,1,2,3,4]: (0,1)+(2,3,4)
    - 3, [1,2,5,6,3,0,4]: (0,1,2)+(3,4,5,6)

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = head
    tail = None
    while n.next is not None:
        if n.next.data >= x:
            if tail is None:
                tail = Node(n.next.data)
            else:
                append_to_tail(tail, n.next.data)
            n.next = n.next.next
        else:
            n = n.next

    n = head
    while n.next is not None:
        n = n.next
    n.next = tail

    return linked_list_to_array(head)

# 5. You have two numbers represented by a linked list, where each node contains a
# single digit. The digits are stored in reverse order, such that the first digit is at the
# head of the list. Write a function that adds the two numbers and returns the sum
# as a linked list.
# Extra: Suppose the digits are stored in forward order. Repeat the above problem.
def question5(head1, head2):
    """
    Test Cases:
    - [7,1,6] + [5,9,2] (ie. 617 + 295): [2,1,9] (ie. 912)
    - [7,1] + [5,9,2] (ie. 17 + 295): [2,1,6] (ie. 312)

    Extra:
    - always have a reference to the last node in r, so that if the sum has an extra its data can be updated
    - check if the lists have the same size, if they don't have, use a delayed pointer

    Alternative:
    - use recursion

    Time Complexity: O(n)
    Space Complexity: O(r)
    """
    n1 = head1
    n2 = head2
    r = None
    extra = 0
    while n1 is not None or n2 is not None:
        result = 0
        if n1 is not None:
            result += n1.data
            n1 = n1.next
        if n2 is not None:
            result += n2.data
            n2 = n2.next
        result += extra
        if result > 9:
            extra = 1
        else:
            extra = 0
        result = result % 10
        if r is None:
            r = Node(result)
        else:
            append_to_tail(r, result)
    return linked_list_to_array(r)

# 6. Given a circular linked list, implement an algorithm which returns the node at
# the beginning of the loop
# DEFINITION
# Circular linked list: A (corrupt) linked list in which a node's next pointer points
# to an earlier node, so as to make a loop in the linked list.
def question6():
    """
    Test Cases:
    - ['a', 'b', 'c', 'd', 'e', 'c']: 'c'
    - ['a', 'b', 'c', 'd', 'e']: None

    Alternative:
    - use a regular and a fast pointer (double speed) and check if they collide (space: O(1))
    - to get the corrupt node, move the regular pointer to the head and then move both the regular and the 
    fast pointer at the same speed until they meet (space: O(1))

    Time Complexity: O(n)
    Space Complexity: O(e)
    """
    def execute(head):
        n = head
        exists = set()
        while n is not None:
            if n not in exists:
                exists.add(n)
            else:
                return n
            n = n.next
        return None
    head = create_linked_list(['a', 'b', 'c', 'd', 'e'])
    corrupted_node = head.next.next
    n = corrupted_node
    while n.next is not None:
        n = n.next
    n.next = corrupted_node

    result = execute(head)
    if result is not None:
        return result.data
    return result

# 7. Implement a function to check if a linked list is a palindrome
from collections import deque
def question7(head):
    """
    Test Cases:
    - [5, 1, 1, 5]: True
    - [5, 1, 2, 1, 5]: True
    - [1, 2, 3]: False

    Alternative:
    - 1) reverse list and compare it half-way to the original list
    - 2) recursive (if the length of the list is known)

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # iterative (regular and fast pointer)
    n_regular = head
    n_fast = head
    skip_last = False
    stack = deque()
    while n_regular is not None:
        if n_fast is None:
            if skip_last:
                stack.pop()
                skip_last = False
            if stack.pop() != n_regular.data:
                return False
        else:
            stack.append(n_regular.data)

        n_regular = n_regular.next
        if n_fast is not None:
            if n_fast.next is not None:
                n_fast = n_fast.next.next
            else:
                skip_last = True
                n_fast = n_fast.next
    return True

if __name__ == "__main__":
    test_linked_list()

    result = question1(create_linked_list([3,3,2,2]))
    result = question2(2, create_linked_list([0,1,2,3,4,5]))
    result = question2_alt(2, create_linked_list([0,1,2,3,4,5]))
    result = question3()
    result = question4(3, create_linked_list([1,2,5,6,3,0,4]))
    result = question5(create_linked_list([7,1,6]), create_linked_list([5,9,2]))
    result = question6()
    result = question7(create_linked_list([5, 1, 3, 1, 5]))
    print str(result)