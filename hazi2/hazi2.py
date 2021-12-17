import re
import fileinput

def felsorol_mindent(nodes, evidents):
    if len(nodes) == 0:
        return 1.0

    Y = nodes.pop(0)
    probability = 0
    if isinstance(evidents[Y.position], type(None)):        
        for i in range(int(Y.k)):
            evidents_copy = evidents.copy()
            evidents_copy[Y.position] = i
            nodes_copy = nodes.copy()
            probability += calcProb(Y, evidents_copy) * felsorol_mindent(nodes_copy, evidents_copy)                
    else:
        probability = calcProb(Y, evidents.copy()) * felsorol_mindent(nodes.copy(), evidents.copy())

    return probability


def calcProb(Y, evidents):
    parent_values = []
    for i in range(Y.numOfParents):
        parent_values.append(evidents[int(Y.parents[i])])

    return Y.probs[tuple(parent_values)][evidents[Y.position]]

def felsorolas_kerdezes(X, e, nodes):
    Q = []
    for i in range(int(X.k)):
        e_copy = e.copy()
        nodes_copy = nodes.copy()
        e_copy[X.position] = i
        Q.append(felsorol_mindent(nodes_copy, e_copy))

    normalizedQ = []
    for i in range(int(X.k)):
        normalizedQ.append(Q[i] / sum(Q))        

    return normalizedQ


def best_utility(decisionNum, p, u):
    best_utility = 0
    best_utility_index = 0
    for key, e in u.items():
            if key[1] == 0:
                best_utility += p[key[0]] * e

    for i in range(decisionNum):
        utility = 0
        for key, e in u.items():
            if key[1] == i:
                utility += p[key[0]] * e
        
        if utility > best_utility:
            best_utility = utility
            best_utility_index = i

    return best_utility_index

def init(nodes, utilities, mainNode, decisionNum, evidencies):
    #comment out for test inputs from file:
    with fileinput.input() as stdin:
    #with open(r'input1.txt') as stdin:
        nodesNum = int(stdin.readline().rstrip())

        for node in range(nodesNum):
            raw_string = stdin.readline().rstrip()
            raw_nodes = [float(numeric_string) for numeric_string in re.split("\t|,|:", raw_string)]
            nodes.append(Node())
            position = node
            k = raw_nodes[0]
            numOfParents = int(raw_nodes[1])

            for p in range(numOfParents):
                index = p + 2
                nodes[node].parents.append(raw_nodes[index])

            item = 2 + int(raw_nodes[1])
            while item < len(raw_nodes):
                keys = []
                for j in range(numOfParents):
                    keys.append(raw_nodes[item + j])

                item += numOfParents

                values = []
                for j in range(int(k)):
                    values.append(raw_nodes[item + j])

                item += int(k)
                nodes[node].probs[tuple(keys)] = values

            nodes[node].position = position
            nodes[node].k = k
            nodes[node].numOfParents = numOfParents
          

        for _ in range(len(nodes)):
            evidencies.append(None)

        for _ in range(int(stdin.readline().rstrip())):
            raw_evidents = [int(numeric_string) for numeric_string in stdin.readline().rstrip().split("\t")]
            evidencies[raw_evidents[0]] = raw_evidents[1]

        mainNode = stdin.readline().rstrip()
        decisionNum = stdin.readline().rstrip()

        for _ in range(int(decisionNum)*int(nodes[int(mainNode)].k)):
            raw_decisions = [float(numeric_string) for numeric_string in stdin.readline().rstrip().split("\t")]
            utilities[tuple([int(raw_decisions[0]), int(raw_decisions[1])])] = raw_decisions[2]

        return nodes, utilities, int(mainNode), int(decisionNum), evidencies

class Node:
    def __init__(self):
        self.position = 0
        self.k = 0
        self.parents = []
        self.probs = {}
        self.numOfParents = 0

def main():
    nodes = []
    utilities = {}
    mainNode = 0
    decisionNum = 0
    evidencies = []

    nodes, utilities, mainNode, decisionNum, evidencies = init(nodes, utilities, mainNode, decisionNum, evidencies)

    #calculate
    Q = felsorolas_kerdezes(nodes[mainNode], evidencies, nodes)

    for p in Q:
        print(p)
    
    print(best_utility(decisionNum, Q, utilities))

if __name__ == "__main__":
    main()