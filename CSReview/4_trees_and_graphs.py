# Notes: The worst case and average case time may vary wildly, and we must evaluate both aspects of any algorithm.

# TREES:

# - Binary Tree vs. Binary Search Tree
#   - Binary Tree: Just a tree where each node may have two subtrees
#   - Binary Search Tree:
#       - the left nodes must be smaller than the key, that is smaller than the right nodes
#       - useful for sorting and search algorithms

# - Full and Complete
#   - trees in which all leaves are at the bottom of the tree, and all non-leaf nodes have exactly two children
#   - rare trees, a tree must have exactly 2**n - 1 nodes to meet this condition

# - Binary Tree Traversal
#   eg.: 3 -> [2 -> [1, _], 4 -> [_, 5]]
#   - in-order:
#       1. Traverse the left subtree, i.e., call in-order (left-subtree)
#       2. Visit the root.
#       3. Traverse the right subtree, i.e., call in-order (right-subtree)
#       eg.: 1 2 4 5 3 (if it is a binary search tree, the result is sorted by the keys)
#   - pre-order:
#       1. Visit the root.
#       2. Traverse the left subtree, i.e., call pre-order (left-subtree)
#       3. Traverse the right subtree, i.e., call pre-order (right-subtree)
#       eg.: 3 2 1 4 5
#   - post-order:
#       1. Traverse the left subtree, i.e., call post-order (left-subtree)
#       2. Traverse the right subtree, i.e., call post-order (right-subtree)
#       3. Visit the root.
#       eg.: 1 2 5 4 3

# - Tree Balancing:
#   - overview of how to balance a tree:
#       - need to re-balance the tree on each insert and delete, which will make this data 
#           structure more difficult to maintain
#       - searching into it will be significantly faster
#           - from O(n) to O(log(n)) in worst-case scenario, the average is O(log n) for both of them
#       - optimization: bulk insert and bulk delete (ie. only balance tree after a few inputs)
#       - The height of a node is the length of the longest downward path to a leaf from that node. 
#   - Specification: A binary tree is height-balanced if 
#       (1) it is empty, or 
#       (2) its left and right children are height-balanced and the height of the left tree is 
#           within X (a predefined value) of the height of the right tree.
#       - A rotation of a binary tree transforms it so that its inorder-walk key ordering is preserved.
#       - AVL Trees:
#           - performance: O(log n) search, insertion, and deletion times (average and worst case)
#           - space: O(n)
#           - X = 1
#           - if after an insertion or deletion the tree is unbalanced, use rotations to rebalance it (O(log n))
#           - each node has an aditional attribute height, that is updated after insert/delete
#           - for lookup-intensive applications, AVL trees are faster than red-black trees because they are more rigidly balanced
#       - Red-Black Trees:
#           - each node of the binary tree has an extra bit for its color (red or black)
#           - these color bits are used to ensure the tree remains approximately balanced during insertions and deletions
#           - when the tree is modified, the new tree is rearranged and repainted to restore the coloring properties (O(log n))
#           - the coloring constrain how unbalanced the tree can become in the worst case
#           - the constraints enforce a critical property of red-black trees:
#               - the path from root to farthest leaf is no more than twice as long as the path from root to nearest leaf

# - Tries
#   - is a tree where each vertex represents a single word or a prefix
#   - the descendants of a node have a common prefix of the string associated with that node
#   - the root is associated with the empty string
#   - values are not necessarily associated with every node (tend to be associated with leaves, and some inner nodes)
#   - applications: auto complete, text corrector
#       - faster than set and hash for these applications + enables: find similar words, common prefix, character missing, etc.
#   - the insertion and finding of a word in a trie can be done in O(L) time (where L is the word's length)
#   - more: https://www.topcoder.com/community/data-science/data-science-tutorials/using-tries/

# - Binary Search Tree Operations:

class TreeNode():
    def __init__(self, key, parent = None):
        self.left = None
        self.right = None
        self.key = key
        self.parent = parent

    def __repr__(self):
        return str(self.key)+" -> ["+str(self.left)+", "+str(self.right)+"]"

#   - Search
def search_recursively(node, key):
    if node is None or node.key == key:
        return node
    elif key < node.key:
        return search_recursively(node.left, key)
    else:  # key > node.key
        return search_recursively(node.right, key)

