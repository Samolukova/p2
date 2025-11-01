import sys
from collections import deque, defaultdict

def bfs(graph, start, blocked):
    dist = {start: 0}
    prev = {}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in sorted(graph[u]):
            if (u, v) in blocked or (v, u) in blocked:
                continue
            if v not in dist:
                dist[v] = dist[u] + 1
                prev[v] = u
                q.append(v)
    return dist, prev

def find_path(prev, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return path

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    virus = "a"
    blocked = set()
    result = []

    while True:
        dist, prev = bfs(graph, virus, blocked)
        gateways = [node for node in dist if node.isupper()]
        if not gateways:
            break

        min_dist = min(dist[g] for g in gateways)
        target_gateway = min(g for g in gateways if dist[g] == min_dist)

        for nb in sorted(graph[virus]):
            if nb.isupper() and (virus, nb) not in blocked and (nb, virus) not in blocked:
                result.append(f"{nb}-{virus}")
                blocked.add((nb, virus))
                blocked.add((virus, nb))
                break
        else:
            path = find_path(prev, virus, target_gateway)
            if len(path) < 2:
                break
            next_virus = path[1]

            cut_edges = []
            for g in graph[next_virus]:
                if g.isupper() and (g, next_virus) not in blocked:
                    cut_edges.append(f"{g}-{next_virus}")
            if cut_edges:
                cut = min(cut_edges)
                g, n = cut.split('-')
                blocked.add((g, n))
                blocked.add((n, g))
                result.append(cut)

            virus = next_virus

        dist2, _ = bfs(graph, virus, blocked)
        if not any(n.isupper() for n in dist2):
            break

    return result

def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))
    for e in solve(edges):
        print(e)

if __name__ == "__main__":
    main()
