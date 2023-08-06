from typing import (
    Callable
)


__all__ = (
    'first',
    'high',
    'low',
    'last',
    'add'
)


Cumulator = Callable[[float, float], float]


def first(prev: float, _: float) -> float:
    return prev


def high(prev: float, current: float) -> float:
    return max(prev, current)


def low(prev: float, current: float) -> float:
    return min(prev, current)


def last(_: float, current: float) -> float:
    return current


def add(prev: float, current: float) -> float:
    return prev + current
