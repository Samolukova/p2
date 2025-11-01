import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    gateways = [node for node in graph if node.isupper()]
    
    virus_pos = "a"
    blocked = set()
    result = []
    
    while True:
        dist, _ = bfs(graph, virus_pos, blocked)
        
        reachable_gateways = [g for g in gateways if g in dist]
        if not reachable_gateways:
            break
            
        min_dist = min(dist[g] for g in reachable_gateways)
        target_gateway = min(g for g in reachable_gateways if dist[g] == min_dist)
        
        dist_from_target, prev_from_target = bfs(graph, target_gateway, blocked)
        
        current_neighbors = sorted(graph[virus_pos])
        next_candidates = []
        
        for neighbor in current_neighbors:
            if (virus_pos, neighbor) in blocked or (neighbor, virus_pos) in blocked:
                continue
            if neighbor in dist_from_target and dist_from_target[neighbor] == dist_from_target[virus_pos] - 1:
                next_candidates.append(neighbor)
        
        if not next_candidates:
            break
            
        virus_next = min(next_candidates)
        
        immediate_threat = False
        for neighbor in sorted(graph[virus_pos]):
            if neighbor.isupper() and (virus_pos, neighbor) not in blocked and (neighbor, virus_pos) not in blocked:
                result.append(f"{neighbor}-{virus_pos}")
                blocked.add((neighbor, virus_pos))
                blocked.add((virus_pos, neighbor))
                immediate_threat = True
                break
        
        if immediate_threat:
            continue
        
        gateway_connections = []
        for gateway in sorted(gateways):
            for neighbor in sorted(graph[gateway]):
                if (gateway, neighbor) not in blocked and (neighbor, gateway) not in blocked:
                    gateway_connections.append(f"{gateway}-{neighbor}")
        
        if not gateway_connections:
            break
            
        connection_to_block = min(gateway_connections)
        result.append(connection_to_block)
        g, n = connection_to_block.split('-')
        blocked.add((g, n))
        blocked.add((n, g))
        
        virus_pos = virus_next
    
    return result

def bfs(graph, start, blocked):
    dist = {start: 0}
    prev = {}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        for neighbor in sorted(graph[current]):
            if (current, neighbor) in blocked or (neighbor, current) in blocked:
                continue
            if neighbor not in dist:
                dist[neighbor] = dist[current] + 1
                prev[neighbor] = current
                queue.append(neighbor)
    
    return dist, prev

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