import networkx as nx
import matplotlib
matplotlib.use('Agg') # Use a non-GUI backend
import matplotlib.pyplot as plt
import time

def draw_graph(graph, labels, pos, title):
    """Helper function to draw the network graph and save to file."""
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=16, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='red')
    plt.title(title)
    
    filename = "rip_topology.png" 
    plt.savefig(filename) 
    print(f"\n*** Graph saved to {filename} ***") 
    plt.close() 

def simulate_rip():
    """Simulates the Routing Information Protocol (RIP)."""
    
    # 1. Create a network topology
    nodes = ['A', 'B', 'C', 'D', 'E']
    edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D'), ('D', 'E')]
    
    network = {node: {} for node in nodes}
    for u, v in edges:
        network[u][v] = 1
        network[v][u] = 1

    tables = {node: {} for node in nodes}
    for node in nodes:
        tables[node][node] = {'next_hop': node, 'cost': 0}
        for neighbor in network[node]:
            tables[node][neighbor] = {'next_hop': neighbor, 'cost': 1}

    print("--- Simulating RIP (Bellman-Ford) ---")
    print(f"Network Nodes: {nodes}")
    print(f"Network Links (all cost 1): {edges}\n")

    # 3. Simulate periodic routing updates until convergence
    round_num = 0
    while True:
        round_num += 1
        print(f"--- ROUND {round_num} ---")
        
        changed = False
        tables_snapshot = {node: table.copy() for node, table in tables.items()}

        for u in nodes:
            for v in network[u]:
                neighbor_table = tables_snapshot[v]
                
                for dest in neighbor_table:
                    cost_to_neighbor = network[u][v]
                    cost_from_neighbor_to_dest = neighbor_table[dest]['cost']
                    new_cost = cost_to_neighbor + cost_from_neighbor_to_dest
                    
                    if new_cost > 15:
                        new_cost = 16 

                    if dest not in tables[u] or new_cost < tables[u][dest]['cost']:
                        tables[u][dest] = {'next_hop': v, 'cost': new_cost}
                        changed = True
                    elif tables[u].get(dest) and tables[u][dest]['next_hop'] == v and new_cost > tables[u][dest]['cost']:
                        tables[u][dest]['cost'] = min(new_cost, 16)
                        changed = True

        # Print tables for this round
        for node in nodes:
            print(f"Router {node} Table (Round {round_num}):")
            for dest, info in sorted(tables[node].items()):
                print(f"  -> Dest: {dest}, Next Hop: {info['next_hop']}, Cost: {info['cost']}")
        
        print("-" * 20)
        
        if not changed:
            print(f"\n*** CONVERGENCE REACHED in {round_num} rounds. ***\n")
            break
        
        if round_num > 10:
            print("Reached max rounds, stopping.")
            break
            
        time.sleep(1) 

    # 4. Display final routing tables
    print("--- FINAL CONVERGED ROUTING TABLES ---")
    for node in nodes:
        print(f"Router {node}'s Final Table:")
        for dest, info in sorted(tables[node].items()):
            print(f"  -> Dest: {dest}, Next Hop: {info['next_hop']}, Cost: {info['cost']}")
        print()

    # Visualization
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    labels = {(u, v): 1 for u, v in edges}
    draw_graph(G, labels, pos, "RIP Network Topology (All Link Costs = 1)")

if __name__ == "__main__":
    simulate_rip()