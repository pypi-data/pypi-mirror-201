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


__all__ = [
    "DictKeyType",
    "ListKeyType",
    "KeyType",
    "PathType",
    "ObjectTuple",
    "Visitor",
    "VisitorStrategy",
]
