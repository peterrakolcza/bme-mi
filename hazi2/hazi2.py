import fileinput

class Node:
    def __init__(self):
        self.idx = 0
        self.k = 0
        self.parent_indexes = []
        self.prob_table = {}


def normalize(q):
    Sum = sum(q)

    for i in range(len(q)):
        q[i] = q[i] / Sum

    return q


def felsorol_mindent(bn, e):
    if not bn:
        return 1.0

    Y = bn.pop(0)
    y_value = e[Y.idx]

    if y_value != None:
        return getProbability(Y, y_value, e) * felsorol_mindent(bn.copy(), e.copy())
    else:
        prob_sum = 0
        for i in range(Y.k):
            temp = e.copy()
            temp[Y.idx] = i

            prob_sum += getProbability(Y, i, e) * felsorol_mindent(bn.copy(), temp)

        return prob_sum


def getProbability(Y, y_value, e):
    parent_values = []
    for i in range(len(Y.parent_indexes)):
        parent_values.append(e[Y.parent_indexes[i]])

    if not Y.parent_indexes:
        return Y.prob_table[tuple([])][y_value]

    return Y.prob_table[tuple(parent_values)][y_value]

def felsorolas_kerdezes(X, e, bn):
    Q = [None] * X.k

    temp = e.copy()
    for x_value in range(X.k):
        temp[X.idx] = x_value
        Q[x_value] = felsorol_mindent(bn.copy(), temp)

    return normalize(Q)


def expected_utilities(Q, expediencies, d):
    calculated_utilities = []
    for i in range(d):
        expected_utility = 0

        for key, e in expediencies.items():
            if key[1] == i:
                expected_utility += Q[key[0]] * e
        calculated_utilities.append(expected_utility)

    return calculated_utilities

#comment out for test inputs from file:
#with open(r'input2.txt') as f:
with fileinput.input() as f:
    numOfNodes = int(f.readline().rstrip())

    nodes = [Node() for i in range(numOfNodes)]

    for i in range(numOfNodes):
        read_items = f.readline().rstrip().split("\t")

        nodes[i].idx = i
        nodes[i].k = int(read_items[0])
        num_indexes = int(read_items[1])
        parent_indexes = []

        # read parent index values
        for j in range(num_indexes):
            parent_indexes.append(int(read_items[j + 2]))

        nodes[i].parent_indexes = parent_indexes

        # read parents values
        for j in range(len(read_items) - num_indexes - 2):
            temp = read_items[num_indexes + 2 + j].split(":")
            keys = []
            values = []
            if len(temp) == 1:
                values = temp[0].split(",")
            else:
                keys = temp[0].split(",")
                values = temp[1].split(",")

            values = list(map(float, values))
            keys = list(map(int, keys))
            
            nodes[i].prob_table[tuple(keys)] = values
            

    numOfEvidencyVariables = int(f.readline().rstrip())
    evidency_variables = [None] * numOfNodes

    # read evidency variables
    for i in range(numOfEvidencyVariables):
        read_items = f.readline().rstrip().split("\t")
        evidency_variables[int(read_items[0])] = int(read_items[1])

    indexOfGoalNode = int(f.readline().rstrip())

    numOfDecisions = int(f.readline().rstrip())

    utilities = {}

    for i in range(nodes[indexOfGoalNode].k * numOfDecisions):
        read_items = f.readline().rstrip().split("\t")
        utilities[tuple([int(read_items[0]), int(read_items[1])])] = float(read_items[2])

    #calculate
    Q = felsorolas_kerdezes(nodes[indexOfGoalNode], evidency_variables, nodes)

    for p in Q:
        print(p)

    #calculate best utility
    expected_decision = expected_utilities(Q, utilities, numOfDecisions)

    print(expected_decision.index(max(expected_decision)))