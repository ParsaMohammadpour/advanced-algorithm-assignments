from typing import Self


class Node:
    def __init__(self, value: int, parent: Self = None, left: Self = None, right: Self = None):
        self.__val = value
        self.__parent = parent
        self.__left = left
        self.__right = right

    def get_val(self) -> int:
        return self.__val

    def get_parent(self) -> Self:
        return self.__parent

    def get_left(self) -> Self:
        return self.__left

    def get_right(self) -> Self:
        return self.__right

    def set_left(self, node: Self) -> None:
        self.__left = node

    def set_right(self, node: Self) -> None:
        self.__right = node

    def set_parent(self, node: Self):
        self.__parent = node

    def add_child(self, num: int) -> None:
        if self.get_val() == num:
            raise ValueError("can't have duplicate values")
        if self.get_val() > num:
            if self.get_left() is not None:
                raise Exception("already have child node")
            node = Node(num, parent=self)
            self.set_left(node)
        else:
            if self.get_right() is not None:
                raise Exception("already have child node")
            node = Node(num, parent=self)
            self.set_right(node)

    def get_children_sub_node_number(self) -> [int, int]:
        left_node = self.get_left()
        left_count = left_node.get_sub_node_number() if left_node is not None else 0
        right_node = self.get_right()
        right_count = right_node.get_sub_node_number() if right_node is not None else 0
        return left_count, right_count
