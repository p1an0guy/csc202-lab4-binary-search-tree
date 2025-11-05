import sys
import unittest
from typing import *
from dataclasses import dataclass
import math
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import random
import time
sys.setrecursionlimit(10**6)
from bst import *

TREES_PER_RUN: int = 10000
n_max: int = 50

# generate a random tree with a given number of nodes
def random_tree(nodes: int) -> BinarySearchTree:
    bst: BinarySearchTree = BinarySearchTree(numeric_lt, None) # empty binary tree
    
    # repeatedly insert random num between 0 and 1
    for i in range(nodes):
        bst = insert(bst, random.random())
    return bst

# find length of the path to the "deepest" node
def max_height(bst: BinarySearchTree) -> int:
    return height_helper(bst.BinTree)

# helper function that takes only the bin tree part (without comparison fn)
def height_helper(bt: BinTree) -> int:
    match bt:
        case None:
            return 0
        case Node(val, left, right):
            return max(1+height_helper(left), 1+height_helper(right))
       
# ---AVERAGE HEIGHT OF RANDOMLY-GENERATED TREE---
# initialize list to store average heights of trees 
avg_height: list[float] = [0] * (n_max)    

# find the average heights of trees with a variety of sizes
for n in range(n_max):
    accum: int = 0
    for i in range(TREES_PER_RUN):  # do it TREES_PER_RUN times, then take average
        accum += max_height(random_tree(n))
    avg_height[n] = float(accum/TREES_PER_RUN)

# ---AVERAGE TIME OF INSERTION INTO RANDOMLY-GENERATED TREE---
# initialize list to store average insertion times
insert_time: list[float] = [0] * n_max

# find avg insertion times for trees with variety of sizes
for n in range(n_max):
    time_accum: float = 0
    for i in range(TREES_PER_RUN): # again, we take the average
        bst: BinarySearchTree = random_tree(n)
        start: float = time.perf_counter()
        insert(bst, random.random())
        end: float = time.perf_counter()
        time_accum += end - start
    insert_time[n] = float(time_accum/TREES_PER_RUN) 



def avg_height_graph_creation() -> None:

    x_coords: List[int] = [n for n in range(n_max)]
    y_coords: List[float] = avg_height

    x_numpy: np.ndarray = np.array(x_coords)
    y_numpy: np.ndarray = np.array(y_coords)

    plt.plot(x_numpy, y_numpy, label="Avg. Tree Height vs. # Nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Average tree height")
    plt.title("Tree Height")
    plt.grid(True)
    plt.legend()
    plt.savefig("avg_height_plot.png", dpi=150, bbox_inches="tight")

def insert_time_graph_creation() -> None:
    x_coords: List[int] = [n for n in range(n_max)]
    y_coords: List[float] = insert_time
    
    x_numpy: np.ndarray = np.array(x_coords)
    y_numpy: np.ndarray = np.array(y_coords)

    plt.plot(x_numpy, y_numpy, label="Insert time vs. # nodes")
    plt.xlabel("Number of nodes")
    plt.ylabel("Insert time")
    plt.title("Insert time vs. # nodes")
    plt.grid(True)
    plt.legend()
    plt.savefig("insert_time.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    insert_time_graph_creation()