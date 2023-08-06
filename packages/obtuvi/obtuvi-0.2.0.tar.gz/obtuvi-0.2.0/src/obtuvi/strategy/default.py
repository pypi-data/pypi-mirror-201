from typing import Any

from ..ctypes import ObjectTuple, Visitor, VisitorStrategy


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
        all_keys = sorted(set(t.a.keys()).union(set(t.b.keys())))
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


__all__ = [
    "DefaultVisitorStrategy",
]
