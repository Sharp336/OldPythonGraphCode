import collections


class Graph(object):
    def __init__(self, edges):
        self.edges = edges
        self.adj = Graph._build_adjacency_list(edges)
        self.crack = []

    @staticmethod
    def _build_adjacency_list(edges):
        adj = collections.defaultdict(list)
        for edge in edges:
            adj[edge[0]].append(edge[1])
        return adj


def dfs(G):
    discovered = set()
    finished = set()

    for u in G.adj:
        if u not in discovered and u not in finished:
            discovered, finished = dfs_visit(G, u, discovered, finished)

def dfs_visit(G, u, discovered, finished):
    discovered.add(u)
    G.crack.append(u)

    for v in G.adj[u]:
        # Detect cycles
        if v in discovered:
            print(f"Найден цикл для {v} через {u}")
            G.crack.append([v, u])
            break

        # Recurse into DFS tree
        if v not in finished:
            dfs_visit(G, v, discovered, finished)

    discovered.remove(u)
    finished.add(u)

    return discovered, finished

graph = [('1', '2', 1), ('2', '3', 2), ('3', '4', 3), ('4', '5', 4), ('5', '2', 5), ('4', '1', 4)]
G = Graph(graph)
govno = {}
for i in graph:
    govno[i[0]+'_'+i[1]] = i[2]
print(govno)
dfs(G)
print(G.crack)
print(G.adj)
cycles = []
for i in G.crack:
    if len(i) > 1:
        start = G.crack.index(i[0])
        end = G.crack.index(i[1])
        print(start, end)
        cycle = G.crack[start:end] + [i[1]] + [i[0]]
        cycles.append(cycle)

result=[]
for cy in cycles:
    weight = 0
    length = len(cy)
    for i in range(length - 1): weight += govno[cy[i]+'_'+cy[i+1]]
    print(f'Найден цикл {cy} с весом {weight}')
    result.append([cy, weight])
result.sort(key = lambda x: x[1])
print(f'Кратчайший цикл - {result[0][0]} с весом {result[0][1]}')