from math import sqrt, isnan, isinf

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

# Define the zero vector
zero = Vector2(0.0, 0.0)

def add(v1: Vector2, v2: Vector2) -> Vector2:
    return Vector2(v1.x + v2.x, v1.y + v2.y)

def sub(v1: Vector2, v2: Vector2) -> Vector2:
    return Vector2(v1.x - v2.x, v1.y - v2.y)

def scalar_times(c: float, v: Vector2) -> Vector2:
    return Vector2(c * v.x, c * v.y)

def mag(v: Vector2) -> float:
    return sqrt(v.x * v.x + v.y * v.y)

def unit(v: Vector2) -> Vector2:
    magnitude = mag(v)
    if magnitude == 0:
        return Vector2(0, 0)
    else:
        return scalar_times(1 / magnitude, v)

def dot(v1: Vector2, v2: Vector2) -> float:
    return v1.x * v2.x + v1.y * v2.y

def avg(v1: Vector2, v2: Vector2) -> Vector2:
    return scalar_times(0.5, add(v1, v2))

def sq_mag(v: Vector2) -> float:
    return v.x * v.x + v.y * v.y

def is_real(v: Vector2) -> bool:
    return not (isnan(v.x) or isnan(v.y) or isinf(v.x) or isinf(v.y))

def in_bounds(v: Vector2, v0: Vector2, v1: Vector2) -> bool:
    return v0.x <= v.x <= v1.x and v0.y <= v.y <= v1.y
