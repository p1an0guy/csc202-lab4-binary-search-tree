from math import e, sqrt
from multiprocessing import Value
from re import search
from sqlite3 import Binary
import sys
#from tkinter import W
from unicodedata import numeric
import unittest
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)


BinTree: TypeAlias = Union["Node", None]


@dataclass(frozen=True)
class BinarySearchTree:
    comes_before: Callable[[Any, Any], bool]
    BinTree: BinTree


@dataclass(frozen=True)
class Node:
    val: Any
    left: BinTree
    right: BinTree
    
@dataclass(frozen=True)
class Point2:
    x: float
    y: float


# given a BST, return True if it's empty, False otherwise
def is_empty(bst: BinarySearchTree) -> bool:
    return bst.BinTree == None


# inputs: BST, new val. output: BST w/ new val using comes_before fn
def insert(bst: BinarySearchTree, new: Any) -> BinarySearchTree:
    # create a new BST w/ orig 'comes_before' fn + new bin_tree from helper fn below
    return BinarySearchTree(
        bst.comes_before, bin_tree_builder(bst.comes_before, bst.BinTree, new)
    )


# helper fn: inserts n into correct position of BinTree
def bin_tree_builder(
    comes_before: Callable[[Any, Any], bool], bt: BinTree, new_value: Any
) -> BinTree:
    match bt:

        # arrive at empty Node -> insert new_value
        case None:
            return Node(new_value, None, None)

        # at each Node along the way, compare new_value with root value
        case Node(val, left, right):
            # use comes_before fn that was passed in from main fn

            # insert into left subtree if new_val 'come before' root val
            if comes_before(new_value, val):
                return Node(val, bin_tree_builder(comes_before, left, new_value), right)

            # insert into right subtree otherwise
            else:
                return Node(val, left, bin_tree_builder(comes_before, right, new_value))


# returns True if given value is in the BST, False otherwise
def lookup(bst: BinarySearchTree, target: Any) -> bool:
    return lookup_helper(bst.comes_before, bst.BinTree, target)


# helper function to loop through the actual BinTree
def lookup_helper(
    comes_before: Callable[[Any, Any], bool], bt: BinTree, target: Any
) -> bool:
    match bt:
        case None:
            return False
        case Node(val, left, right):
            if comes_before(target, val):
                return lookup_helper(comes_before, left, target)
            elif comes_before(val, target):
                return lookup_helper(comes_before, right, target)
            else:
                return True


# deletes specified element from BST if it's present
def delete(bst: BinarySearchTree, target: Any) -> BinarySearchTree:
    # call a helper function that takes in BT and comes_before from BST
    return BinarySearchTree(
        bst.comes_before, search_and_destroy(bst.BinTree, bst.comes_before, target)
    )


# helper function doing recursive calls to remove value from BT
def search_and_destroy(
    bt: BinTree, cb: Callable[[Any, Any], bool], target: Any
) -> BinTree:
    match bt:
        case None:
            raise ValueError("Error: Attempted deletion from empty Binary Search Tree")
        case Node(val, left, right):
            if cb(target, val):
                return Node(val, search_and_destroy(left, cb, target), right)
            if cb(val, target):
                return Node(val, left, search_and_destroy(right, cb, target))
            return delete_root(bt, cb)


# deletes root value from BST, replacing w/ largest value in left subtree
# or the smallest value in the right subtree
def delete_root(bt: BinTree, cb: Callable[[Any, Any], bool]) -> BinTree:
    if not bt:
        raise ValueError("Binary Search Tree is empty")
    if bt.left:
        # replace the value with the largest val in left subtree
        curr_node: BinTree = bt.left
        while curr_node.right:
            curr_node = curr_node.right
        replacement_val: Any = curr_node.val
        return Node(replacement_val, delete_rightmost_child(bt.left), bt.right)

    # if bst.left is None, we use smallest val in right subtree
    if bt.right:
        curr_node: BinTree = bt.right
        while curr_node.left:
            curr_node = curr_node.left
        replacement_val: Any = curr_node.val
        return Node(replacement_val, bt.left, delete_leftmost_child(bt.right))
    return None


