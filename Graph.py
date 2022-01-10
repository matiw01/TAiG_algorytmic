from Vertex import Vertex
from Edge import Edge

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

# v = [(1,"a"), (2,"a"), (3,"2"), (4,"sdasd")]
# e = [(1,3, "2231"), (1,4,"M")]
#
# print(Graph(v,e))