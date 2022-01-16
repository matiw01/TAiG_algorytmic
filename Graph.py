from typing import List, Tuple

import graphviz

from Edge import Edge
from Vertex import Vertex


# assuming matrixGraph is matrix where each row is list of outgoing edges and column is list of ingoing edges
# and labels is list of labels so labels[i] is label for vertex created of matrixGraph[i]
class Graph:
    def __init__(self, vertices: List[Tuple[int, str]], edges: List[Tuple[int, int, str]], name: str):
        self.name = name
        self.previous_data = [vertices, edges]
        self.create(self, vertices, edges)

    def undo(self):
        self.create(self, self.previous_data[0], self.previous_data[1])

    def store(self):
        pass  # TODO: update previous_data with current values

    @staticmethod
    def create(self, vertices: List[Tuple[int, str]], edges: List[Tuple[int, int, str]]):
        self.vertices_dict = {}
        self.label_dict = {}
        for idx, label in vertices:
            self.vertices_dict[idx] = Vertex(idx, label)
            self.label_dict[label] = []

        for idx, label in vertices:
            self.label_dict[label].append(self.vertices_dict[idx])

        for out_vertex, in_vertex, label in edges:
            self.vertices_dict[out_vertex].add_out_edge(Edge(out_vertex, in_vertex, label))
            self.vertices_dict[in_vertex].add_in_edge(Edge(out_vertex, in_vertex, label))

    def __str__(self):
        tmp = "vertices: "
        for i in self.vertices_dict:
            tmp += str(self.vertices_dict[i])
        tmp += "labels: "
        tmp += str(self.label_dict)
        return tmp

    def get_graph(self, bg_color):
        g = graphviz.Digraph(self.name, format='png')
        g.attr(rankdir='LR', size='10', bgcolor=bg_color)
        for i in self.vertices_dict:
            g.node(str(i), label=f"{self.vertices_dict[i].label},{self.vertices_dict[i].idx}")
            for j in self.vertices_dict[i].out_edges:
                g.edge(str(i), str(j.in_vertex), label=j.label)
        return g.pipe(format='png')

    @staticmethod
    def is_input_valid(input_data: str) -> bool:
        if "\n" not in input_data:
            return False
        s = input_data.replace('\n', '\n ')
        s = s.split(' ')
        i = 0
        s1 = []
        s2 = []
        while True:
            s1.append(s[i])
            if s[i][-1] == '\n':
                i += 1
                break
            i += 1
        while i < len(s):
            s2.append(s[i])
            i += 1
        s = input_data.replace('\n', '\n ')
        s = s.split(' ')
        flag = True
        if len(s1) % 2 != 0:
            return False
        if len(s2) % 3 != 0:
            return False
        for i in range(len(s1)):
            if (i + 1) % 2 != 0 and s1[i][-1] != ',':
                flag = False
                break
            if (i + 1) % 2 == 0 and i < len(s1) - 2 and s[i][-1] != ";":
                print(i)
                flag = False
                break
            if i == len(s1) - 1 and s[i][-1] != "\n":
                flag = False
                break
        if not flag:
            return flag
        for i in range(len(s2)):
            if (i + 1) % 3 != 0 and s2[i][-1] != ',':
                flag = False
                break
            if (i + 1) % 3 == 0 and i < len(s2) - 1 and s2[i][-1] != ";":
                flag = False
                break
        return flag

    @staticmethod
    def parse(input_data: str) -> Tuple[List[Tuple[int, str]], List[Tuple[int, int, str]]]:
        """ Parses graph

        :param input_data:  "index, label\n index1, index2, label_e;"
        :return: [[(vertex_index, vertex_label)],[(vertex1_index, vertex2_index, edge_label)]]
        """
        s = input_data.replace('\n', '\n ')
        s = s.split(' ')
        i = 0
        s1 = []
        s2 = []
        while True:
            if i >= len(s):
                return Graph.parse_vertices(s1), []
            if s[i][-1] == '\n':
                s1.append(s[i][:-1])
                i += 1
                break
            s1.append(s[i])
            i += 1
        while i < len(s):
            s2.append(s[i])
            i += 1
        return Graph.parse_vertices(s1), Graph.parse_edges(s2)

    @staticmethod
    def parse_vertices(input_data: List[str]) -> List[Tuple[int, str]]:
        """ Parses vertices

        :param input_data: "index, label;"
        :return: [(vertex_index, vertex_label)]
        """
        return [(int(input_data[i][:-1]), input_data[i + 1][:-1]) for i in range(0, len(input_data), 2)]

    @staticmethod
    def parse_edges(input_data: List[str]) -> List[Tuple[int, int, str]]:
        """ Parses edges


        :param input_data: "index1, index2, label_e;"
        :return: [(vertex1_index, vertex2_index, edge_label)]
        """
        return [(int(input_data[i][:-1]), int(input_data[i + 1][:-1]), input_data[i + 2][:-1]) for i in range(0, len(input_data), 3)]

    def add_vertex(self, vertex):
        self.vertices_dict[vertex.idx] = vertex
        if vertex.label not in self.label_dict:
            self.label_dict[vertex.label] = []
        self.label_dict[vertex.label].append(self.vertices_dict[vertex.idx])

    def add_edge(self, edge):
        self.vertices_dict[edge.out_vertex].add_out_edge(edge)
        self.vertices_dict[edge.in_vertex].add_in_edge(edge)

    def remove_edge(self, edge):
        self.vertices_dict[edge.out_vertex].remove_out_edge(edge)
        self.vertices_dict[edge.in_vertex].remove_in_edge(edge)

    def remove_vertex(self, vertex_id):
        vertex = self.vertices_dict[vertex_id]
        for edge in vertex.out_edges:
            self.vertices_dict[edge.out_vertex].remove_in_edge(edge)

        for edge in vertex.in_edges:
            self.vertices_dict[edge.in_vertex].remove_out_edge(edge)

        self.label_dict[vertex.label].remove(vertex)
        del self.vertices_dict[vertex_id]
