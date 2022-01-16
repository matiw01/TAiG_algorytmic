class Production:

    def __init__(self, left_graph, right_graph, attachment):
        self.operations = []
        self.left_graph = left_graph
        self.right_graph = right_graph
        self.attachment = attachment

    def get_lr_graphs(self):
        return self.left_graph, self.right_graph

    @staticmethod
    def is_input_valid(input_data) -> bool:
        s = input_data.replace('\n', '\n ')
        s = s.split(' ')
        flag = True
        if len(s) % 4 != 0:
            return False
        for i in range(len(s)):
            if (i + 1) % 4 != 0 and s[i][-1] != ',':
                flag = False
                break
            if (i + 1) % 4 == 0 and i < len(s) - 1 and s[i][-2:] != ";\n":
                flag = False
                break
        return flag

    @staticmethod
    def parse(input_data: str):
        """ Parse a production.

        :param input_data:
        \"""edge_label, direction, index_left; ver_right_label, ver_g_label, edge_label, direction;
        edge_label, direction, index_left; ver_right_label, ver_g_label, edge_label, direction;\"""

        :return:
        [[[edge_label, direction, index_left], [ver_right_label, ver_g_label, edge_label, direction]],
        [[edge_label, direction, index_left], [ver_right_label, ver_g_label, edge_label, direction]]]
        """
        s = input_data[:-1]
        s = s.replace('\n', ' ')
        s = s.split('; ')
        for i in range(len(s)):
            s[i] = s[i].split(', ')
        v = [[]]
        idx = 0
        idx_v = 0
        while idx < len(s):
            if len(s[idx]) == 3 and idx > 0:
                v.append([])
                idx_v += 1
            v[idx_v].append(s[idx])
            idx += 1
        if len(v) == 0:
            return []
        return [[(operation[0][0], operation[0][1], int(operation[0][2]))] + \
                [(added_edge_desc[0], added_edge_desc[1], added_edge_desc[2], added_edge_desc[3])
                 for added_edge_desc in operation[1:]] for operation in v]
