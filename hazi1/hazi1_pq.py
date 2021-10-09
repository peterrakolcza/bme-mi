import heapq
import math

def read(n, bemenet):
    for i in range(n):
        temp = input().split("\t")
        bemenet[i] = temp
        bemenet[i][0] = int(bemenet[i][0])
        bemenet[i][1] = int(bemenet[i][1])


def dijkstra(graph, starting_vertex, destination_vertex):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[starting_vertex] = 0

    pq = [(0, starting_vertex)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return round(distances[destination_vertex], 2)

def build_graph(edges, weights, e):
    graph = edges

    for i in range(e):
        graph[i].append(weights[i])
        
    return graph


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

graph2 = build_graph(utszakaszok, hosszak, e)
graph = { }
[graph.setdefault(i, []) for i in range(n)] 
for i in range(n):
    graph[i] = {}
for edge in graph2:
    graph[edge[0]].update({edge[1]: edge[2]})
    graph[edge[1]].update({edge[0]: edge[2]})

for i in range(p):
    if i == p - 1:
        print(dijkstra(graph, pontparok[i][0], pontparok[i][1]))
    else:
        print(dijkstra(graph, pontparok[i][0], pontparok[i][1]), end="\t")