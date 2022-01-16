from typing import List
from copy import deepcopy

from Edge import Edge
from Graph import Graph
from Production import Production
from Vertex import Vertex


class Main:
    def __init__(self):
        self.graphs = []
        self.prev_graphs = []
        self.productions = []

    def add_graph(self, graph: str, name: str):
        self.graphs.append(Graph(
            Graph.parse(graph)[0],
            Graph.parse(graph)[1],
            name))
        self.prev_graphs.append(deepcopy(self.graphs[-1]))

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

    def use_production(self, production: Production, graph: Graph, pointed_vertexes: List[int], graph_number: int):
        # storing previous version of the graph
        self.prev_graphs[graph_number] = deepcopy(graph)

        graph.store()

        left_side_to_graph_vertex_id_map = dict()
        for i in range(0, len(pointed_vertexes), 2):
            left_side_to_graph_vertex_id_map[pointed_vertexes[i]] = pointed_vertexes[i + 1]
        set(left_side_to_graph_vertex_id_map.values())

        right_side_to_graph_vertex_id_map = dict()
        indexes_of_vertices_from_right_side_in_graph = set()

        next_idx = max(graph.vertices_dict.keys()) + 1

        for idx in production.right_graph.vertices_dict:
            if idx in production.left_graph.vertices_dict:
                right_side_to_graph_vertex_id_map[idx] = left_side_to_graph_vertex_id_map[idx]
                indexes_of_vertices_from_right_side_in_graph.add(left_side_to_graph_vertex_id_map[idx])

        # delete vertices, that are absent on right side
        for idx in production.left_graph.vertices_dict:
            if idx not in production.right_graph.vertices_dict:
                graph.remove_vertex(left_side_to_graph_vertex_id_map[idx])

        # add vertices, that are absent on left side
        for idx in production.right_graph.vertices_dict:
            if idx not in production.left_graph.vertices_dict:
                new_idx = next_idx
                next_idx += 1
                right_side_to_graph_vertex_id_map[idx] = new_idx
                indexes_of_vertices_from_right_side_in_graph.add(new_idx)
                vertex = Vertex(new_idx, production.right_graph.vertices_dict[idx].label)
                graph.add_vertex(vertex)

        left_side_edges = [edge for vertex in production.left_graph.vertices_dict.values() for edge in vertex.in_edges]
        right_side_edges = [edge for vertex in production.right_graph.vertices_dict.values() for edge in
                            vertex.in_edges]

        # delete vertices, that are present on left side
        for edge in left_side_edges:
            g_edge = Edge(left_side_to_graph_vertex_id_map[edge.out_vertex],
                          left_side_to_graph_vertex_id_map[edge.in_vertex],
                          edge.label)
            graph.remove_edge(g_edge)

        # add vertices, that are present on right side
        for edge in right_side_edges:
            g_edge = Edge(right_side_to_graph_vertex_id_map[edge.out_vertex],
                          right_side_to_graph_vertex_id_map[edge.in_vertex],
                          edge.label)
            graph.add_edge(g_edge)

        # do operation, that adds edges
        for operation in production.attachment:

            graph_in_idx = left_side_to_graph_vertex_id_map[operation[0][2]]
            direction = operation[0][1]
            label = operation[0][0]

            added_edges = operation[1:]

            left_side_to_graph_edges_to_process = graph.vertices_dict[graph_in_idx].in_edges if direction == 'in' else \
                graph.vertices_dict[graph_in_idx].out_edges
            left_side_to_graph_edges_to_process = list(
                filter(lambda x: x.label == label, left_side_to_graph_edges_to_process))

            for processed_edge in left_side_to_graph_edges_to_process:
                other_vertex_id = processed_edge.in_vertex if direction == 'out' else processed_edge.out_vertex
                if other_vertex_id in indexes_of_vertices_from_right_side_in_graph:
                    continue  # the edge must be into a vertex outside of 'mapped' left side

                graph.remove_edge(processed_edge)

                for added_edge in added_edges:

                    right_vertices = [right_side_to_graph_vertex_id_map[v.idx] for v in
                                      production.right_graph.label_dict[added_edge[0]]]
                    if graph.vertices_dict[other_vertex_id].label != added_edge[1]:
                        continue
                    # add edges between all matching vertices
                    for right_vertex_id in right_vertices:
                        if added_edge[3] == 'out':
                            graph.add_edge(Edge(right_vertex_id, other_vertex_id, added_edge[2]))
                        else:
                            graph.add_edge(Edge(other_vertex_id, right_vertex_id, added_edge[2]))


# 0 1
# 0 2
# 0 3
# 1 4
# 2 5
# 2 6
# 2 7
# 3 8
# 1 9
# 1 10
# 3 11
# 1 12
# 3 13
# 1 14
# 3 15
# 1 16
# 3 17
# 3 18

# Embedded transform input format:
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
graphs = [(g_l1, "g_l1", g_r1, "g_r1"),
          (g_l2, "g_l2", g_r2, "g_r2"),
          (g_l3, "g_l3", g_r3, "g_r3"),
          (g_l4, "g_l4", g_r4, "g_r4"),
          ]

embedment = [A1, A2, A3, A4]


def default(m=None):
    if m is None:
        m = Main()
    for i in range(len(graphs)):
        m.add_production(graphs[i][0], graphs[i][1], graphs[i][2], graphs[i][3], embedment[i])
    for i in range(len(graphs)):
        for j in range(2):
            m.add_graph(graphs[i][j * 2], graphs[i][j * 2 + 1])

    # for i in range(len(M.productions)):
    #     M.show_production(i)
    return m


M = default()
