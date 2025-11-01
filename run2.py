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

def is_reachable(graph, start, blocked):
    """Проверяет, можно ли добраться от start до шлюза."""
    dist, _ = bfs(graph, start, blocked)
    return any(n.isupper() for n in dist)

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

        # Если вирус рядом со шлюзом — сразу режем
        immediate = []
        for g in sorted(graph.keys()):
            if not g.isupper():
                continue
            for nb in sorted(graph[g]):
                if nb == virus and (g, nb) not in blocked:
                    immediate.append(f"{g}-{nb}")
        if immediate:
            cut = min(immediate)
            g, n = cut.split('-')
            blocked.add((g, n))
            blocked.add((n, g))
            result.append(cut)
        else:
            # иначе ищем все возможные отключения шлюзов
            possible = []
            for g in sorted(graph.keys()):
                if not g.isupper():
                    continue
                for nb in sorted(graph[g]):
                    if nb.isupper():
                        continue
                    if (g, nb) in blocked or (nb, g) in blocked:
                        continue
                    # проверяем: если отрежем это ребро, вирус всё ещё не достигнет шлюза?
                    tmp_blocked = set(blocked)
                    tmp_blocked.add((g, nb))
                    tmp_blocked.add((nb, g))
                    if is_reachable(graph, virus, tmp_blocked):
                        possible.append(f"{g}-{nb}")
            if not possible:
                break
            cut = min(possible)
            g, n = cut.split('-')
            blocked.add((g, n))
            blocked.add((n, g))
            result.append(cut)

        # Вирус двигается
        dist2, prev2 = bfs(graph, virus, blocked)
        gateways2 = [n for n in dist2 if n.isupper()]
        if not gateways2:
            break
        min_dist = min(dist2[g] for g in gateways2)
        target = min(g for g in gateways2 if dist2[g] == min_dist)
        path = find_path(prev2, virus, target)
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
    for e in solve(edges):
        print(e)

if __name__ == "__main__":
    main()
