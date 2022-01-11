from Graph import Graph
from Production import Production


class Main:
    def __init__(self):
        self.graphs = []
        self.productions = []

    def add_graph(self, graph, name):
        self.graphs.append(Graph(
            Graph.parse(graph)[0],
            Graph.parse(graph)[1],
            name))

    def add_production(self, graph_l, name_l, graph_r, name_r, attachment):
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

    def show_production(self, idx):
        if len(self.productions) > idx >= 0:
            self.productions[idx].draw()

    def use_production(self, production, graph, pointed_vertexes):
        pass


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
grafs = [(g_l1,"g_l1",g_r1,"g_r1"),
         (g_l2,"g_l2",g_r2,"g_r2"),
         (g_l3,"g_l3",g_r3,"g_r3"),
         (g_l4,"g_l4",g_r4,"g_r4"),
         ]
osadzenia = [A1,A2,A3,A4]
M = Main()
for i in range(len(grafs)):
    M.add_production(grafs[i][0],grafs[i][1],grafs[i][2],grafs[i][3],osadzenia[i])
for i in range(len(grafs)):
    for j in range(2):
        M.add_graph(grafs[i][j*2], grafs[i][j*2+1])

for i in range(len(M.productions)):
    M.show_production(i)