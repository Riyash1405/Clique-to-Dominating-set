import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

# Function to read graph from CSV file
def read_graph_from_csv(file_path):
    adj_matrix = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            adj_matrix.append([int(x) for x in row])
    G = nx.from_numpy_array(np.array(adj_matrix))
    return G

# Function to find a maximum clique (greedy approach)
def find_max_clique(G):
    vertices = list(G.nodes())
    clique = []
    candidates = vertices.copy()
    
    while candidates:
        # Choose vertex with maximum degree
        degrees = [(v, G.degree(v)) for v in candidates]
        v, _ = max(degrees, key=lambda x: x[1])
        clique.append(v)
        
        # Keep only vertices that are neighbors of v
        neighbors = set(G.neighbors(v))
        candidates = [u for u in candidates if u in neighbors or u == v]
        candidates.remove(v)
        
        # Check if remaining candidates form a clique
        if not candidates:
            break
        subgraph = G.subgraph(candidates)
        is_clique = all(subgraph.has_edge(u, w) for u in candidates for w in candidates if u < w)
        if not is_clique:
            clique.pop()
            break
    
    return clique

# Function to verify if a set is a clique
def verify_clique(G, clique):
    for u in clique:
        for v in clique:
            if u != v and not G.has_edge(u, v):
                return False
    return True

# Function to transform clique to dominating set
def clique_to_dominating_set(G, clique):
    dominating_set = clique.copy()
    covered = set(clique)
    for v in clique:
        covered.update(G.neighbors(v))
    
    # Add vertices to cover remaining nodes
    remaining = set(G.nodes()) - covered
    while remaining:
        best_vertex = None
        max_coverage = 0
        for v in G.nodes():
            if v not in dominating_set:
                new_coverage = set(G.neighbors(v)) & remaining
                new_coverage.add(v)
                if len(new_coverage) > max_coverage:
                    max_coverage = len(new_coverage)
                    best_vertex = v
        if best_vertex is None:
            break
        dominating_set.append(best_vertex)
        covered.add(best_vertex)
        covered.update(G.neighbors(best_vertex))
        remaining = set(G.nodes()) - covered
    
    return dominating_set

# Function to verify if a set is a dominating set
def verify_dominating_set(G, dom_set):
    covered = set(dom_set)
    for v in dom_set:
        covered.update(G.neighbors(v))
    return len(covered) == G.number_of_nodes()

# Function to transform dominating set to clique (if possible)
def dominating_set_to_clique(G, dom_set):
    # Induced subgraph of dominating set
    subgraph = G.subgraph(dom_set)
    if all(subgraph.has_edge(u, v) for u in dom_set for v in dom_set if u < v):
        return list(dom_set)
    return None  # Not a clique

# Function to visualize and save graph
def visualize_graph(G, highlighted_nodes=None, title="Graph", filename="graph.png"):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8))
    
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    # Highlight specific nodes
    if highlighted_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlighted_nodes, node_color='red', node_size=500)
    
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.title(title)
    plt.savefig(filename)
    plt.close()

# Main function
def main():
    # Read graph from CSV
    input_file = "graph_16_vertices.csv"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return
    
    G = read_graph_from_csv(input_file)
    
    # Visualize input graph
    visualize_graph(G, title="Input Graph", filename="input_graph.png")
    
    # Find clique
    clique = find_max_clique(G)
    print(f"Clique: {clique}")
    print(f"Is Clique Valid? {'Yes' if verify_clique(G, clique) else 'No'}")
    visualize_graph(G, highlighted_nodes=clique, title="Clique", filename="clique_graph.png")
    
    # Transform to dominating set
    dominating_set = clique_to_dominating_set(G, clique)
    print(f"Dominating Set: {dominating_set}")
    print(f"Is Dominating Set Valid? {'Yes' if verify_dominating_set(G, dominating_set) else 'No'}")
    visualize_graph(G, highlighted_nodes=dominating_set, title="Dominating Set", filename="dominating_set_graph.png")
    
    # Transform dominating set back to clique
    new_clique = dominating_set_to_clique(G, dominating_set)
    if new_clique:
        print(f"New Clique from Dominating Set: {new_clique}")
        print(f"Is New Clique Valid? {'Yes' if verify_clique(G, new_clique) else 'No'}")
    else:
        print("Dominating Set is not a clique.")

if __name__ == "__main__":
    main()