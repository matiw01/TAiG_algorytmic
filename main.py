from typing import List

from Edge import Edge
from Graph import Graph
from Production import Production, Direction
from Vertex import Vertex


class Main:
    def __init__(self):
        self.graphs = []
        self.productions = []

    def add_graph(self, graph: str, name: str):
        self.graphs.append(Graph(
            Graph.parse(graph)[0],
            Graph.parse(graph)[1],
            name))

    def add_production(self, graph_l: str, name_l: str, graph_r: str, name_r: str, attachment: str):
        self.productions.append(Production(
            Graph(
                Graph.parse(graph_l)[0],
                Graph.parse(graph_l)[1],
                name_l),
            Graph(
                Graph.parse(graph_r)[0],
                Graph.parse(graph_r)[1],
                name_r),
            Production.parse(attachment)))

    def show_production(self, idx: int):
        if len(self.productions) > idx >= 0:
            self.productions[idx].draw()

    def use_production(self, production: Production, graph: Graph, pointed_vertexes: List[int]):

        left_side_to_graph_vertex_id_map = dict()
        for i in range(0, len(pointed_vertexes), 2):
            left_side_to_graph_vertex_id_map[pointed_vertexes[i]] = pointed_vertexes[i + 1]

        right_side_to_graph_vertex_id_map = dict()
        indexes_of_vertices_from_right_side_in_graph = set()

        next_idx = max(graph.verticesDict.keys()) + 1

        for idx in production.right_graph.verticesDict:
            if idx in production.left_graph.verticesDict:
                right_side_to_graph_vertex_id_map[idx] = left_side_to_graph_vertex_id_map[idx]
                indexes_of_vertices_from_right_side_in_graph.add(left_side_to_graph_vertex_id_map[idx])

        # usuwanie wierzchołków, których nie ma w prawej stronie
        for idx in production.left_graph.verticesDict:
            if idx not in production.right_graph.verticesDict:
                graph.remove_vertex(left_side_to_graph_vertex_id_map[idx])

        # zmiana etykiety wierzchołków które z lewej na prawą stronę
        for idx in production.left_graph.verticesDict:
            if idx in production.right_graph.verticesDict:
                graph.verticesDict[left_side_to_graph_vertex_id_map[idx]].label = \
                    production.left_graph.verticesDict[idx].label

        # dodawanie wierzchołków, których nie ma w lewej stronie
        for idx in production.right_graph.verticesDict:
            if idx not in production.left_graph.verticesDict:
                new_idx = next_idx
                next_idx += 1
                right_side_to_graph_vertex_id_map[idx] = new_idx
                indexes_of_vertices_from_right_side_in_graph.add(new_idx)
                vertex = Vertex(new_idx, production.right_graph.verticesDict[idx].label)
                graph.add_vertex(vertex)

        left_side_edges = [edge for vertex in production.left_graph.verticesDict.values() for edge in vertex.in_edges]
        right_side_edges = [edge for vertex in production.right_graph.verticesDict.values() for edge in vertex.in_edges]

        # usuwanie krawędzi występujących w lewej stronie
        for edge in left_side_edges:
            g_edge = Edge(left_side_to_graph_vertex_id_map[edge.out_vertex],
                          left_side_to_graph_vertex_id_map[edge.in_vertex],
                          edge.label)
            graph.remove_edge(g_edge)

        # dodawanie krawędzi występujących w prawej stronie
        for edge in right_side_edges:
            g_edge = Edge(right_side_to_graph_vertex_id_map[edge.out_vertex],
                          right_side_to_graph_vertex_id_map[edge.in_vertex],
                          edge.label)
            graph.add_edge(g_edge)

        # wykonywanie operacji osadzenia
        for attachment in production.attachment:

            graph_in_idx = left_side_to_graph_vertex_id_map[attachment[0][2]]
            direction = attachment[0][1]
            label = attachment[0][0]

            added_edges = attachment[1:]

            left_side_to_graph_edges_to_process = graph.verticesDict[
                graph_in_idx].in_edges if direction == Direction.IN else \
                graph.verticesDict[graph_in_idx].out_edges

            for processed_edge in left_side_to_graph_edges_to_process:
                if processed_edge.label != label:
                    continue
                graph.remove_edge(processed_edge)

                for added_edge in added_edges:

                    right_vertices = [right_side_to_graph_vertex_id_map[i] for i in
                                      production.right_graph.labelDict[added_edge[0]]]
                    graph_vertices = [i for i in graph.labelDict[added_edge[1]] if
                                      i not in indexes_of_vertices_from_right_side_in_graph]

                    # add edges between all matching vertices
                    for right_vertex_id in right_vertices:
                        for graph_vertex_id in graph_vertices:

                            if added_edge[3] == Direction.IN:
                                graph.add_edge(Edge(right_vertex_id, graph_vertex_id, added_edge[2]))
                            else:
                                graph.add_edge(Edge(graph_vertex_id, right_vertex_id, added_edge[2]))


# format wejścia transformacji osadzenia:
# """edge_label, direction, index_left; ver_right_label, ver_g_label, edge_label, direction;
# edge_label, direction, index_left; ver_right_label, ver_g_label, edge_label, direction;"""
A1 = """s, out, 1; A, N, s, out; N, N, -n, in; N, N, n, in;"""
A2 = """s, out, 1; A, N, s, out; M, N, -a, in;
ai, out, 1; A, I, ai, out; M, I, -c, in;"""
A3 = """am, out, 1; A, M, am, out; E, M, -b, in;"""
A4 = """ae, out, 1; A, E, ae, out; I, E, -l, in;
am, out, 1; A, M, am, out; I, M, c, in;"""

# S = A4.replace('\n', ' ')
# S = S.split(';')
# for i in range(len(S)):
#     S[i] = S[i].split(', ')
# print(S)

g_l1 = """1, A;"""
g_r1 = """1, A; 2, N;
1, 2, s;"""
g_l2 = """1, A;"""
g_r2 = """1, A; 2, M;
1, 2, am;"""
g_l3 = """1, A;"""
g_r3 = """1, A; 2, E;
1, 2, ae;"""
g_l4 = """1, A;"""
g_r4 = """1, A; 2, I;
1, 2, ai;"""
grafs = [(g_l1, "g_l1", g_r1, "g_r1"),
         (g_l2, "g_l2", g_r2, "g_r2"),
         (g_l3, "g_l3", g_r3, "g_r3"),
         (g_l4, "g_l4", g_r4, "g_r4"),
         ]
osadzenia = [A1, A2, A3, A4]
M = Main()
for i in range(len(grafs)):
    M.add_production(grafs[i][0], grafs[i][1], grafs[i][2], grafs[i][3], osadzenia[i])
for i in range(len(grafs)):
    for j in range(2):
        M.add_graph(grafs[i][j * 2], grafs[i][j * 2 + 1])

# for i in range(len(M.productions)):
#     M.show_production(i)
