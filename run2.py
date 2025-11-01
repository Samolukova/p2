import sys
from collections import deque, defaultdict

def bfs_single(graph, start, blocked_set):
    dist = {}
    q = deque([start])
    dist[start] = 0
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist and (u, v) not in blocked_set:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    virus_pos = 'a'
    blocked = set()
    result = []

    while True:
        blocked_set = set()
        for g, n in blocked:
            blocked_set.add((g, n))
            blocked_set.add((n, g))
        
        dist_v = bfs_single(graph, virus_pos, blocked_set)
        gateways = {node: d for node, d in dist_v.items() if node.isupper()}
        if not gateways:
            break
            
        min_dist = min(gateways.values())
        target_gateway = min(g for g, d in gateways.items() if d == min_dist)
        
        candidates = []
        for neighbor in graph[target_gateway]:
            if neighbor.isupper():
                continue
            if (target_gateway, neighbor) not in blocked:
                candidates.append((target_gateway, neighbor))
                
        if not candidates:
            break
            
        to_block = min(candidates)
        result.append(f"{to_block[0]}-{to_block[1]}")
        blocked.add(to_block)
        
        blocked_set = set()
        for g, n in blocked:
            blocked_set.add((g, n))
            blocked_set.add((n, g))
            
        dist_v = bfs_single(graph, virus_pos, blocked_set)
        gateways = {node: d for node, d in dist_v.items() if node.isupper()}
        if not gateways:
            break
        min_dist = min(gateways.values())
        target_gateway = min(g for g, d in gateways.items() if d == min_dist)
        
        dist_g = bfs_single(graph, target_gateway, blocked_set)
        
        next_candidates = []
        for nb in sorted(graph[virus_pos]):
            if (virus_pos, nb) in blocked_set:
                continue
            if (nb in dist_v and nb in dist_g and 
            virus_pos in dist_g and dist_v[nb] == dist_v[virus_pos] + 1 and 
            dist_g[nb] == dist_g[virus_pos] - 1):
                    next_candidates.append(nb)
                    
        if next_candidates:
            virus_pos = next_candidates[0]
        else:
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
                
    result = solve(edges)
    for edge in result:
        print(edge)
if __name__ == "__main__":
    main()