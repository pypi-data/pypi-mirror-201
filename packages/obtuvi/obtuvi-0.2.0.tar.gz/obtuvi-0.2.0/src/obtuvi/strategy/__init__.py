from typing import Any, Optional

from ..ctypes import ObjectTuple, Visitor, VisitorStrategy
from .default import DefaultVisitorStrategy


def visit(a: Any, b: Any, v: Visitor, strategy: Optional[VisitorStrategy] = None):
    strategy = strategy if strategy else DefaultVisitorStrategy()
    t = ObjectTuple(a, b)
    strategy.accept(t, v)


__all__ = [
    "DefaultVisitorStrategy",
    "visit",
]
