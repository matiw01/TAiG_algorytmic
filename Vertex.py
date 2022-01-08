

class Vertex:

    def __init__(self, idx, out_edges, in_edges, label):
        self.idx = idx
        self.out_edges = out_edges
        self.in_edges = in_edges
        self.label = label

    def __str__(self):
        return "idx: " + str(self.idx) + " " + \
        "out_edges: " + str(self.out_edges) + " " + \
        "in_edges: " + str(self.in_edges) + " " + \
        "label: " + str(self.label) + " | "

    def add_out_edge(self, edge):
        self.out_edges.append(edge)

    def add_in_edge(self, edge):
        self.in_edges.append(edge)