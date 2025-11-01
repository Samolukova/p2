import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    virus_pos = "a"
    blocked = set()
    result = []
    
    while True:
        gateway_connections = []
        for node in sorted(graph.keys()):
            if node.isupper():
                for neighbor in sorted(graph[node]):
                    if not neighbor.isupper():
                        edge = (node, neighbor)
                        if edge not in blocked and (neighbor, node) not in blocked:
                            gateway_connections.append(f"{node}-{neighbor}")
        
        if not gateway_connections:
            break
        
        dist_from_virus, prev_from_virus = bfs(graph, virus_pos, blocked)
        
        reachable_gateways = [node for node in dist_from_virus if node.isupper()]
        if not reachable_gateways:
            break
        
        min_dist = min(dist_from_virus[g] for g in reachable_gateways)
        target_gateway = min(g for g in reachable_gateways if dist_from_virus[g] == min_dist)
        
        virus_next = None
        if dist_from_virus[target_gateway] == 1:
            connection_to_block = f"{target_gateway}-{virus_pos}"
            if connection_to_block in gateway_connections:
                result.append(connection_to_block)
                blocked.add((target_gateway, virus_pos))
                blocked.add((virus_pos, target_gateway))
                continue
            else:
                pass
        
        next_moves = []
        for neighbor in sorted(graph[virus_pos]):
            if (virus_pos, neighbor) in blocked or (neighbor, virus_pos) in blocked:
                continue
            dist_from_neighbor, _ = bfs(graph, neighbor, blocked)
            if target_gateway in dist_from_neighbor and dist_from_neighbor[target_gateway] == dist_from_virus[target_gateway] - 1:
                next_moves.append(neighbor)
        
        if next_moves:
            virus_next = min(next_moves)
        
        immediate_threats = []
        for conn in gateway_connections:
            g, n = conn.split('-')
            if n == virus_pos:
                immediate_threats.append(conn)
        
        if immediate_threats:
            connection_to_block = min(immediate_threats)
        else:
            connection_to_block = min(gateway_connections)
        
        result.append(connection_to_block)
        g, n = connection_to_block.split('-')
        blocked.add((g, n))
        blocked.add((n, g))
        
        if virus_next is not None:
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