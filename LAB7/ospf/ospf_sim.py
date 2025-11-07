import networkx as nx
import matplotlib
matplotlib.use('Agg') # Use a non-GUI backend
import matplotlib.pyplot as plt
import heapq

def draw_graph_with_costs(graph, pos, title):
    """Helper function to draw the network graph with link costs."""
    plt.figure(figsize=(12, 8))
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=2500, font_size=16, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='darkred')
    plt.title(title)
    
    filename = "ospf_topology.png" 
    plt.savefig(filename) 
    print(f"\n*** Graph saved to {filename} ***") 
    plt.close() 

def draw_spt(graph, spt_edges, pos, router_name, title):
    """Helper function to draw a specific router's Shortest Path Tree."""
    plt.figure(figsize=(12, 8))
    
    nx.draw(graph, pos, with_labels=True, node_color='gray', node_size=2000, font_size=14, alpha=0.3)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='gray', alpha=0.3)
    
    spt_nodes = set([router_name])
    for u, v in spt_edges:
        spt_nodes.add(u)
        spt_nodes.add(v)
        
    nx.draw_networkx_nodes(graph, pos, nodelist=spt_nodes, node_color='skyblue', node_size=2500)
    nx.draw_networkx_labels(graph, pos, font_size=16, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edgelist=spt_edges, edge_color='blue', width=2.5)
    
    nx.draw_networkx_nodes(graph, pos, nodelist=[router_name], node_color='tomato', node_size=3000)
    
    plt.title(title)
    
    filename = f"ospf_spt_{router_name}.png" 
    plt.savefig(filename) 
    print(f"*** SPT graph saved to {filename} ***") 
    plt.close() 

def dijkstra(graph, start_node):
    """Implements Dijkstra's algorithm to find shortest paths."""
    
    pq = [(0, start_node, None)]
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {node: None for node in graph.nodes}
    spt_edges = []
    visited = set()

    while pq:
        cost, node, prev = heapq.heappop(pq)
        
        if node in visited:
            continue
            
        visited.add(node)
        
        if prev is not None:
            spt_edges.append((prev, node))

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                edge_data = graph.get_edge_data(node, neighbor)
                new_cost = cost + edge_data['weight']
                
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    predecessors[neighbor] = node
                    heapq.heappush(pq, (new_cost, neighbor, node))
                    
    return distances, predecessors, spt_edges

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


def simulate_ospf():
    """Simulates the Open Shortest Path First (OSPF) protocol."""
    
    print("--- Simulating OSPF (Dijkstra) ---")
    
    G = nx.Graph()
    edges = [
        ('A', 'B', 5), ('A', 'C', 4), ('A', 'D', 2),
        ('B', 'C', 3), ('B', 'F', 5),
        ('C', 'D', 2), ('C', 'E', 4),
        ('D', 'E', 7),
        ('E', 'F', 6)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    print(f"Network Nodes: {list(G.nodes)}")
    print(f"Network Links (with costs): {edges}\n")
    
    link_state_database = G
    print("Step 1: Link-State Advertisement (LSA) flooding simulated.")
    print("All routers now have a complete map (LSDB) of the network.\n")
    
    pos = nx.spring_layout(G)
    draw_graph_with_costs(G, pos, "OSPF Network Topology (Link Costs)")
    
    all_routing_tables = {}
    
    print("Step 2: Each router runs Dijkstra's algorithm to build its SPT.\n")
    
    for router_name in G.nodes:
        print(f"--- Router {router_name} Calculations ---")
        
        distances, predecessors, spt_edges = dijkstra(link_state_database, router_name)
        
        routing_table = build_routing_table(router_name, predecessors)
        for dest in routing_table:
            routing_table[dest]['cost'] = distances[dest]
            
        all_routing_tables[router_name] = routing_table
        
        print(f"Shortest Path Tree (SPT) for Router {router_name} (Edges): {spt_edges}")
        print(f"Routing Table for Router {router_name}:")
        print(f"  {'Destination':<12} | {'Next Hop':<10} | {'Total Cost':<10}")
        print("  " + "-"*40)
        for dest, info in sorted(routing_table.items()):
            print(f"  {dest:<12} | {info['next_hop']:<10} | {info['cost']:<10}")
        print()
        
        draw_spt(G, spt_edges, pos, router_name, f"Shortest Path Tree (SPT) for Router {router_name}")

if __name__ == "__main__":
    simulate_ospf()