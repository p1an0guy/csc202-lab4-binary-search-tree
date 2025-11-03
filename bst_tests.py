import sys
import unittest
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)
from bst import *


class BSTTests(unittest.TestCase):
    def test_is_empty1(self) -> None:
        self.assertEqual(is_empty(BinarySearchTree(numeric_lt, None)), True)
    
    def test_is_empty2(self) -> None:
        self.assertEqual(is_empty(BinarySearchTree(numeric_lt, Node(1,
                                                                    Node(2, None, None),
                                                                    Node(3, None, None)))),
                         False)
    def test_is_empty3(self) -> None:
        self.assertEqual(is_empty(bst3), False)

    def test_is_empty4(self) -> None:
        self.assertEqual(is_empty(bst4), False)
        
    def test_insert1(self) -> None:
        self.assertEqual(insert(bst1, 2), BinarySearchTree(numeric_lt, Node(3, Node(1, None, Node(2, None, None)), Node(5, None, None))))
                                                        
    def test_insert2(self) -> None:
        self.assertEqual(insert(BinarySearchTree(numeric_lt, None), 1), BinarySearchTree(numeric_lt, Node(1, None, None)))

    def test_insert3(self) -> None:
        self.assertEqual(insert(bst3, "zebra"), BinarySearchTree(string_lt, bt3_after_insert_zebra))
    
    def test_insert4(self) -> None:
        self.assertEqual(insert(bst4, Point2(1.1, 2.2)), BinarySearchTree(distance_lt, bt4_aftr_insert_pt))

    def test_lookup1(self) -> None:
        self.assertEqual(lookup(bst1, 3), True)
    
    def test_lookup2(self) -> None:
        self.assertEqual(lookup(bst1, 2), False)
    
    def test_lookup3(self) -> None:
        self.assertEqual(lookup(BinarySearchTree(numeric_lt, None), 1), False)
    
    def test_lookup4(self) -> None:
        self.assertEqual(lookup(bst3, "zebra"), False)
    
    def test_lookup5(self) -> None:
        self.assertEqual(lookup(bst3, "apple"), True)

    def test_lookup6(self) -> None:
        self.assertEqual(lookup(bst4, Point2(2.17, 3.14)), True)
    
    def test_lookup7(self) -> None:
        self.assertEqual(lookup(bst4, Point2(1.1, 2.2)), False)

    def test_delete1(self) -> None:
        self.assertEqual(delete(bst1, 3), BinarySearchTree(numeric_lt, Node(1, None, Node(5, None, None))))
    
    def test_delete2(self) -> None:
        self.assertEqual(delete(bst2, 6), BinarySearchTree(numeric_lt, bt2_after_delete6))

    def test_delete3(self) -> None:
        self.assertEqual(delete(bst2, 3), BinarySearchTree(numeric_lt, bt2_after_delete3)) 

    def test_delete4(self) -> None:
        self.assertEqual(delete(BinarySearchTree(string_lt, bt3_after_insert_zebra), "zebra"), bst3)
    
    def test_delete5(self) -> None:
        self.assertEqual(delete(BinarySearchTree(string_lt, bt3_after_insert_zebra), "banana"), BinarySearchTree(string_lt, bt3_after_delete_banana))
    
    def test_delete6(self) -> None:
        self.assertEqual(delete(BinarySearchTree(distance_lt, bt4_aftr_insert_pt), Point2(1.1, 2.2)), bst4)

if __name__ == "__main__":
    unittest.main()