def search_iteratively(node, key): 
    current_node = node
    while current_node is not None:
        if key == current_node.key:
            return current_node
        elif key < current_node.key:
            current_node = current_node.left
        else:  # key > current_node.key:
            current_node = current_node.right
    return None

#   - Insert
def insert(node, key):
    if node is None:
        return TreeNode(key)
    else:
        if node.key > key:
            if node.left is None:
                node.left = TreeNode(key, parent = node)
            else:
                insert(node.left, key)
        else:
            if node.right is None:
                node.right = TreeNode(key, parent = node)
            else:
                insert(node.right, key)

#   - Remove
def remove(node, key):

    def find_min(node):   # Gets minimum node in a subtree
        current_node = node
        while current_node.left:
            current_node = current_node.left
        return current_node

    def replace_node_in_parent(node, new_node):
        if node.parent:
            if node == node.parent.left:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
        if new_node:
            new_node.parent = node.parent

    if key < node.key:
        remove(node.left, key)
    elif key > node.key:
        remove(node.right, key)
    else: # delete the key
        if node.left and node.right:
            successor = find_min(node.right)
            node.key = successor.key
            remove(successor, successor.key)
        elif node.left:
            replace_node_in_parent(node, node.left)
        elif node.right:
            replace_node_in_parent(node, node.right)
        else:
            replace_node_in_parent(node, None)

#   - Traversal
def traverse(node, callback):
    if node is None:
        return
    traverse(node.left, callback)
    callback(node)
    traverse(node.right, callback)

def print_tree_data(node):
    def print_node(node):
        print str(node.key)
    traverse(node, print_node)

def build_tree():
    root = TreeNode(5)
    insert(root, 4)
    insert(root, 1)
    insert(root, 7)
    return root

def test_tree_operations():
    root = build_tree()
    print str(root)
    print_tree_data(root)
    print "7? "+str(search_recursively(root, 7))
    print "7? "+str(search_iteratively(root, 7))
    print "3? "+str(search_recursively(root, 3))
    print "3? "+str(search_iteratively(root, 3))
    remove(root, 7)
    print str(root)
    insert(root, 7)
    print str(root)
    remove(root, 4)
    print str(root)
    insert(root, 4)
    print str(root)
    remove(root, 5)
    print str(root)
    insert(root, 5)
    print str(root)
    print_tree_data(root)

# GRAPHS:

# Representation in memory
#   - objects and pointers
#       - extra data can be stored in the objects
#       - good if the graph is sparse
#       - space complexity: O(v) (if representing only the vertices as objects, not also the edges)
#   - adjacency matrix
#       - a two-dimensional matrix
#       - the rows represent source vertices and columns represent destination vertices.
#       - only can store the cost for the edges
#       - good if the graph is very dense
#       - space complexity: O(v**2)
#       - time complexity (add/remove edge, check if edge exists): O(1)
#   - adjacency list
#       - an array of linked lists, the size is the total of vertices
#       - for each vertex you store an array of the vertices adjacent to it
#       - can be implemented with a hash map or a defaultdict
#       - good if the graph is sparse
#       - space complexity: O(v+e)
#       - time complexity (add/remove edge, check if edge exists): O(log v)
#   - others: list of edges (as pairs of vertices, very simple)

# Graph Traversal

#   - Depth First Search (DFS)
#       - key element: stack (recursive implementation uses the call-stack)
#       - easier to visit all nodes from a graph, but is bad if the graph is too deep
#       - pre-order and other forms of tree traversal are a form of DPS
#           - the difference for a graph is that we check if the node has been visited, to avoid infinite loops
#   - Breadth First Search (BFS)
#       - key element: queue
#   - Tradeoffs
#       - depends on the structure of the tree and characteristics of the results
#       - eg.:
#           - good for DFS: solutions are deep in the tree, the tree is too wide
#           - good for BFS: solutions are near the root, the tree is too deep
#   - Time Complexity: O(v+e), since every edge and every vertix will be explored in the worst case

class Node():
    def __init__(self, data):
        self.visited = False
        self.children = []
        self.data = data

    def add_children(self, data):
        self.children.append(Node(data))

    def __repr__(self):
        return "("+str(self.data)+", "+str(self.visited)+") -> "+str(self.children)

global_visited = []

def visit_and_print(node):
    print str(node.data)

def visit_and_append(node):
    global global_visited
    global_visited.append(node.data)

