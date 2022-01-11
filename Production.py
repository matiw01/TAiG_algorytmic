# expected_format = '[([(s1, out, 1, 2, 3), (ai, out, 1, 2)], [(0, A, M, in), (0, A, N, out)]), ' \
#     '([(s1, out, 1, 2, 3), (ai, out, 1, 4)], [(0, A, M, in), (0, A, N, out)]), ' \
#     '([(s1, out, 1, 2, 5), (ai, out, 1, 6)], [(0, A, M, in), (0, A, N, out)])]'

class Production:
    def __init__(self, left_graph, right_graph, attachment):
        self.operations = []
        self.left_graph = left_graph
        self.right_graph = right_graph
        self.attachment = attachment

    # def parseProduction(self, productions_to_parse: str):
    #     productions_to_parse = productions_to_parse.strip()
    #     productions_to_parse = productions_to_parse[3: -3]
    #
    #     operations_list = productions_to_parse.split("]), ([")
    #
    #     for operationStr in operations_list:
    #         operation = ([], [])
    #
    #         delete_operation_str = operationStr.split("], [")[0][1: -1]
    #         delete_operations_list = delete_operation_str.split("), (")
    #
    #         for single_delete in delete_operations_list:
    #             single_delete_list = single_delete.split(", ")
    #
    #             label = single_delete_list[0]
    #             direction = single_delete_list[1]
    #             highlighted_vertices = []
    #
    #             for v_str in single_delete_list[2:]:
    #                 highlighted_vertices.append(int(v_str))
    #
    #             operation[0].append((label, direction, highlighted_vertices))
    #
    #         add_operation_str = operationStr.split("], [")[1][1: -1]
    #         add_operations_list = add_operation_str.split("), (")
    #
    #         for single_add in add_operations_list:
    #             single_add_list = single_add.split(", ")
    #
    #             single_add_list[0] = int(single_add_list[0])
    #
    #             operation[1].append(tuple(single_add_list))
    #
    #         self.operations.append(operation)
    #
    # def make_production(self):
    #     pass

    # def __str__(self):

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
