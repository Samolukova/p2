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
        gateways = [n for n in dist if n.isupper()]
        if not gateways:
            break

        min_dist = min(dist[g] for g in gateways)
        target_gateway = min(g for g in gateways if dist[g] == min_dist)

        immediate = []
        for g in sorted(graph.keys()):
            if not g.isupper():
                continue
            for nb in sorted(graph[g]):
                if nb == virus and (g, nb) not in blocked:
                    immediate.append(f"{g}-{nb}")

        if not immediate:
            candidates = []
            for g in sorted(graph.keys()):
                if not g.isupper():
                    continue
                for nb in sorted(graph[g]):
                    if (g, nb) not in blocked and not nb.isupper():
                        candidates.append(f"{g}-{nb}")

            if not candidates:
                break

            to_block = min(candidates)
        else:
            to_block = min(immediate)

        g, n = to_block.split('-')
        blocked.add((g, n))
        blocked.add((n, g))
        result.append(to_block)

        dist2, prev2 = bfs(graph, virus, blocked)
        gateways2 = [node for node in dist2 if node.isupper()]
        if not gateways2:
            break
        min_dist2 = min(dist2[g] for g in gateways2)
        target2 = min(g for g in gateways2 if dist2[g] == min_dist2)
        path = find_path(prev2, virus, target2)
        if len(path) >= 2:
            virus = path[1]
        else:
            break

    return result

def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            a, _, b = line.partition('-')
            edges.append((a, b))
    for r in solve(edges):
        print(r)

if __name__ == "__main__":
    main()