def depth_first_search(root, visit):
    if root is None:
        return
    visit(root)
    root.visited = True
    for child in root.children:
        if not child.visited:
            depth_first_search(child, visit)

from collections import deque
def breadth_first_search(root, visit):
    queue = deque()
    visit(root)
    root.visited = True
    queue.appendleft(root)

    while len(queue) > 0:
        node = queue.pop()
        for child in node.children:
            if not child.visited:
                visit(child)
                child.visited = True
                queue.appendleft(child)

def create_graph():
    root = Node("A")
    root.add_children("B")
    root.add_children("C")
    root.add_children("D")
    root.children[0].add_children("E")
    root.children[2].add_children("F")
    root.children[0].children[0].add_children("G")
    return root

def test_searches():
    global global_visited
    root = create_graph()
    print "tree: "+str(root)
    depth_first_search(root, visit_and_append)
    print str(global_visited)
    global_visited = []
    root = create_graph()
    breadth_first_search(root, visit_and_append)
    print str(global_visited)

#   - Graph Overview

#       - Dijkstra:
#           - find the shortest paths between nodes in a graph
#           - elements: weighted graph, initial node, goal node
#           - the distances to the nodes start as zero for the initial node, and infinite for the other nodes
#           - keep track of lists of visited and unvisited nodes
#           - for each node, calculate the distance from it to its next unvisited nodes
#               - update the node's distance if it is lower than the current distance
#               - start by visiting the unvisited nodes with lower distance
#               - a node is marked as visited if you checked and updated all its neighboors
#           - finished when the final node is marked as visited
#           - one cost function: g(x), the real cost to reach a node x
#           - complexity (using a binary heap):
#               - time: O((e+v)*log v) (worst case)
#               - space: O(v)
#           - doesn’t work for graphs with negative weight edges
#           - works for directed and undirected graphs

#       - A*:
#           - similar to Dijkstra, but use heuristics to prioritize the node search
#           - two cost functions:
#               - g(x), the real cost to reach a node x
#               - h(x), approximate cost from node x to goal node (heuristic function)
#           - total cost: f(x)=g(x)+h(x)
#           - is complete (finds a path if it exists) and optimal (finds the shortest path) if using an Admissible heuristic function. 
#               - the real cost to reach from node x to goal node should be greater than or equal h(x)

#       - coloring:
#           - colors the nodes with the minimum number of colors so adjacent nodes don't have the same color
#           - chromatic number: smallest number of colors that suffice for a coloring a graph
#           - it is NP-complete to decide if a given graph admits a k-coloring for a given k
#           - it is NP-hard to compute the chromatic number
#           - backtracking algorithm:
#               - based on doing DFS on a state space tree with possible combinations of colouring
#               - The idea is to assign colors one by one to different vertices, starting from the vertex 0. 
#               Before assigning a color, we check for safety by considering already assigned colors to the adjacent 
#               vertices. If we find a color assignment which is safe, we mark the color assignment as part of solution. 
#               If we do not a find color due to clashes then we backtrack and return false.

# Dijkstra code (not optimal):
# nodes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
# distances = {
#     'B': {'A': 5, 'D': 1, 'G': 2},
#     'A': {'B': 5, 'D': 3, 'E': 12, 'F' :5},
#     'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
#     'G': {'B': 2, 'D': 1, 'C': 2},
#     'C': {'G': 2, 'E': 1, 'F': 16},
#     'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
#     'F': {'A': 5, 'E': 2, 'C': 16}}

# unvisited = {node: None for node in nodes} #using None as +inf
# visited = {}
# current = 'B'
# currentDistance = 0
# unvisited[current] = currentDistance

# while True:
#     for neighbour, distance in distances[current].items():
#         if neighbour not in unvisited: continue
#         newDistance = currentDistance + distance
#         if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
#             unvisited[neighbour] = newDistance
#     visited[current] = currentDistance
#     del unvisited[current]
#     if not unvisited: break
#     candidates = [node for node in unvisited.items() if node[1]]
#     current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]

# print(visited)


# /* Java program for solution of M Coloring problem
#    using backtracking */
# public class mColoringProblem {
#     final int V = 4;
#     int color[];
 
#     /* A utility function to check if the current
#        color assignment is safe for vertex v */
#     boolean isSafe(int v, int graph[][], int color[],
#                    int c)
#     {
#         for (int i = 0; i < V; i++)
#             if (graph[v][i] == 1 && c == color[i])
#                 return false;
#         return true;
#     }
 
