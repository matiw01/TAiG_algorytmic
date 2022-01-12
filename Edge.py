class Edge:

    def __init__(self, out_vertex: int, in_vertex: int, label: str):
        self.out_vertex = out_vertex
        self.in_vertex = in_vertex
        self.label = label

    def __str__(self):
        return f"""{self.out_vertex}, {self.in_vertex}, {self.label}; """
