from __future__ import annotations

from copy import deepcopy
from typing import Any, Optional, Sequence, Union
from typing import Protocol, runtime_checkable

DictKeyType = str
ListKeyType = int
KeyType = Union[DictKeyType, ListKeyType]
PathType = Union[KeyType, Sequence[KeyType]]


class ObjectTuple:
    def __init__(
        self,
        a: Any,
        b: Any,
        key: Optional[KeyType] = None,
        parent: Optional[ObjectTuple] = None,
        path: Optional[PathType] = None,
    ) -> None:
        self.a = a
        self.b = b
        self.key = key
        self.parent = parent
        self.path = path or []

    @property
    def empty(self) -> bool:
        return not self.a and not self.b

    def create_list_child(self, key: ListKeyType) -> ObjectTuple:
        assert isinstance(self.a, list)
        assert isinstance(self.b, list)
        path = deepcopy(self.path)
        path.append(key)
        return ObjectTuple(
            a=self.a[key] if 0 <= key < len(self.a) else None,
            b=self.b[key] if 0 <= key < len(self.b) else None,
            key=key,
            parent=self,
            path=path,
        )

    def create_dict_child(self, key: DictKeyType) -> ObjectTuple:
        assert isinstance(self.a, dict)
        assert isinstance(self.b, dict)
        path = deepcopy(self.path)
        path.append(key)
        return ObjectTuple(
            a=self.a.get(key, None),
            b=self.b.get(key, None),
            key=key,
            parent=self,
            path=path,
        )


class Visitor:
    def visit_node(self, t: ObjectTuple):
        pass

    def visit_node_added(self, t: ObjectTuple):
        pass

    def visit_node_removed(self, t: ObjectTuple):
        pass

    def visit_node_modified(self, t: ObjectTuple):
        pass

    def visit_node_unmodified(self, t: ObjectTuple):
        pass

    def visit_node_length_mismatch(self, t: ObjectTuple):
        pass

    def visit_node_type_mismatch(self, t: ObjectTuple):
        pass

    def visit_dict_node(self, t: ObjectTuple):
        pass

    def visit_list_node(self, t: ObjectTuple):
        pass


@runtime_checkable
class VisitorStrategy(Protocol):
    def accept(self, t: ObjectTuple, v: Visitor):
        ...


class DefaultVisitorStrategy:
    def accept(self, t: ObjectTuple, v: Visitor) -> None:
        if t.empty:
            return

        v.visit_node(t)

        if t.a is None and t.b is not None:
            v.visit_node_added(t)
        elif t.a is not None and t.b is None:
            v.visit_node_removed(t)
        elif not self.is_type_equal(t.a, t.b):
            v.visit_node_type_mismatch(t)
        elif isinstance(t.a, dict) and isinstance(t.b, dict):
            v.visit_dict_node(t)
            self.accept_dict_node(t, v)
        elif isinstance(t.a, list) and isinstance(t.b, list):
            v.visit_list_node(t)
            self.accept_list_node(t, v)
        elif not self.is_value_equal(t.a, t.b):
            v.visit_node_modified(t)
        else:
            v.visit_node_unmodified(t)

    def accept_dict_node(self, t: ObjectTuple, v: Visitor) -> None:
        assert isinstance(t.a, dict)
        assert isinstance(t.b, dict)
        len_a = len(t.a)
        len_b = len(t.b)
        all_keys = set(t.a.keys()).union(set(t.b.keys()))
        if len_a != len_b:
            v.visit_node_length_mismatch(t)
        for key in all_keys:
            self.accept(t.create_dict_child(key), v)

    def accept_list_node(self, t: ObjectTuple, v: Visitor) -> None:
        assert isinstance(t.a, list)
        assert isinstance(t.b, list)
        len_a = len(t.a)
        len_b = len(t.b)
        max_len = max(len_a, len_b)
        if len_a != len_b:
            v.visit_node_length_mismatch(t)
        for key in range(max_len):
            self.accept(t.create_list_child(key), v)

    # noinspection PyMethodMayBeStatic
    def is_type_equal(self, a: Any, b: Any) -> bool:
        return type(a) is type(b)

    # noinspection PyMethodMayBeStatic
    def is_value_equal(self, a: Any, b: Any) -> bool:
        return a == b


assert isinstance(DefaultVisitorStrategy, VisitorStrategy)


def visit(a: Any, b: Any, v: Visitor, strategy: Optional[VisitorStrategy] = None):
    strategy = strategy if strategy else DefaultVisitorStrategy()
    t = ObjectTuple(a, b)
    strategy.accept(t, v)


__name__ = "obtuvi"
__version__ = "0.1.0"
__all__ = [
    "DictKeyType",
    "ListKeyType",
    "KeyType",
    "PathType",
    "ObjectTuple",
    "Visitor",
    "VisitorStrategy",
    "DefaultVisitorStrategy",
    "visit",
]
