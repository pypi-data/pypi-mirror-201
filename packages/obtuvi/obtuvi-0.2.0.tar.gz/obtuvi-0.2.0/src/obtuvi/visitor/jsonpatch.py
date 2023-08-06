from __future__ import annotations

import json

from dataclasses import dataclass, field
from io import StringIO
from typing import Any, List, Literal, Optional, Sequence, Union

from ..ctypes import PathType, ObjectTuple, Visitor


def jsonptr_escape(value: Any) -> str:
    if not isinstance(value, str):
        value = str(value)
    return value.replace("~", "~0").replace("/", "~1")


def jsonptr_unescape(value: Any) -> str:
    if not isinstance(value, str):
        value = str(value)
    return value.replace("~1", "/").replace("~0", "~")


def pathtype_to_jsonptr(path: PathType, prefix: str = "#/") -> str:
    return prefix + "/".join(map(jsonptr_escape, path))


JsonPatchOperationType = Literal["add", "remove", "replace", "copy", "move", "test"]


@dataclass
class JsonPatchOperation:
    op: JsonPatchOperationType
    path: str
    value: Optional[Any] = None
    from_: Optional[str] = None

    def __dict__(self) -> dict:
        dikt = {"op": self.op}
        if self.from_ and self.op in {"copy", "move"}:
            dikt["from"] = self.from_
        dikt["path"] = self.path
        if self.op in {"add", "replace", "test"}:
            dikt["value"] = self.value
        return dikt

    def __str__(self) -> str:
        return json.dumps(self.__dict__()).strip()

    def test_wrap(self, old_value: Any) -> JsonPatchOperationSet:
        if self.op not in {"remove", "replace"}:
            return self
        return [
            JsonPatchOperation(op="test", path=self.path, value=old_value),
            self,
        ]


JsonPatchOperationSet = Union[JsonPatchOperation, Sequence[JsonPatchOperation]]


@dataclass
class JsonPatch:
    operations: List[JsonPatchOperationSet] = field(default_factory=list)

    def __str__(self) -> str:
        indent = "  "
        sio = StringIO()
        sio.write("[\n")
        l0 = len(self.operations)
        for i0, o0 in enumerate(self.operations):
            if isinstance(o0, JsonPatchOperation):
                sio.write(indent)
                sio.write(str(o0))
            else:
                l1 = len(o0)
                for i1, o1 in enumerate(o0):
                    sio.write(indent)
                    sio.write(str(o1))
                    if i1 < l1 - 1:
                        sio.write(",\n")
            if i0 < l0 - 1:
                sio.write(",\n")
            sio.write("\n")
        sio.write("]")
        return sio.getvalue()

    def append(self, item) -> None:
        self.operations.append(item)


class JsonPatchVisitor(Visitor):
    def __init__(self) -> None:
        self.patch: JsonPatch = JsonPatch()

    def visit_node_added(self, t: ObjectTuple) -> None:
        self.patch.append(
            JsonPatchOperation(op="add", path=pathtype_to_jsonptr(t.path), value=t.b)
        )

    def visit_node_removed(self, t: ObjectTuple) -> None:
        self.patch.append(
            JsonPatchOperation(op="remove", path=pathtype_to_jsonptr(t.path)).test_wrap(
                old_value=t.a
            )
        )

    def visit_node_modified(self, t: ObjectTuple) -> None:
        self.patch.append(
            JsonPatchOperation(
                op="replace", path=pathtype_to_jsonptr(t.path), value=t.b
            ).test_wrap(old_value=t.a)
        )

    def visit_node_type_mismatch(self, t: ObjectTuple):
        self.visit_node_modified(t=t)


__all__ = [
    "JsonPatch",
    "JsonPatchOperation",
    "JsonPatchOperationSet",
    "JsonPatchOperationType",
    "JsonPatchVisitor",
    "jsonptr_escape",
    "jsonptr_unescape",
    "pathtype_to_jsonptr",
]
