import networkx as nx
import matplotlib.pyplot as plt

from Q1.classes.median_maintenance import MedianMaintenance
from Q1.classes.BST.node import Node
from networkx.drawing.nx_pydot import graphviz_layout


class MedianMaintenanceBST(MedianMaintenance):
    def __init__(self):
        self.__node_number = 0
        self.__root = None
        self.__left_count = 0
        self.__right_count = 0
        self.__medians = []

    def get_root(self) -> Node:
        return self.__root

    def set_root(self, node: Node) -> None:
        self.__root = node

    def get_left_count(self) -> int:
        return self.__left_count

    def get_right_count(self) -> int:
        return self.__right_count

    def get_median_list(self) -> list[int]:
        return self.__medians.copy()

    def __increase_left_count(self) -> None:
        self.__left_count += 1

    def __increase_right_count(self) -> None:
        self.__right_count += 1

    def __decrease_left_count(self) -> None:
        self.__left_count -= 1

    def __decrease_right_count(self) -> None:
        self.__right_count -= 1

    def insert_number(self, num: int) -> None:
        if self.__root is None:
            self.__root = Node(num)
        else:
            if self.get_root().get_val() > num:
                self.__increase_left_count()
            else:
                self.__increase_right_count()
            self.__add_number_to_tree(num)
        self.__rebalance()
        self.__medians.append(self.get_median())

    def __add_number_to_tree(self, num: int) -> None:
        node = self.__root
        parent = None
        while node is not None:
            parent = node
            if num == node.get_val():
                raise ValueError("can't have duplicate values")
            if node.get_val() > num:
                node = node.get_left()
            else:
                node = node.get_right()
        parent.add_child(num)

    def __find_max_from_lower(self) -> Node:
        node = self.get_root().get_left()
        while node.get_right() is not None:
            node = node.get_right()
        return node

    def __find_min_from_upper(self) -> Node:
        node = self.get_root().get_right()
        while node.get_left() is not None:
            node = node.get_left()
        return node

    def __rotate_left(self):
        node = self.__find_min_from_upper()
        root = self.get_root()
        self.set_root(node)
        node_right = node.get_right()
        node_parent = node.get_parent()
        root_right = root.get_right()
        if root_right.get_val() == node.get_val():
            root.parent = node
            root.set_right(None)
            node.set_parent(None)
            node.set_left(root)
        else:
            node_parent.set_left(node_right)
            if node_right is not None:
                node_right.set_parent(node_parent)
            root.parent = node
            root.set_right(None)
            node.set_parent(None)
            node.set_left(root)
            node.set_right(root_right)

    def __rotate_right(self):
        node = self.__find_max_from_lower()
        root = self.get_root()
        self.set_root(node)
        node_left = node.get_left()
        node_parent = node.get_parent()
        root_left = root.get_left()
        if root_left.get_val() == node.get_val():
            root.parent = node
            root.set_left(None)
            node.set_parent(None)
            node.set_right(root)
        else:
            node_parent.set_right(node_left)
            if node_left is not None:
                node_left.set_parent(node_parent)
            root.parent = node
            root.set_left(None)
            node.set_parent(None)
            node.set_right(root)
            node.set_left(root_left)

    def __rebalance(self):
        if self.get_left_count() > self.get_right_count():
            # print('rotate right')
            self.__rotate_right()
            self.__increase_right_count()
            self.__decrease_left_count()
        elif self.get_right_count() > self.get_left_count() + 1:
            # print('rotate left')
            self.__rotate_left()
            self.__increase_left_count()
            self.__decrease_right_count()

    def get_median(self) -> int:
        return self.get_root().get_val()

    def to_graph(self) -> nx.Graph:
        nodes = [self.get_root()]
        graph = nx.Graph()
        graph.add_node(self.get_root().get_val())
        while len(nodes) > 0:
            node = nodes.pop(0)
            left, right = node.get_left(), node.get_right()
            if left is not None:
                nodes.append(left)
                graph.add_edge(left.get_val(), node.get_val())
            if right is not None:
                nodes.append(right)
                graph.add_edge(right.get_val(), node.get_val())
        return graph

    def plot_graph(self) -> None:
        graph = self.to_graph()
        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True)
        plt.show()
