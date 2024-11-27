from typing import Self


class Node:
    def __init__(self, val: str, freq: int, parent: Self = None, left: Self = None, right: Self = None):
        self.__val = val
        self.__freq = freq
        self.__parent = parent
        self.__left = left
        self.__right = right
        self.__code = None

    def get_val(self) -> str:
        return self.__val

    def get_freq(self) -> int:
        return self.__freq

    def set_val(self, val: str) -> None:
        self.__val = val

    def set_freq(self, freq: int) -> None:
        self.__freq = freq

    def get_parent(self) -> Self:
        return self.__parent

    def set_parent(self, parent: Self) -> None:
        self.__parent = parent

    def get_left(self) -> Self:
        return self.__left

    def set_left(self, left: Self) -> None:
        self.__left = left

    def get_right(self) -> Self:
        return self.__right

    def set_right(self, right: Self) -> None:
        self.__right = right

    def get_code(self) -> str:
        return self.__code

    def set_code(self, code: str) -> None:
        self.__code = code

    def get_graph_repr(self) -> str:
        res = self.get_code()
        if res == '':
            res = ' '
        if self.get_val() is not None:
            res += ' -> ' + self.get_val()
        return res

    def has_value(self) -> bool:
        return self.get_val() is not None

    def __str__(self) -> str:
        return self.get_graph_repr()

    def __repr__(self) -> str:
        return self.get_graph_repr()

    def __lt__(self, other):
        return self.get_freq() < other.get_freq()
