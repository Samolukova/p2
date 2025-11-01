import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    gateway_edges = set()
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        if u.isupper() and not v.isupper():
            gateway_edges.add((u, v))
        elif v.isupper() and not u.isupper():
            gateway_edges.add((v, u))
    
    virus_pos = 'a'
    blocked = set()
    result = []
    while True:
        dist = bfs_distances(graph, virus_pos, blocked)
        gateways_with_dist = {
            node: d for node, d in dist.items() if node.isupper()
        }
        
        if not gateways_with_dist:
            break

        min_dist = min(gateways_with_dist.values())
        target_gateway = min(g for g, d in gateways_with_dist.items() if d == min_dist)

        candidates = []
        for neighbor in graph[target_gateway]:
            if not neighbor.isupper():
                edge = (target_gateway, neighbor)
                if edge not in blocked:
                    candidates.append(edge)
        
        if not candidates:
            break

        to_block = min(candidates, key=lambda x: (x[0], x[1]))
        result.append(f"{to_block[0]}-{to_block[1]}")
        blocked.add(to_block)

        virus_pos = find_virus_next_move(graph, virus_pos, blocked)

        if len(result) > 100:
            break

    return result


def bfs_distances(graph, start, blocked):
    blocked_set = set()
    for g, u in blocked:
        blocked_set.add((g, u))
        blocked_set.add((u, g))

    def can_go(u, v):
        return (u, v) not in blocked_set

    dist = {}
    queue = deque([start])
    dist[start] = 0

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist and can_go(u, v):
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

def find_virus_next_move(graph, current, blocked):
    dist = bfs_distances(graph, current, blocked)
    gateways = {node: d for node, d in dist.items() if node.isupper()}
    if not gateways:
        return current

    min_d = min(gateways.values())
    target = min(g for g, d in gateways.items() if d == min_d)
    dist_from_target = bfs_distances_from_target(graph, target, blocked)
    
    next_candidates = []
    for nb in sorted(graph[current]):
        if (current, nb) in [(g, u) for g, u in blocked] or (nb, current) in [(g, u) for g, u in blocked]:
            continue
        if dist_from_target.get(nb, float('inf')) == dist_from_target.get(current, float('inf')) - 1:
            next_candidates.append(nb)

    if next_candidates:
        return min(next_candidates)
    else:
        return current

def bfs_distances_from_target(graph, start, blocked):
    return bfs_distances(graph, start, blocked)

def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)

if __name__ == "__main__":
    main()