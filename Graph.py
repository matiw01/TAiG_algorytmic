from typing import List, Tuple

import graphviz

from Edge import Edge
from Vertex import Vertex

Edge_decs = Tuple[int, int, str]
Vertex_desc = Tuple[int, str]


# assuming matrixGraph is matrix where each row is list of outgoing edges and collumn is list of  ingoing edges
# and labels is list of labels so labels[i] is label for vertex created of matrixGraph[i]
class Graph:
    def __init__(self, vertices: List[Vertex_desc], edges: List[Edge_decs], name: str):
        self.name = name
        self.previous_data = [vertices, edges]
        self.create(self, vertices, edges)

    def undo(self):
        self.create(self, self.previous_data[0], self.previous_data[1])

    @staticmethod
    def create(self, vertices: List[Vertex_desc], edges: List[Edge_decs]):
        self.verticesDict = {}
        self.labelDict = {}
        for idx, label in vertices:
            self.verticesDict[idx] = Vertex(idx, label)
            self.labelDict[label] = []

        for idx, label in vertices:
            self.labelDict[label].append(self.verticesDict[idx])

        for out_vertex, in_vertex, label in edges:
            self.verticesDict[out_vertex].add_out_edge(Edge(out_vertex, in_vertex, label))
            self.verticesDict[in_vertex].add_in_edge(Edge(out_vertex, in_vertex, label))

    def __str__(self):
        tmp = "vertices: "
        for i in self.verticesDict:
            tmp += str(self.verticesDict[i])
        tmp += "labels: "
        tmp += str(self.labelDict)
        return tmp

    def get_graph(self, bg_color):
        g = graphviz.Digraph(self.name, format='png')
        g.attr(rankdir='LR', size='10', bgcolor=bg_color)
        for i in self.verticesDict:
            g.node(str(i), label=self.verticesDict[i].label)
            for j in self.verticesDict[i].out_edges:
                g.edge(str(i), str(j.in_vertex), label=j.label)
        return g.pipe(format='png')

    @staticmethod
    def if_input_is_valid(input_data: str) -> bool:
        if "\n" not in input_data:
            return False
        S = input_data.replace('\n', '\n ')
        S = S.split(' ')
        i = 0
        S1 = []
        S2 = []
        while True:
            S1.append(S[i])
            if S[i][-1] == '\n':
                i += 1
                break
            i += 1
        while i < len(S):
            S2.append(S[i])
            i += 1
        S = input_data.replace('\n', '\n ')
        S = S.split(' ')
        flag = True
        if len(S1) % 2 != 0:
            return False
        if len(S2) % 3 != 0:
            return False
        for i in range(len(S1)):
            if (i + 1) % 2 != 0 and S1[i][-1] != ',':
                flag = False
                break
            if (i + 1) % 2 == 0 and i < len(S1) - 2 and S[i][-1] != ";":
                print(i)
                flag = False
                break
            if i == len(S1) - 1 and S[i][-1] != "\n":
                flag = False
                break
        if not flag:
            return flag
        for i in range(len(S2)):
            if (i + 1) % 3 != 0 and S2[i][-1] != ',':
                flag = False
                break
            if (i + 1) % 3 == 0 and i < len(S2) - 1 and S2[i][-1] != ";":
                flag = False
                break
        return flag

    @staticmethod  # input_data "index, label\n index1, index2, label_e;"
    def parse(input_data: str) -> Tuple[List[Vertex_desc], List[Edge_decs]]:
        # return [[(vertex_index, vertex_label)],[(vertex1_index, vertex2_index, edge_label)]]
        S = input_data.replace('\n', '\n ')
        S = S.split(' ')
        i = 0
        S1 = []
        S2 = []
        while True:
            if i >= len(S):
                return Graph.parseVertexes(S1), []
            if S[i][-1] == '\n':
                S1.append(S[i][:-1])
                i += 1
                break
            S1.append(S[i])
            i += 1
        while i < len(S):
            S2.append(S[i])
            i += 1
        return Graph.parseVertexes(S1), Graph.parseEdges(S2)

    @staticmethod  # input_data "index, label;"
    def parseVertexes(s: List[str]) -> List[Vertex_desc]:  # return [(vertex_index, vertex_label)]
        return [(int(s[i][:-1]), s[i + 1][:-1]) for i in range(0, len(s), 2)]

    @staticmethod  # input_data "index1, index2, label_e;"
    def parseEdges(s: List[str]) -> List[Edge_decs]:  # return [(vertex1_index, vertex2_index, edge_label)]
        return [(int(s[i][:-1]), int(s[i + 1][:-1]), s[i + 2][:-1]) for i in range(0, len(s), 3)]

    def add_vertex(self, vertex: Vertex):
        self.verticesDict[vertex.idx] = vertex
        if vertex.label not in self.labelDict:
            self.labelDict[vertex.label] = []
        self.labelDict[vertex.label].append(self.verticesDict[vertex.idx])

    def add_edge(self, edge: Edge):
        self.verticesDict[edge.out_vertex].add_out_edge(edge)
        self.verticesDict[edge.in_vertex].add_in_edge(edge)

    def remove_edge(self, edge: Edge):
        self.verticesDict[edge.out_vertex].remove_out_edge(edge)
        self.verticesDict[edge.in_vertex].remove_in_edge(edge)

    def remove_vertex(self, vertex_id: int):
        for edge in self.verticesDict[vertex_id].out_edges:
            self.verticesDict[edge.out_vertex].remove_in_edge(edge)

        for edge in self.verticesDict[vertex_id].in_edges:
            self.verticesDict[edge.in_vertex].remove_out_edge(edge)

        self.labelDict[self.verticesDict[vertex_id].label].remove(vertex_id)
        del self.verticesDict[vertex_id]
