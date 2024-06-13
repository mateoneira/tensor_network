import math
from typing import List, Tuple, TypeVar, Optional, Generic
from collections import defaultdict
from vector import Vector2
from utils import argmin

A = TypeVar('A')

class Storage(Generic[A]):
    pass

class ListStorage(Storage[A]):
    def __init__(self):
        self.items: List[Tuple[Vector2, A]] = []

    def __repr__(self):
        return f"ListStorage({self.items})"

class BucketsStorage(Storage[A]):
    def __init__(self, width: float, height: float, nbuckets: int):
        self.width = width
        self.height = height
        self.xsize = width / nbuckets
        self.ysize = height / nbuckets
        self.buckets = defaultdict(lambda: defaultdict(list))

    def __repr__(self):
        return f"BucketsStorage(width={self.width}, height={self.height}, buckets={dict(self.buckets)})"

def buckets_new(width: float, height: float, nbuckets: int) -> BucketsStorage[A]:
    return BucketsStorage(width, height, nbuckets)

def buckets_insert(storage: BucketsStorage[A], point: Tuple[Vector2, A]) -> BucketsStorage[A]:
    px, py = point[0].x, point[0].y
    if not (0 <= px < storage.width and 0 <= py < storage.height):
        return storage

    x = int(px / storage.xsize)
    y = int(py / storage.ysize)
    storage.buckets[y][x].append(point)
    return storage

def buckets_lookup(storage: BucketsStorage[A], query: Vector2) -> Optional[Tuple[Vector2, A]]:
    x, y = query.x, query.y
    bx = int(x / storage.xsize)
    by = int(y / storage.ysize)
    n = int(storage.width / storage.xsize)
    points = [(bx+a, by+b) for a in range(-1, 2) for b in range(-1, 2)]
    
    def get_bucket(a: int, b: int) -> List[Tuple[Vector2, A]]:
        if 0 <= a < n and 0 <= b < n:
            return storage.buckets[b][a]
        return []

    blist = [item for p in points for item in get_bucket(*p)]
    if not blist:
        return None
    
    def dist(v: Vector2) -> float:
        return (v.x - x)**2 + (v.y - y)**2

    return argmin(lambda item: dist(item[0]), blist)

class NearestNeighbor(Generic[A]):
    def __init__(self, width: float, height: float, nbuckets: int):
        self.storage = buckets_new(width, height, nbuckets)

    def insert(self, point: Tuple[Vector2, A]) -> None:
        self.storage = buckets_insert(self.storage, point)

    def lookup(self, query: Vector2) -> Optional[Tuple[Vector2, A]]:
        return buckets_lookup(self.storage, query)

# Example usage:
if __name__ == "__main__":
    nn = NearestNeighbor[float](100, 100, 10)
    nn.insert((Vector2(10, 10), 1.0))
    nn.insert((Vector2(20, 20), 2.0))
    nn.insert((Vector2(30, 30), 3.0))
    print(nn.lookup(Vector2(15, 15)))
