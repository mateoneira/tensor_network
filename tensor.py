import math
from vector import Vector2 
from typing import Union

class Tensor:
    def __init__(self, a: float, b: float, d: float):
        self.a = a
        self.b = b
        self.d = d

    def __repr__(self):
        return f"Tensor({self.a}, {self.b}, {self.d})"

# Define the trivial tensor
trivial = Tensor(0.0, 0.0, 0.0)

# Creating tensors from various types of constraints
def from_r_theta(r: float, t: float) -> Tensor:
    cos_2t = r * math.cos(2 * t)
    sin_2t = r * math.sin(2 * t)
    return Tensor(cos_2t, sin_2t, -cos_2t)

def from_xy(x: float, y: float) -> Tensor:
    xy = -2 * x * y
    diff_squares = y * y - x * x
    return Tensor(diff_squares, xy, -diff_squares)

# Basic tensor operations
def add(t1: Tensor, t2: Tensor) -> Tensor:
    return Tensor(t1.a + t2.a, t1.b + t2.b, t1.d + t2.d)

def sum_tensors(tensors: list) -> Tensor:
    return sum(tensors, trivial)

def scalar_times(c: float, t: Tensor) -> Tensor:
    return Tensor(c * t.a, c * t.b, c * t.d)

def is_real(t: Tensor) -> bool:
    def isreal(x):
        return not (math.isnan(x) or math.isinf(x))
    return isreal(t.a) and isreal(t.b) and isreal(t.d)

# Calculating eigenvalues and vectors
def eigenvalues(t: Tensor) -> Union[float, float]:
    eval_ = math.sqrt(t.a * t.a + t.b * t.b)
    return eval_, -eval_

def eigenvectors(t: Tensor) -> Union[Vector2, Vector2]:
    if t.b == 0:
        if t.a > t.d:
            return Vector2(1, 0), Vector2(0, 1)
        else:
            return Vector2(0, 1), Vector2(1, 0)
    else:
        eval1, eval2 = eigenvalues(t)
        mk_evec = lambda eval_: Vector2(1, (eval_ - t.a) / t.b)
        return mk_evec(eval1), mk_evec(eval2)
