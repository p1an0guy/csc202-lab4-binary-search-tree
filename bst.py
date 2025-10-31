from math import e
from multiprocessing import Value
from re import search
from sqlite3 import Binary
import sys
from tkinter import W
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


# given a BST, return True if it's empty, False otherwise
def is_empty(bst: BinarySearchTree) -> bool:
    return bst.BinTree == None


# inputs: BST, new val. output: BST w/ new val using comes_before fn
def insert(bst: BinarySearchTree, n: Any) -> BinarySearchTree:
    # create a new BST w/ orig 'comes_before' fn + new bin_tree from helper fn below
    return BinarySearchTree(
        bst.comes_before, bin_tree_builder(bst.comes_before, bst.BinTree, n)
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
            return None
        case Node(val, left, right):
            if cb(target, val):
                return Node(val, search_and_destroy(left, cb, target), right)
            if cb(val, target):
                return Node(val, left, search_and_destroy(right, cb, target))
            delete_root(bt, cb)


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
