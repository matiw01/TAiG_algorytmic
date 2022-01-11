from Graph import Graph
from Production import Production

graphs = []
productions = []

# S, g1, g2 oraz g3 to są przykładowe ciągi zczytane przez gui. Są one nastepnie parsowane i tworzone są
# z nich odpowiednie struktury. Poniższy przykład jest mocno poglądowy

S = """he, h, hi, ha; do, he, h, ha; do, he, h, do;"""

g1 = """1, a; 2, x; 3, 2; 4, asvae| 1, 3, 3124; 1, 4, M; 2, 2, ab; 4, 2, :D; 2, 3, cds;"""
g2 = """1, x| 1, 1, ab;"""
g3 = """1, x; 2, y| 1, 2, ab; 2, 1, xy;"""

graphs.append(Graph(
                Graph.parse(g1)[0],
                Graph.parse(g1)[1],
                "graf solo"))

graphs[0].get_graph().view()

productions.append(Production(
                Graph(
                    Graph.parse(g2)[0],
                    Graph.parse(g2)[1],
                    "graf lewej strony"),
                Graph(
                    Graph.parse(g3)[0],
                    Graph.parse(g3)[1],
                    "graf prawej strony"),
                Production.parse(S)))

productions[0].draw()
