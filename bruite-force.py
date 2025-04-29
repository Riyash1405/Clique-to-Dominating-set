import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
import os

# Function to read adjacency matrix from CSV
def read_graph_from_csv(filename):
    try:
        # Read CSV as a matrix (16x16, no header)
        df = pd.read_csv(filename, header=None)
        if df.shape != (16, 16):
            raise ValueError(f"Expected 16x16 adjacency matrix, got shape {df.shape}")
        
        # Create graph with vertices 0 to 15
        G = nx.Graph()
        G.add_nodes_from(range(16))
        
        # Add edges based on adjacency matrix
        for i in range(16):
            for j in range(i + 1, 16):  # Upper triangle, excluding diagonal
                if df.iloc[i, j] == 1:
                    G.add_edge(i, j)
        
        return G
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

# Brute force to find the maximum clique in graph G
def find_clique(G, k):
    vertices = list(G.nodes())
    max_clique = None
    max_size = 0
    
    # Try sizes from 2 to n (cliques must have at least 2 vertices)
    for size in range(2, len(vertices) + 1):
        for subset in combinations(vertices, size):
            if is_clique(G, subset):
                if size > max_size:  # Update if larger clique found
                    max_clique = list(subset)
                    max_size = size
    
    return max_clique  # Return maximum clique found, or None

# Check if a subset of vertices forms a clique
def is_clique(G, subset):
    for u, v in combinations(subset, 2):
        if not G.has_edge(u, v):
            return False
    return True

# Brute force to find a dominating set of size k in graph G
def find_dominating_set(G, k):
    vertices = list(G.nodes())
    for subset in combinations(vertices, k):
        if is_dominating_set(G, subset):
            return list(subset)
    return None

# Check if a subset of vertices forms a dominating set
def is_dominating_set(G, subset):
    subset_set = set(subset)
    dominated = set(subset)
    for u in subset:
        dominated.update(G.neighbors(u))
    return dominated == set(G.nodes())

# Visualize graph with highlighted subset
def visualize_graph(G, subset, title, filename):
    pos = nx.spring_layout(G, seed=42)  # Fixed seed for consistent layout
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=12, edge_color='gray')
    if subset:
        nx.draw_networkx_nodes(G, pos, nodelist=subset, node_color='red', node_size=600)
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v in G.edges() if u in subset and v in subset], edge_color='red', width=2)
    plt.title(title, fontsize=14, pad=20)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

# Main function to perform transformations and visualizations
def main():
    # Read input graph
    filename = 'graph_16_vertices.csv'
    G = read_graph_from_csv(filename)
    if G is None:
        return

    # Ensure output directory exists
    output_dir = 'visualizations'
    os.makedirs(output_dir, exist_ok=True)

    # Get user input for k
    while True:
        try:
            k = int(input("Enter the value of k (2 <= k <= 16): "))
            if 2 <= k <= 16:
                break
            else:
                print("Error: k must be between 2 and 16.")
        except ValueError:
            print("Error: Please enter a valid integer.")

    # Step 1: Find maximum clique in G
    print("Searching for maximum clique in original graph G...")
    clique = find_clique(G, k)
    if clique:
        max_clique_size = len(clique)
        # Determine instance type dynamically
        instance = "YES" if max_clique_size < k else "NO"
        print(f"\n=== Testing {instance} instance with k={k} ===")
        clique_status = f"Maximum clique of size {max_clique_size} found: {clique}"
    else:
        instance = "NO"
        print(f"\n=== Testing {instance} instance with k={k} ===")
        clique_status = "No clique found."
    print(clique_status)

    # Visualize original graph with maximum clique
    clique_title = f"Original Graph G\n{clique_status}"
    clique_filename = os.path.join(output_dir, f"original_graph_k{k}_{instance}.png")
    visualize_graph(G, clique, clique_title, clique_filename)
    print(f"Saved visualization: {clique_filename}")

    # Step 2: Transform to dominating set problem (only if max clique size < k)
    if clique and len(clique) < k:
        # Construct G' as complement graph
        G_prime = nx.complement(G)
        print("Constructed complement graph G' for dominating set problem.")

        # Find dominating set in G' (use clique size for consistency)
        clique_size = len(clique)
        print(f"Searching for dominating set of size {clique_size} in G'...")
        dom_set = find_dominating_set(G_prime, clique_size)
        dom_status = f"Dominating set of size {clique_size} found: {dom_set}" if dom_set else f"No dominating set of size {clique_size} found."
        print(dom_status)

        # Visualize G' with dominating set
        dom_title = f"Complement Graph G'\n{dom_status}"
        dom_filename = os.path.join(output_dir, f"complement_graph_k{k}_{instance}.png")
        visualize_graph(G_prime, dom_set, dom_title, dom_filename)
        print(f"Saved visualization: {dom_filename}")

        # Step 3: Convert dominating set back to clique in G
        if dom_set:
            print("Converting dominating set back to clique in G...")
            recon_clique_status = f"Dominating set {dom_set} is a clique in G." if is_clique(G, dom_set) else f"Dominating set {dom_set} is not a clique in G."
            print(recon_clique_status)

            # Visualize reconstructed clique
            recon_title = f"Original Graph G with Reconstructed Clique\n{recon_clique_status}"
            recon_filename = os.path.join(output_dir, f"reconstructed_clique_k{k}_{instance}.png")
            visualize_graph(G, dom_set, recon_title, recon_filename)
            print(f"Saved visualization: {recon_filename}")
        else:
            print("No dominating set found, cannot convert back to clique.")
    else:
        print(f"Skipping dominating set transformation (maximum clique size {len(clique) if clique else 0} is not < {k}).")

if __name__ == "__main__":
    main()