#     /* A recursive utility function to solve m
#        coloring  problem */
#     boolean graphColoringUtil(int graph[][], int m,
#                               int color[], int v)
#     {
#         /* base case: If all vertices are assigned
#            a color then return true */
#         if (v == V)
#             return true;
 
#         /* Consider this vertex v and try different
#            colors */
#         for (int c = 1; c <= m; c++)
#         {
#             /* Check if assignment of color c to v
#                is fine*/
#             if (isSafe(v, graph, color, c))
#             {
#                 color[v] = c;
 
#                 /* recur to assign colors to rest
#                    of the vertices */
#                 if (graphColoringUtil(graph, m,
#                                       color, v + 1))
#                     return true;
 
#                 /* If assigning color c doesn't lead
#                    to a solution then remove it */
#                 color[v] = 0;
#             }
#         }
 
#         /* If no color can be assigned to this vertex
#            then return false */
#         return false;
#     }
 
#     /* This function solves the m Coloring problem using
#        Backtracking. It mainly uses graphColoringUtil()
#        to solve the problem. It returns false if the m
#        colors cannot be assigned, otherwise return true
#        and  prints assignments of colors to all vertices.
#        Please note that there  may be more than one
#        solutions, this function prints one of the
#        feasible solutions.*/
#     boolean graphColoring(int graph[][], int m)
#     {
#         // Initialize all color values as 0. This
#         // initialization is needed correct functioning
#         // of isSafe()
#         color = new int[V];
#         for (int i = 0; i < V; i++)
#             color[i] = 0;
 
#         // Call graphColoringUtil() for vertex 0
#         if (!graphColoringUtil(graph, m, color, 0))
#         {
#             System.out.println("Solution does not exist");
#             return false;
#         }
 
#         // Print the solution
#         printSolution(color);
#         return true;
#     }
 
#     /* A utility function to print solution */
#     void printSolution(int color[])
#     {
#         System.out.println("Solution Exists: Following" +
#                            " are the assigned colors");
#         for (int i = 0; i < V; i++)
#             System.out.print(" " + color[i] + " ");
#         System.out.println();
#     }
 
#     // driver program to test above function
#     public static void main(String args[])
#     {
#         mColoringProblem Coloring = new mColoringProblem();
#         /* Create following graph and test whether it is
#            3 colorable
#           (3)---(2)
#            |   / |
#            |  /  |
#            | /   |
#           (0)---(1)
#         */
#         int graph[][] = {{0, 1, 1, 1},
#             {1, 0, 1, 0},
#             {1, 1, 0, 1},
#             {1, 0, 1, 0},
#         };
#         int m = 3; // Number of colors
#         Coloring.graphColoring(graph, m);
#     }
# }

# 1. Implement a function to check if a binary tree is balanced. For the purposes of
# this question, a balanced tree is defined to be a tree such that the heights of the
# two subtrees of any node never differ by more than one.
def question1():
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def check_height(node):
        if node is None:
            return 0
        left_height = check_height(node.left)
        right_height = check_height(node.right)
        height_diff = abs(left_height-right_height)
        if left_height == -1 or right_height == -1 or height_diff > 1:
            return -1
        else:
            return max(left_height, right_height)+1

    root = build_tree()
    # insert(root, 0) # so it returns false
    if check_height(root) == -1:
        return False
    else:
        return True

# 2. Given a directed graph, design an algorithm to find out whether there is a route
# between two nodes.
found_a = False
found_b = False
def question2():
    """
    Assumption:
    - Route: The connection may be indirect via other nodes
    - I don't have access to the nodes, only to the start of the graph

    Notes:
    - breadth_first_search could be used, to guarantee to obtain the shortest path
    - depth_first_search is simpler, and may be better depending on the context

    Time Complexity: O(n)
    Space Complexity: O(r)
    """
    def depth_first_search(root, route_a, route_b, results):
        if root is None:
            return

        global found_a
        if root.data == route_a:
            found_a = True
        global found_b
        if root.data == route_b:
            found_b = True
        if found_a or found_b:
            results.append(root.data)
        if found_a and root.data == route_b or found_b and root.data == route_a:
            return

        root.visited = True
        print str(root.data)
        for child in root.children:
            if not child.visited:
                depth_first_search(child, route_a, route_b, results)
                if found_a and found_b:
                    return

    graph = create_graph()
    route_a = "B"
    route_b = "G"
    results = []
    depth_first_search(graph, route_a, route_b, results)
    return results

