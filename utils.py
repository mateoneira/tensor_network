from typing import Callable, List, TypeVar

A = TypeVar('A')
B = TypeVar('B')

def argcmp(cmp: Callable[[B, B], bool], f: Callable[[A], B], lst: List[A]) -> A:
    if not lst:
        raise ValueError("argcmp passed empty list")
    if len(lst) == 1:
        return lst[0]

    def recursive_cmp(n: A, ns: List[A]) -> A:
        if not ns:
            return n
        s = recursive_cmp(ns[0], ns[1:])
        return n if cmp(f(n), f(s)) else s

    return recursive_cmp(lst[0], lst[1:])

def argmin(f: Callable[[A], B], lst: List[A]) -> A:
    return argcmp(lambda x, y: x < y, f, lst)

def argmax(f: Callable[[A], B], lst: List[A]) -> A:
    return argcmp(lambda x, y: x > y, f, lst)
