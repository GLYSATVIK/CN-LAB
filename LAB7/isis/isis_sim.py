import networkx as nx
import matplotlib
matplotlib.use('Agg') # Use a non-GUI backend
import matplotlib.pyplot as plt
import heapq

def draw_graph_with_costs(graph, pos, title):
    """Helper function to draw the network graph with link costs."""
    plt.figure(figsize=(12, 8))
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color='lightcoral', node_size=2500, font_size=16, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='blue')
    plt.title(title)
    
    filename = "isis_topology.png" 
    plt.savefig(filename) 
    print(f"\n*** Graph saved to {filename} ***") 
    plt.close() 

def dijkstra(graph, start_node):
    """Implements Dijkstra's algorithm to find shortest paths."""
    
    pq = [(0, start_node, None)]
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {node: None for node in graph.nodes}
    visited = set()

    while pq:
        cost, node, prev = heapq.heappop(pq)
        
        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                edge_data = graph.get_edge_data(node, neighbor)
                new_cost = cost + edge_data['weight']
                
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    predecessors[neighbor] = node
                    heapq.heappush(pq, (new_cost, neighbor, node))
                    
    return distances, predecessors

def build_routing_table(start_node, predecessors):
    """Builds a routing table from Dijkstra's predecessors map."""
    table = {}
    for dest in predecessors:
        if dest == start_node:
            table[dest] = {'next_hop': '-', 'cost': 0}
            continue
            
        if predecessors[dest] is None:
            table[dest] = {'next_hop': '-', 'cost': float('inf')}
            continue

        curr = dest
        while predecessors[curr] is not None and predecessors[curr] != start_node:
            curr = predecessors[curr]
        
        table[dest] = {'next_hop': curr, 'cost': 0}
            
    return table

def simulate_is_is():
    """Simulates the IS-IS protocol (using Dijkstra)."""
    
    print("--- Simulating IS-IS (Link-State / Dijkstra) ---")
    
    G = nx.Graph()
    edges = [
        ('R1', 'R2', 10), ('R1', 'R3', 5),
        ('R2', 'R3', 2), ('R2', 'R4', 1),
        ('R3', 'R2', 2), ('R3', 'R4', 9), ('R3', 'R5', 2),
        ('R4', 'R5', 4),
        ('R5', 'R1', 7)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    print(f"Network Nodes: {list(G.nodes)}")
    print(f"Network Links (with metrics): {edges}\n")
    
    link_state_database = G
    print("Step 1: Link-State PDU (LSP) flooding simulated.")
    print("All routers now have a complete map (LSDB) of the network.\n")
    
    pos = nx.spring_layout(G)
    draw_graph_with_costs(G, pos, "IS-IS Network Topology (Link Metrics)")
    
    all_routing_tables = {}
    
    print("Step 2: Each router runs Dijkstra's algorithm (IS-IS uses SPF).\n")
    
    for router_name in G.nodes:
        print(f"--- Router {router_name} Calculations ---")
        
        distances, predecessors = dijkstra(link_state_database, router_name)
        
        routing_table = build_routing_table(router_name, predecessors)
        for dest in routing_table:
            routing_table[dest]['cost'] = distances[dest]
            
        all_routing_tables[router_name] = routing_table
        
        print(f"Routing Table for Router {router_name}:")
        print(f"  {'Destination':<12} | {'Next Hop':<10} | {'Total Cost':<10}")
        print("  " + "-"*40)
        for dest, info in sorted(routing_table.items()):
            print(f"  {dest:<12} | {info['next_hop']:<10} | {info['cost']:<10}")
        print()

if __name__ == "__main__":
    simulate_is_is()