# 3. Given a sorted (increasing order) array with unique integer elements, write an
# algorithm to create a binary search tree with minimal height.
def question3():
    """
    Notes:
    - finds the median, divide, finds the median, divide... recursive

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    def build_tree_using_medians(array):
        if len(array) == 0:
            return None
        median_pos = len(array)/2
        median = array[median_pos]
        print str(median)
        node = TreeNode(median)
        array_left = array[0:median_pos]
        array_right = array[median_pos+1:]
        node.left = build_tree_using_medians(array_left)
        node.right = build_tree_using_medians(array_right)
        return node
    array = [1,2,3,4,5,6,7,8,9]
    result = build_tree_using_medians(array)
    return result

# 4. Given a binary tree, design an algorithm which creates a linked list of all the
# nodes at each depth (e.g., if you have a tree with depth D, you'll have D linked
# lists).
from collections import defaultdict
def question4():
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    def question4_recursion(root, lists, height):
        if root is None:
            return
        lists[height].append(root.key)
        question4_recursion(root.left, lists, height+1)
        question4_recursion(root.right, lists, height+1)
    root = build_tree()
    lists = defaultdict(list)
    question4_recursion(root, lists, height = 0)
    return lists

# 5. Implement a function to check if a binary tree is a binary search tree.
import sys
def question5():
    """
    Time Complexity: O(n)
    Space Complexity: O(log n)
    """
    def is_binary_tree_search(node, min_value, max_value):
        if node is None:
            return True
        ok = True
        if node.key > max_value or node.key <= min_value:
            ok = False
        return (ok and is_binary_tree_search(node.left, min_value, node.key) 
            and is_binary_tree_search(node.right, node.key, max_value))
    root = build_tree()
    # root.key = 100
    # print str(root)
    return is_binary_tree_search(root, -sys.maxint-1, sys.maxint)

# 6. Write an algorithm to find the'next'node (i.e., in-order successor) of a given node
# in a binary search tree. You may assume that each node has a link to its parent.
def question6():
    """
    """
    def left_most_child(node):
        while node.left is not None:
            node = node.left
        return node

    def previous_branch_parent(node):
        parent = node.parent
        while parent is not None and parent.left is not node:
            node = parent
            parent = parent.parent
        return parent

    def next_inorder_node(node):
        if node is None:
            return None
        if node.right is not None:
            return left_most_child(node.right)
        else:
            return previous_branch_parent(node)

    root = build_tree()
    # print str(root)
    result = next_inorder_node(root.left)
    if result:
        return result.key
    else:
        return None

# 7. Design an algorithm and write code to find the first common ancestor of two
# nodes in a binary tree. Avoid storing additional nodes in a data structure. NOTE:
# This is not necessarily a binary search tree.
def question7():
    """
    Time Complexity: 
    Space Complexity: 
    """
    pass
    # get a set of the ancestors of both nodes and compare?
    # iteratively go up, adding ancestors to the set, and checking if the new ancestor already exist in the other's set

# 8. You have two very large binary trees: T1, with millions of nodes, and T2, with
# hundreds of nodes. Create an algorithm to decide if T2 is a subtree of T1.
def question8():
    """
    Time Complexity: 
    Space Complexity: 
    """
    pass 
    # find the first node of the subtree T2 in T1 (be careful with duplicates)
    # recursively traverse T2 at the same time as T1, from that initial point
    # compare the nodes
    # be careful to check if the subtree in T2 doesn't have extra nodes after the subtree T1 finishes

# 9. You are given a binary tree in which each node contains a value. Design an algorithm
# to print all paths which sum to a given value. The path does not need to
# start or end at the root or a leaf.
def question9():
    """
    Time Complexity: 
    Space Complexity: 
    """
    pass
    # use recursion to accumulate a list of current sums up to the point of each node
    #   - can stop accumulating a sum if it is equal or bigger than the final sum (only if there are only values >= 0)
    # also store a list of the parents, in order to have the paths
    # to save memory but increase processing, can store only the values and nodes in the path and compute the sums for each node

if __name__ == "__main__":
    # test_searches()
    # test_tree_operations()
    # result = question1()
    # result = question2()
    # result = question3()
    # result = question4()
    # result = question5()
    result = question6()
    print str(result)

# 95

# 233