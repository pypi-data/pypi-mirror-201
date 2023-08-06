from ..ctypes import ObjectTuple, Visitor


class EchoVisitor(Visitor):
    def visit_node(self, t: ObjectTuple):
        print(f"node: {t.path}")

    def visit_node_added(self, t: ObjectTuple):
        print(f"node: {t.path} added: {t.b}")

    def visit_node_removed(self, t: ObjectTuple):
        print(f"node: {t.path} removed: {t.a}")

    def visit_node_modified(self, t: ObjectTuple):
        print(f"node: {t.path} modified: {t.a} -> {t.b}")

    def visit_node_unmodified(self, t: ObjectTuple):
        print(f"node: {t.path} unmodified: {t.a} == {t.b}")

    def visit_node_length_mismatch(self, t: ObjectTuple):
        print(f"node: {t.path} length-mismatch: [{len(t.a)}] -> [{len(t.b)}]")

    def visit_node_type_mismatch(self, t: ObjectTuple):
        print(
            f"node: {t.path} type-mismatch: {t.a} ({type(t.a)}) -> {t.b} ({type(t.b)})"
        )

    def visit_dict_node(self, t: ObjectTuple):
        print(f"node: {t.path} dict")

    def visit_list_node(self, t: ObjectTuple):
        print(f"node: {t.path} list")


__all__ = [
    "EchoVisitor",
]
