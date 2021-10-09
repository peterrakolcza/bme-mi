import sys
import math
 
class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    def minDistance(self, dist, sptSet):
 
        min = sys.maxsize
 
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    def dijkstra(self, src, dest):
 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            u = self.minDistance(dist, sptSet)
 
            sptSet[u] = True
 
            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
 
        return round(dist[dest], 2)
 
def build_graph(edges, weights, e):
    graph = edges

    for i in range(e):
        graph[i].append(weights[i])
        
    return graph

def read(n, bemenet):
    for i in range(n):
        temp = input().split("\t")
        bemenet[i] = temp
        bemenet[i][0] = int(bemenet[i][0])
        bemenet[i][1] = int(bemenet[i][1])

# Driver program
p = int(input())
n = int(input())
e = int(input())
input()

pontparok = [[0] * 2] * p
csucsok = [[0] * 2] * n
utszakaszok = [[0] * 2] * e
hosszak = [0] * e

read(p, pontparok)
input()
read(n, csucsok)
input()
read(e, utszakaszok)

for i in range(e):
    hosszak[i] = math.sqrt(pow((csucsok[utszakaszok[i][0]][0] - csucsok[utszakaszok[i][1]][0]), 2) + pow((csucsok[utszakaszok[i][0]][1] - csucsok[utszakaszok[i][1]][1]), 2))

graph1 = build_graph(utszakaszok, hosszak, e)
graph2 = [[0 for _ in range(n)] for _ in range(n)]

for edge in graph1:
    graph2[edge[0]][edge[1]] = edge[2]
    graph2[edge[1]][edge[0]] = edge[2]

g = Graph(n)
g.graph = graph2
 
for i in range(p):
    if i == p - 1:
        print(g.dijkstra(pontparok[i][0], pontparok[i][1]))
    else:
        print(g.dijkstra(pontparok[i][0], pontparok[i][1]), end="\t")