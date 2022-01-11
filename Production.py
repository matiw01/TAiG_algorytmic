# expected_format = '[([(s1, out, 1, 2, 3), (ai, out, 1, 2)], [(0, A, M, in), (0, A, N, out)]), ' \
#     '([(s1, out, 1, 2, 3), (ai, out, 1, 4)], [(0, A, M, in), (0, A, N, out)]), ' \
#     '([(s1, out, 1, 2, 5), (ai, out, 1, 6)], [(0, A, M, in), (0, A, N, out)])]'

class Production:
    def __init__(self, left_graph, right_graph, attachment):
        self.operations = []
        self.left_graph = left_graph
        self.right_graph = right_graph
        self.attachment = attachment

    def draw(self):
        # self.left_graph.get_graph().view()
        # self.right_graph.get_graph().view()
        print(self.attachment)

    @staticmethod
    def if_input_is_valid(input_data):
        S = input_data.replace('\n', '\n ')
        S = S.split(' ')
        print(S)
        flag = True
        if len(S) % 4 != 0:
            return False
        for i in range(len(S)):
            if (i + 1) % 4 != 0 and S[i][-1] != ',':
                flag = False
                break
            if (i + 1) % 4 == 0 and i < len(S) - 1 and S[i][-2:] != ";\n":
                flag = False
                break
        return flag

    # input format:
    # """edge_label, direction, index_left; ver_right_label, ver_g_label, edge_label, direction;
    # edge_label, direction, index_left; ver_right_label, ver_g_label, edge_label, direction;"""
    # format after parse:
    # [[[edge_label, direction, index_left], [ver_right_label, ver_g_label, edge_label, direction]],
    # [[edge_label, direction, index_left], [ver_right_label, ver_g_label, edge_label, direction]]]
    @staticmethod
    def parse(input_data):
        S = input_data[:-1]
        S = S.replace('\n', ' ')
        S = S.split('; ')
        for i in range(len(S)):
            S[i] = S[i].split(', ')
        V = [[]]
        idx = 0
        idxV = 0
        while idx < len(S):
            if len(S[idx]) == 3 and idx > 0:
                V.append([])
                idxV += 1
            V[idxV].append(S[idx])
            idx += 1
        return V

# if __name__ == '__main__':
#     Prod = Production()
#     Prod.parseProduction(expected_format)
#     for op in Prod.operations:
#         print(op)
