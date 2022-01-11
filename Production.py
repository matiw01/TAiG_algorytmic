# expected_format = '[([(s1, out, 1, 2, 3), (ai, out, 1, 2)], [(0, A, M, in), (0, A, N, out)]), ' \
#     '([(s1, out, 1, 2, 3), (ai, out, 1, 4)], [(0, A, M, in), (0, A, N, out)]), ' \
#     '([(s1, out, 1, 2, 5), (ai, out, 1, 6)], [(0, A, M, in), (0, A, N, out)])]'

class Production:
    def __init__(self, left_graph, right_graph, to):
        self.operations = []
        self.left_graph = left_graph
        self.right_graph = right_graph
        self.to = to

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
        self.left_graph.get_graph().view()
        self.right_graph.get_graph().view()
        print(self.to)

    @staticmethod  # input_data "label_p, label_g, label_e, direction;"
    def parse(input_data):  # return [(label_vertex_right_graph, label_vertex_rest_graph, label_edge, direction)]
        S = input_data.split(' ')
        return [(S[i][:-1], S[i + 1][:-1], S[i + 2][:-1], S[i + 3][:-1]) for i in range(0, len(S), 4)]


# if __name__ == '__main__':
#     Prod = Production()
#     Prod.parseProduction(expected_format)
#     for op in Prod.operations:
#         print(op)

