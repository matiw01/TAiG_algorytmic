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

    def show_graphs(self, idx):
        if len(self.graphs) > idx >= 0:
            self.graphs[idx].get_graph().view()

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

    def show_productions(self, idx):
        if len(self.productions) > idx >= 0:
            self.productions[idx].draw()

    def use_production(self, production, graph, pointed_vertexes):
        pass


# S, g1, g2 oraz g3 to są przykładowe ciągi zczytane przez gui. Są one nastepnie parsowane i tworzone są
# z nich odpowiednie struktury. Poniższy przykład jest mocno poglądowy

# S = """he, h, hi, ha;
# do, he, h, ha;
# do, he, h, do;"""

# S1 = """he, h, hi, ha;
# do, he, h, ha;
# do, he, h, do;"""
#
# print(Production.if_input_is_valid(S1))

# g1 = """1, a; 2, x; 3, 2; 4, asvae
# 1, 3, 3124; 1, 4, M; 2, 2, ab; 4, 2, :D; 2, 3, cds;"""
# g2 = """1, x
# 1, 1, ab;"""
# g3 = """1, x; 2, y
# 1, 2, ab; 2, 1, xy;"""

# g4 = """1, x; 2, y
# 1, 2, ab; 2, 1, xy;"""
#
# print(Graph.if_input_is_valid(g4))

# M = Main()
# M.add_graph(g1, "graf solo")
# M.show_graphs(0)
# M.add_production(g2, "graf lewej strony", g3, "graf prawej strony", S)
# M.show_productions(0)


# graphs[0].get_graph().view()
# productions[0].draw()
