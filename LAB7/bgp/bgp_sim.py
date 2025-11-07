import networkx as nx
import matplotlib
matplotlib.use('Agg') # Use a non-GUI backend
import matplotlib.pyplot as plt
import time

def draw_as_graph(graph, pos, title):
    """Helper function to draw the AS-level graph."""
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_color='lightgreen', node_size=3000, 
            font_size=18, font_weight='bold')
    plt.title(title)
    
    filename = "bgp_topology.png" 
    plt.savefig(filename) 
    print(f"\n*** Graph saved to {filename} ***") 
    plt.close() 

def simulate_bgp():
    """Simulates the Border Gateway Protocol (BGP) as a Path Vector protocol."""
    
    print("--- Simulating BGP (Path Vector) ---")
    
    ases = [100, 200, 300, 400]
    links = [(100, 200), (200, 300), (300, 400), (400, 100), (200, 400)]
    
    G = nx.Graph()
    G.add_edges_from(links)
    pos = nx.circular_layout(G)
    draw_as_graph(G, pos, "BGP AS-Level Topology")
    
    prefixes = {
        100: '10.1.0.0/16',
        200: '20.2.0.0/16',
        300: '30.3.0.0/16',
        400: '40.4.0.0/16'
    }
    
    rib = {asn: {} for asn in ases}
    
    for asn, prefix in prefixes.items():
        rib[asn][prefix] = {
            'as_path': [asn],
            'next_hop': 'self'
        }
        
    print(f"ASes: {ases}")
    print(f"AS Links: {links}\n")
    print("--- Simulating BGP UPDATEs ---")

    round_num = 0
    while True:
        round_num += 1
        print(f"--- BGP CONVERGENCE ROUND {round_num} ---")
        
        changed = False
        rib_snapshot = {asn: table.copy() for asn, table in rib.items()}

        for u_asn in ases:
            for v_asn in G.neighbors(u_asn):
                for prefix, info in rib_snapshot[u_asn].items():
                    if v_asn in info['as_path']:
                        continue 
                    
                    new_path = [u_asn] + info['as_path']
                    
                    if prefix not in rib[v_asn]:
                        rib[v_asn][prefix] = {
                            'as_path': new_path,
                            'next_hop': u_asn
                        }
                        changed = True
                    else:
                        current_path_len = len(rib[v_asn][prefix]['as_path'])
                        new_path_len = len(new_path)
                        
                        if new_path_len < current_path_len:
                            rib[v_asn][prefix] = {
                                'as_path': new_path,
                                'next_hop': u_asn
                            }
                            changed = True

        if not changed:
            print(f"\n*** BGP CONVERGENCE REACHED in {round_num} rounds. ***\n")
            break
            
        if round_num > 5:
            print("Reached max rounds, stopping.")
            break
            
        time.sleep(1)

    print("--- FINAL BGP ROUTING TABLES (RIBs) ---")
    for asn in ases:
        print(f"AS {asn}'s RIB:")
        print(f"  {'Prefix':<15} | {'Next Hop AS':<12} | {'AS_PATH':<20}")
        print("  " + "-"*50)
        for prefix, info in sorted(rib[asn].items()):
            path_str = " -> ".join(map(str, info['as_path']))
            print(f"  {prefix:<15} | {info['next_hop']:<12} | {path_str}")
        print()

if __name__ == "__main__":
    simulate_bgp()