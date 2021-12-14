import fileinput


class Node:
    idx = 0
    k = 0
    parent_indexes = []

    def __init__(self):
        self.probability_table = []


class TableRow:
    values = []
    probabilities = []

    def __init__(self, v, p):
        self.values = [int(numeric_string) for numeric_string in v]
        self.probabilities = [float(numeric_string) for numeric_string in p]


class Expedience:
    def __init__(self, var_value, decision, expedience_value):
        self.var_value = var_value
        self.decision = decision
        self.expedience_value = expedience_value


def normalize(q):
    sum = 0
    for i in range(len(q)):
        sum += q[i]

    for i in range(len(q)):
        q[i] = q[i] / sum

    return q


def evident_values(y_idx, e):
    value = e[y_idx]
    if value is not None:
        return value
    else:
        return -1


def get_p(Y, y_value, e):
    parent_vals = []
    for i in range(len(Y.parent_indexes)):
        parent_vals.append(evident_values(Y.parent_indexes[i], e))

    if not Y.parent_indexes:
        return Y.probability_table[0].probabilities[y_value]

    for t in range(len(Y.probability_table)):
        matches = 0
        for i in range(len(Y.probability_table[t].values)):
            if Y.probability_table[t].values[i] == parent_vals[i]:
                matches += 1
            else:
                break
        if matches == len(Y.parent_indexes):
            return Y.probability_table[t].probabilities[y_value]


def list_all(bn, e):
    if not bn:
        return 1.0

    Y = bn.pop(0)
    y_value = evident_values(Y.idx, e)
    if y_value != -1:
        return get_p(Y, y_value, e) * list_all(bn.copy(), e.copy())
    else:
        prob_sum = 0
        for i in range(Y.k):
            new_e = e.copy()
            new_e[Y.idx] = i

            prob_sum += get_p(Y, i, e) * list_all(bn.copy(), new_e)

        return prob_sum


def list_ask(X, e, bn):
    Q = [None] * X.k

    temp_e = e.copy()
    for x_val in range(X.k):
        temp_e[X.idx] = x_val
        Q[x_val] = list_all(bn.copy(), temp_e)

    return normalize(Q)


def expected_expediences(Q, expediencies, d):
    result = []
    for i in range(d):
        expected_expedience = 0
        for e in range(len(expediencies)):
            if expediencies[e].decision == i:
                expected_expedience += Q[expediencies[e].var_value] * expediencies[e].expedience_value
        result.append(expected_expedience)

    return result


# files=r'C:\projects\ai\hazi2\mi-bayes-halo\examples_mihf_decisionnet_2021\input2.txt'
with fileinput.input() as f:
    num_of_nodes = int(f.readline().rstrip())

    nodes = [Node() for i in range(num_of_nodes)]

    for i in range(num_of_nodes):
        attributes = f.readline().rstrip().split("\t")

        nodes[i].idx = i
        nodes[i].k = int(attributes[0])
        num_indexes = int(attributes[1])
        parent_indexes = []

        # read parent index values
        for j in range(num_indexes):
            parent_indexes.append(int(attributes[j + 2]))

        nodes[i].parent_indexes = parent_indexes

        # read parents values
        for j in range(len(attributes) - num_indexes - 2):
            v_p_array = attributes[num_indexes + 2 + j].split(":")
            v = []
            p = []
            if len(v_p_array) == 1:
                p = v_p_array[0].split(",")
            else:
                v = v_p_array[0].split(",")
                p = v_p_array[1].split(",")
            nodes[i].probability_table.append(TableRow(v, p))

    num_of_evidency_var = int(f.readline().rstrip())
    evident_vars = [None] * num_of_nodes

    # read evidency variables
    for i in range(num_of_evidency_var):
        attributes = f.readline().rstrip().split("\t")
        evident_vars[int(attributes[0])] = int(attributes[1])

    index_of_goal_var = int(f.readline().rstrip())

    num_of_decisions = int(f.readline().rstrip())

    expediences = []

    for i in range(nodes[index_of_goal_var].k * num_of_decisions):
        attributes = f.readline().rstrip().split("\t")
        expediences.append(Expedience(int(attributes[0]), int(attributes[1]), float(attributes[2])))

    Q = list_ask(nodes[index_of_goal_var], evident_vars, nodes)

    for i in range(len(Q)):
        print(Q[i])

    expected_e = expected_expediences(Q, expediences, num_of_decisions)

    print(expected_e.index(max(expected_e)))
