from Edge import Edge


class Vertex:

    def __init__(self, idx: int, label: str, out_edges=None, in_edges=None):
        self.idx = idx
        self.label = label
        if out_edges is None:
            out_edges = []
        self.out_edges = out_edges
        if in_edges is None:
            in_edges = []
        self.in_edges = in_edges

    def __str__(self):
        str_out_edges = ""
        for edge in self.out_edges:
            str_out_edges += str(edge)
        str_in_edges = ""
        for edge in self.in_edges:
            str_in_edges += str(edge)

        return f"""
        idx: {self.idx}
        out_edges:  {str_out_edges}
        in_edges:  {str_in_edges}
        label:   {str(self.label)} 
        """

    def __eq__(self, other):
        return self.idx == other.idx and self.label == other.label and self.in_edges == other.in_edges and self.out_edges == other.out_edges

    def add_out_edge(self, edge: Edge):
        self.out_edges.append(edge)

    def add_in_edge(self, edge: Edge):
        self.in_edges.append(edge)

    def remove_out_edge(self, edge: Edge):
        self.out_edges.remove(edge)

    def remove_in_edge(self, edge: Edge):
        self.in_edges.remove(edge)
