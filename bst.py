from math import e
from sqlite3 import Binary
import sys
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
                    return Node(
                        val, bin_tree_builder(comes_before, left, new_value), right
                    )

                # insert into right subtree otherwise
                else:
                    return Node(
                        val, left, bin_tree_builder(comes_before, right, new_value)
                    )

    # create a new BST w/ orig 'comes_before' fn + new bin_tree from helper fn above
    return BinarySearchTree(
        bst.comes_before, bin_tree_builder(bst.comes_before, bst.BinTree, n)
    )