def delete_rightmost_child(bt: BinTree) -> BinTree:
    match bt:
        case None:
            raise ValueError("Binary Tree does not exist")
        case Node(val, left, right):
            # if the right subtree exists, recursively call
            if right:
                return Node(val, left, delete_rightmost_child(right))
            # if right subtree doesn't exist, we're at the rightmost child
            return None


def delete_leftmost_child(bt: BinTree) -> BinTree:
    match bt:
        case None:
            raise ValueError("Binary Tree does not exist")
        case Node(val, left, right):
            # if the left subtree exists
            if left:
                return Node(val, delete_leftmost_child(left), right)
            # if there is no subtree, we've reached the leftmost child and can delete
            return None

# defining example comes_before fns and bst's for the test cases
def numeric_lt(n1: int, n2: int) -> bool:
    return n1 < n2

def string_lt(s1: str, s2: str) -> bool:
    return s1 < s2

def distance_lt(p1: Point2, p2: Point2) -> bool:
    d1: float = sqrt(p1.x**2 + p1.y**2)
    d2: float =sqrt(p2.x**2 + p2.y**2)
    return d1 < d2
    
bt1: BinTree = Node(3, Node(1, None, None), Node(5, None, None))
bst1: BinarySearchTree = BinarySearchTree(numeric_lt, bt1)
bt2: BinTree = Node(5,
                    Node(3,
                            Node(1, None,
                                 Node(2, None, None)),
                            Node(4, None, None)),
                    Node(8,
                         Node(7,
                              Node(6, None, None),
                              Node(9, None,
                                   Node(10, None, None))),
                         None))
bst2: BinarySearchTree = BinarySearchTree(numeric_lt, bt2)
bt2_after_delete6: BinTree = Node(5,
                    Node(3,
                            Node(1, None,
                                 Node(2, None, None)),
                            Node(4, None, None)),
                    Node(8,
                         Node(7,
                              None,
                              Node(9, None,
                                   Node(10, None, None))),
                         None))

bt2_after_delete3: BinTree = Node(5,
                    Node(2,
                            Node(1, None, None),
                            Node(4, None, None)),
                    Node(8,
                         Node(7,
                              Node(6, None, None),
                              Node(9, None,
                                   Node(10, None, None))),
                         None))

bt3: BinTree = Node("gucci",
                    Node("dog",
                         Node("banana",
                              Node("apple", None, None),None),
                         Node("elephant", None,
                              Node("french", None, None))),
                    Node("monkey",
                         Node("hobo", None,
                              Node("interest", None, Node("jonah", None, None))),
                         Node("popcorn", Node("orange", None, None), None)))
bt3_after_insert_zebra: BinTree =  Node("gucci",
                    Node("dog",
                         Node("banana",
                              Node("apple", None, None),None),
                         Node("elephant", None,
                              Node("french", None, None))),
                    Node("monkey",
                         Node("hobo", None,
                              Node("interest", None, Node("jonah", None, None))),
                         Node("popcorn", Node("orange", None, None), Node("zebra", None, None))))
bt3_after_delete_banana: BinTree = Node("gucci",
                    Node("dog",
                         Node("apple",
                             None,None),
                         Node("elephant", None,
                              Node("french", None, None))),
                    Node("monkey",
                         Node("hobo", None,
                              Node("interest", None, Node("jonah", None, None))),
                         Node("popcorn", Node("orange", None, None), Node("zebra", None, None))))
bst3: BinarySearchTree = BinarySearchTree(string_lt, bt3)

bt4: BinTree = Node(Point2(5.5, 6.5),
                    Node(Point2(2.17, 3.14), None,
                         Node(Point2(3.7, 4.2), None, None)),
                    Node(Point2(10, 9.8),
                         Node(Point2(7.8, 8.9), None,
                              Node(Point2(8.9, 9.2), None, None)),
                         Node(Point2(25.1, 24), None, None)))

bt4_aftr_insert_pt: BinTree = Node(Point2(5.5, 6.5),
                    Node(Point2(2.17, 3.14),
                         Node(Point2(1.1, 2.2), None, None),
                         Node(Point2(3.7, 4.2), None, None)),
                    Node(Point2(10, 9.8),
                         Node(Point2(7.8, 8.9), None,
                              Node(Point2(8.9, 9.2), None, None)),
                         Node(Point2(25.1, 24), None, None)))
bst4: BinarySearchTree = BinarySearchTree(distance_lt, bt4)