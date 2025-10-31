import sys
import unittest
from typing import *
from dataclasses import dataclass
import math
import matplotlib as plt
import numpy as np
import random

sys.setrecursionlimit(10**6)
from bst import *

TREES_PER_RUN: int = 10000


def example_graph_creation() -> None:
    def f_to_graph(x: float) -> float:
        return math.log2(x) + 5.0

    x_coords: List[float] = [float(i) for i in range(1, 100)]
    y_coords: List[float] = [f_to_graph(x) for x in x_coords]

    x_numpy: np.ndarray = np.array(x_coords)
    y_numpy: np.ndarray = np.array(y_coords)

    plt.plot(x_numpy, y_numpy, label="log_2(x)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Example Graph")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    example_graph_creation()
