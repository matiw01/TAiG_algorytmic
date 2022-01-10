class Edge:

    def __init__(self, out_vertex, in_vertex, label):
        self.out_vertex = out_vertex
        self.in_vertex = in_vertex
        self.label = label

    def __str__(self):
        return f"""{self.out_vertex}, {self.in_vertex}, {self.label}; """
