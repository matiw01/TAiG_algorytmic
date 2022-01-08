from Vertex import Vertex

# assuming matrixGraph is matrix where each row is list of outgoing edges and collumn is list of  ingoing edges
# and labels is list of labels so labels[i] is label for vertex created of matrixGraph[i]
class Graph:
    def __init__(self, matrixGraph, labels):
        self.verticiesDict = {}
        self.labelDict = {}

        n = len(matrixGraph)
        for i in range(n):
            out_edges = []
            in_edges = []
            for j in range(n):
                if matrixGraph[i][j]:
                   out_edges.append(j)
                if matrixGraph[j][i]:
                    in_edges.append(j)
            self.verticiesDict[i] = Vertex(i, out_edges, in_edges, labels[i])
        for label in labels:
            self.labelDict[label] = []
        for i in range(n):
            self.labelDict[labels[i]].append(i)

    def __str__(self):
        tmp = "verticies: "
        for i in self.verticiesDict:
            tmp += str(self.verticiesDict[i])
        tmp += "labels: "
        tmp += str(self.labelDict)
        return tmp

    