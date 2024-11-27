import heapq
import heapq as hq
import networkx as nx
import matplotlib.pyplot as plt

from typing import Any
from networkx.drawing.nx_pydot import graphviz_layout

from Q2.classes.node import Node


class HuffmanAlgorithm:

    @staticmethod
    def __set_node_code(node: Node, path: str):
        node.set_code(path)
        left_child, right_child = node.get_left(), node.get_right()
        if left_child is not None:
            HuffmanAlgorithm.__set_node_code(left_child, path + '0')
        if right_child is not None:
            HuffmanAlgorithm.__set_node_code(right_child, path + '1')

    @staticmethod
    def set_tree_codes(root: Node):
        HuffmanAlgorithm.__set_node_code(root, '')

    @staticmethod
    def generate_tree(symbol_freq: list[Any, int]) -> Node:
        nodes = [Node(val, freq) for val, freq in symbol_freq]
        heapq.heapify(nodes)
        while len(nodes) > 1:
            min_node = heapq.heappop(nodes)
            second_min = heapq.heappop(nodes)
            freq = min_node.get_freq() + second_min.get_freq()
            new_node = Node(None, freq)
            new_node.set_left(min_node)
            new_node.set_right(second_min)
            min_node.set_parent(new_node)
            second_min.set_parent(new_node)
            hq.heappush(nodes, new_node)
        root = nodes[0]
        HuffmanAlgorithm.set_tree_codes(root)
        return root

    @staticmethod
    def generate_nx_graph(root: Node) -> [nx.Graph, list[str]]:
        nodes = [root]
        graph = nx.Graph()
        node_colors = []
        graph.add_node(root.get_graph_repr())
        color = 'deepskyblue' if root.has_value() else 'yellow'
        node_colors.append(color)
        while len(nodes) > 0:
            node = nodes.pop(0)
            left, right = node.get_left(), node.get_right()
            if left is not None:
                nodes.append(left)
                color = 'deepskyblue' if left.has_value() else 'yellow'
                node_colors.append(color)
                graph.add_edge(left.get_graph_repr(), node.get_graph_repr(), weight='*0')
            if right is not None:
                nodes.append(right)
                color = 'deepskyblue' if right.has_value() else 'yellow'
                node_colors.append(color)
                graph.add_edge(right.get_graph_repr(), node.get_graph_repr(), weight='*1')
        return graph, node_colors

    @staticmethod
    def plot_tree(root: Node, figsize: tuple[int, int] = None, save_path:str=None) -> None:
        if figsize is not None:
            plt.figure(figsize=figsize)
        graph, node_colors = HuffmanAlgorithm.generate_nx_graph(root)
        pos = graphviz_layout(graph, prog='dot')
        nx.draw(graph, pos, with_labels=True, )
        nx.draw_networkx_nodes(graph, pos, node_color=node_colors)
        labels = nx.get_edge_attributes(graph, 'weight')
        for key, val in labels.items():
            labels[key] = '1' if val == '*1' else '0'
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        if save_path is not None:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    @staticmethod
    def __depth(node, func) -> int:
        if node.has_value():
            return len(node.get_code())
        children_vals = []
        if node.get_left() is not None:
            left = HuffmanAlgorithm.__depth(node.get_left(), func)
            children_vals.append(left)
        if node.get_right() is not None:
            right = HuffmanAlgorithm.__depth(node.get_right(), func)
            children_vals.append(right)
        return func(children_vals)

    @staticmethod
    def get_min_code_len(root: Node) -> int:
        return HuffmanAlgorithm.__depth(root, min)

    @staticmethod
    def get_max_code_len(root: Node) -> int:
        return HuffmanAlgorithm.__depth(root, max)
