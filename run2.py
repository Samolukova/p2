import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    virus = "a"
    blocked = set()
    result = []
    
    while True:
        gateway_conns = []
        for node in graph:
            if node.isupper():
                for neighbor in graph[node]:
                    if not neighbor.isupper():
                        edge_str = f"{node}-{neighbor}"
                        if (node, neighbor) not in blocked:
                            gateway_conns.append(edge_str)
        
        if not gateway_conns:
            break
            
        dist, prev = bfs(graph, virus, blocked)
        
        gateways = [n for n in dist if n.isupper()]
        if not gateways:
            break
            
        min_dist = min(dist[g] for g in gateways)
        target_gw = min(g for g in gateways if dist[g] == min_dist)
        
        immediate_threat = None
        for neighbor in graph[virus]:
            if neighbor.isupper() and (virus, neighbor) not in blocked:
                immediate_threat = f"{neighbor}-{virus}"
                break
        
        if immediate_threat:
            result.append(immediate_threat)
            g, n = immediate_threat.split('-')
            blocked.add((g, n))
            blocked.add((n, g))
            continue
        
        if dist[target_gw] > 1:
            path = []
            current = target_gw
            while current != virus:
                path.append(current)
                current = prev[current]
            path.reverse()
            virus_next = path[0] if path else virus
        else:
            virus_next = virus
        
        gateway_conns.sort()
        to_block = gateway_conns[0]
        result.append(to_block)
        g, n = to_block.split('-')
        blocked.add((g, n))
        blocked.add((n, g))
        virus = virus_next
    
    return result

def bfs(graph, start, blocked):
    dist = {start: 0}
    prev = {}
    q = deque([start])
    
    while q:
        u = q.popleft()
        for v in graph[u]:
            if (u, v) in blocked or (v, u) in blocked:
                continue
            if v not in dist:
                dist[v] = dist[u] + 1
                prev[v] = u
                q.append(v)
    
    return dist, prev

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