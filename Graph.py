from Vertex import Vertex
from Edge import Edge
import graphviz


# assuming matrixGraph is matrix where each row is list of outgoing edges and collumn is list of  ingoing edges
# and labels is list of labels so labels[i] is label for vertex created of matrixGraph[i]
class Graph:
    def __init__(self, vertices, edges, name):
        self.verticesDict = {}
        self.labelDict = {}
        self.name = name

        for idx, label in vertices:
            self.verticesDict[idx] = Vertex(idx, label)
            self.labelDict[label] = []

        for idx, label in vertices:
            self.labelDict[label].append(self.verticesDict[idx])

        for out_vertex, in_vertex, label in edges:
            self.verticesDict[out_vertex].add_out_edge(Edge(out_vertex, in_vertex, label))
            self.verticesDict[in_vertex].add_in_edge(Edge(out_vertex, in_vertex, label))

    def __str__(self):
        tmp = "verticies: "
        for i in self.verticesDict:
            tmp += str(self.verticesDict[i])
        tmp += "labels: "
        tmp += str(self.labelDict)
        return tmp

    def get_graph(self):
        g = graphviz.Digraph(self.name, format='png')
        g.attr(rankdir='LR', size='10')
        for i in self.verticesDict:
            g.node(str(i), label=self.verticesDict[i].label)
            for j in self.verticesDict[i].out_edges:
                g.edge(str(i), str(j.in_vertex), label=j.label)
        return g

    @staticmethod  # input_data "index, label| index1, index2, label_e;"
    def parse(input_data):  # return [[(vertex_index, vertex_label)],[(vertex1_index, vertex2_index, edge_label)]]
        S = input_data.split(' ')
        i = 0
        S1 = []
        S2 = []
        while True:
            S1.append(S[i])
            if S[i][-1] == '|':
                i += 1
                break
            i += 1
        while i < len(S):
            S2.append(S[i])
            i += 1
        return [Graph.parseVertexes(S1), Graph.parseEdges(S2)]

    @staticmethod  # input_data "index, label;"
    def parseVertexes(s):  # return [(vertex_index, vertex_label)]
        return [(s[i][:-1], s[i + 1][:-1]) for i in range(0, len(s), 2)]

    @staticmethod  # input_data "index1, index2, label_e;"
    def parseEdges(s):  # return [(vertex1_index, vertex2_index, edge_label)]
        return [(s[i][:-1], s[i + 1][:-1], s[i + 2][:-1]) for i in range(0, len(s), 3)]
