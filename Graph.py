from Vertex import Vertex
from Edge import Edge
import graphviz


# assuming matrixGraph is matrix where each row is list of outgoing edges and collumn is list of  ingoing edges
# and labels is list of labels so labels[i] is label for vertex created of matrixGraph[i]
class Graph:
    def __init__(self, verticies, edges):
        self.verticiesDict = {}
        self.labelDict = {}

        for idx, label in verticies:
            self.verticiesDict[idx] = Vertex(idx, label)
            self.labelDict[label] = []

        for idx, label in verticies:
            self.labelDict[label].append(self.verticiesDict[idx])

        for out_vertex, in_vertex, label in edges:
            self.verticiesDict[out_vertex].add_out_edge(Edge(out_vertex, in_vertex, label))
            self.verticiesDict[in_vertex].add_in_edge(Edge(out_vertex, in_vertex, label))

    def __str__(self):
        tmp = "verticies: "
        for i in self.verticiesDict:
            tmp += str(self.verticiesDict[i])
        tmp += "labels: "
        tmp += str(self.labelDict)
        return tmp

    def draw(self):
        g = graphviz.Digraph("Graf", format='png')
        g.attr(rankdir='LR', size='40')
        for i in self.verticiesDict:
            g.node(str(i), label=self.verticiesDict[i].label)
            for j in self.verticiesDict[i].out_edges:
                g.edge(str(i), str(j.in_vertex), label=j.label)
        return g

    @staticmethod  # input_data "index, label;"
    def parseVertexes(input_data):  # return [(vertex_index, vertex_label)]
        S = input_data.split(' ')
        return [(S[i][:-1:], S[i + 1][:-1:]) for i in range(0, len(S), 2)]

    @staticmethod  # input_data "index1, index2, label_e;"
    def parseEdges(input_data):  # return [(vertex1_index, vertex2_index, edge_label)]
        S = input_data.split(' ')
        return [(S[i][:-1:], S[i + 1][:-1:], S[i + 2][:-1:]) for i in range(0, len(S), 3)]
