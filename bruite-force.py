# import networkx as nx
# import matplotlib.pyplot as plt
# import pandas as pd
# from itertools import combinations
# import os

# # Function to read adjacency matrix from CSV
# def read_graph_from_csv(filename):
#     try:
#         df = pd.read_csv(filename, header=None)
#         if df.shape != (16, 16):
#             raise ValueError(f"Expected 16x16 adjacency matrix, got shape {df.shape}")
#         G = nx.Graph()
#         G.add_nodes_from(range(16))
#         for i in range(16):
#             for j in range(i + 1, 16):
#                 if df.iloc[i, j] == 1:
#                     G.add_edge(i, j)
#         return G
#     except FileNotFoundError:
#         print(f"Error: File {filename} not found.")
#         return None
#     except Exception as e:
#         print(f"Error reading CSV: {e}")
#         return None

# # Brute force to find the maximum clique in graph G
# def find_clique(G, k):
#     vertices = list(G.nodes())
#     max_clique = None
#     max_size = 0
#     for size in range(2, len(vertices) + 1):
#         for subset in combinations(vertices, size):
#             if is_clique(G, subset):
#                 if size > max_size:
#                     max_clique = list(subset)
#                     max_size = size
#     return max_clique

# # Check if a subset of vertices forms a clique
# def is_clique(G, subset):
#     for u, v in combinations(subset, 2):
#         if not G.has_edge(u, v):
#             return False
#     return True

# # Brute force to find a dominating set of size k in graph G
# def find_dominating_set(G, k):
#     vertices = list(G.nodes())
#     for subset in combinations(vertices, k):
#         if is_dominating_set(G, subset):
#             return list(subset)
#     return None

# # Check if a subset of vertices forms a dominating set
# def is_dominating_set(G, subset):
#     subset_set = set(subset)
#     dominated = set(subset)
#     for u in subset:
#         dominated.update(G.neighbors(u))
#     return dominated == set(G.nodes())

# # Find a dominating set starting from a clique
# def find_dominating_set_from_clique(G, clique):
#     if not clique:
#         clique = []
#     subset = list(clique)
#     dominated = set(subset)
#     for u in subset:
#         dominated.update(G.neighbors(u))
    
#     # Greedily add vertices to dominate remaining nodes
#     remaining = set(G.nodes()) - dominated
#     while remaining:
#         best_vertex = None
#         best_coverage = set()
#         for v in remaining:
#             coverage = set(G.neighbors(v)) | {v}
#             uncovered = coverage - dominated
#             if len(uncovered) > len(best_coverage):
#                 best_vertex = v
#                 best_coverage = uncovered
#         if best_vertex is None:
#             break
#         subset.append(best_vertex)
#         dominated.update(best_coverage)
#         remaining = set(G.nodes()) - dominated
    
#     return subset if is_dominating_set(G, subset) else None

# # Visualize graph with highlighted subset
# def visualize_graph(G, subset, title, filename):
#     pos = nx.spring_layout(G, seed=42)
#     plt.figure(figsize=(10, 8))
#     nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=12, edge_color='gray')
#     if subset:
#         nx.draw_networkx_nodes(G, pos, nodelist=subset, node_color='red', node_size=600)
#         nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v in G.edges() if u in subset and v in subset], edge_color='red', width=2)
#     plt.title(title, fontsize=14, pad=20)
#     plt.savefig(filename, bbox_inches='tight')
#     plt.close()

# # Main function to perform transformations and visualizations
# def main():
#     # Read input graph
#     filename = 'graph_16_vertices.csv'
#     G = read_graph_from_csv(filename)
#     if G is None:
#         return

#     # Ensure output directory exists
#     output_dir = 'visualizations'
#     os.makedirs(output_dir, exist_ok=True)

#     # Get user input for k
#     while True:
#         try:
#             k = int(input("Enter the value of k (2 <= k <= 16): "))
#             if 2 <= k <= 16:
#                 break
#             else:
#                 print("Error: k must be between 2 and 16.")
#         except ValueError:
#             print("Error: Please enter a valid integer.")

#     # Step 1: Find maximum clique in G
#     print("Searching for maximum clique in original graph G...")
#     clique = find_clique(G, k)
#     if clique:
#         max_clique_size = len(clique)
#         instance = "YES" if max_clique_size < k else "NO"
#         print(f"\n=== Testing {instance} instance with k={k} ===")
#         clique_status = f"Maximum clique of size {max_clique_size} found: {clique}"
#     else:
#         instance = "NO"
#         print(f"\n=== Testing {instance} instance with k={k} ===")
#         clique_status = "No clique found."
#     print(clique_status)

#     # Visualize original graph with maximum clique
#     clique_title = f"Original Graph G\n{clique_status}"
#     clique_filename = os.path.join(output_dir, f"original_graph_k{k}_{instance}.png")
#     visualize_graph(G, clique, clique_title, clique_filename)
#     print(f"Saved visualization: {clique_filename}")

#     # Step 2: Check if clique is a dominating set and visualize
#     if clique:
#         print("Checking if clique is a dominating set...")
#         is_clique_dominating = is_dominating_set(G, clique)
#         clique_dom_status = f"Clique {clique} is a dominating set." if is_clique_dominating else f"Clique {clique} is not a dominating set."
#         print(clique_dom_status)

#         # Visualize clique as dominating set (if it is)
#         if is_clique_dominating:
#             clique_dom_title = f"Original Graph G\n{clique_dom_status}"
#             clique_dom_filename = os.path.join(output_dir, f"clique_dominating_set_k{k}_{instance}.png")
#             visualize_graph(G, clique, clique_dom_title, clique_dom_filename)
#             print(f"Saved visualization: {clique_dom_filename}")
#     else:
#         print("No clique found, cannot check for dominating set.")

#     # Step 3: Find dominating set in G using the clique
#     print("Searching for dominating set in original graph G using clique...")
#     dom_set = find_dominating_set_from_clique(G, clique)
#     dom_status = f"Dominating set found: {dom_set}" if dom_set else "No dominating set found."
#     print(dom_status)

#     # Visualize dominating set in G
#     dom_title = f"Original Graph G\n{dom_status}"
#     dom_filename = os.path.join(output_dir, f"extended_dominating_set_k{k}_{instance}.png")
#     visualize_graph(G, dom_set, dom_title, dom_filename)
#     print(f"Saved visualization: {dom_filename}")

#     # Step 4: Transform to dominating set problem (only if max clique size < k)
#     if clique and len(clique) < k:
#         # Construct G' as complement graph
#         G_prime = nx.complement(G)
#         print("Constructed complement graph G' for dominating set problem.")

#         # Find dominating set in G' (use clique size for consistency)
#         clique_size = len(clique)
#         print(f"Searching for dominating set of size {clique_size} in G'...")
#         dom_set_prime = find_dominating_set(G_prime, clique_size)
#         dom_status_prime = f"Dominating set of size {clique_size} found: {dom_set_prime}" if dom_set_prime else f"No dominating set of size {clique_size} found."
#         print(dom_status_prime)

#         # Visualize G' with dominating set
#         dom_title_prime = f"Complement Graph G'\n{dom_status_prime}"
#         dom_filename_prime = os.path.join(output_dir, f"complement_graph_k{k}_{instance}.png")
#         visualize_graph(G_prime, dom_set_prime, dom_title_prime, dom_filename_prime)
#         print(f"Saved visualization: {dom_filename_prime}")

#         # Step 5: Convert dominating set back to clique in G
#         if dom_set_prime:
#             print("Converting dominating set back to clique in G...")
#             recon_clique_status = f"Dominating set {dom_set_prime} is a clique in G." if is_clique(G, dom_set_prime) else f"Dominating set {dom_set_prime} is not a clique in G."
#             print(recon_clique_status)

#             # Visualize reconstructed clique
#             recon_title = f"Original Graph G with Reconstructed Clique\n{recon_clique_status}"
#             recon_filename = os.path.join(output_dir, f"reconstructed_clique_k{k}_{instance}.png")
#             visualize_graph(G, dom_set_prime, recon_title, recon_filename)
#             print(f"Saved visualization: {recon_filename}")
#         else:
#             print("No dominating set found, cannot convert back to clique.")
#     else:
#         print(f"Skipping dominating set transformation (maximum clique size {len(clique) if clique else 0} is not < {k}).")

# if __name__ == "__main__":
#     main()

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
import os

# Function to read adjacency matrix from CSV
def read_graph_from_csv(filename):
    try:
        df = pd.read_csv(filename, header=None)
        if df.shape != (16, 16):
            raise ValueError(f"Expected 16x16 adjacency matrix, got shape {df.shape}")
        G = nx.Graph()
        G.add_nodes_from(range(16))
        for i in range(16):
            for j in range(i + 1, 16):
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
    for size in range(2, len(vertices) + 1):
        for subset in combinations(vertices, size):
            if is_clique(G, subset):
                if size > max_size:
                    max_clique = list(subset)
                    max_size = size
    return max_clique

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

# Find a dominating set starting from a clique
def find_dominating_set_from_clique(G, clique):
    if not clique:
        clique = []
    subset = list(clique)
    dominated = set(subset)
    for u in subset:
        dominated.update(G.neighbors(u))
    
    # Greedily add vertices to dominate remaining nodes
    remaining = set(G.nodes()) - dominated
    while remaining:
        best_vertex = None
        best_coverage = set()
        for v in remaining:
            coverage = set(G.neighbors(v)) | {v}
            uncovered = coverage - dominated
            if len(uncovered) > len(best_coverage):
                best_vertex = v
                best_coverage = uncovered
        if best_vertex is None:
            break
        subset.append(best_vertex)
        dominated.update(best_coverage)
        remaining = set(G.nodes()) - dominated
    
    return subset if is_dominating_set(G, subset) else None

# Visualize graph with highlighted subset
def visualize_graph(G, subset, title, filename):
    pos = nx.spring_layout(G, seed=42)
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

    # Step 2: Check if clique is a dominating set and visualize
    if clique:
        print("Checking if clique is a dominating set...")
        is_clique_dominating = is_dominating_set(G, clique)
        clique_dom_status = f"Clique {clique} is a dominating set." if is_clique_dominating else f"Clique {clique} is not a dominating set."
        print(clique_dom_status)

        # Visualize clique as dominating set (if it is)
        if is_clique_dominating:
            clique_dom_title = f"Original Graph G\n{clique_dom_status}"
            clique_dom_filename = os.path.join(output_dir, f"clique_dominating_set_k{k}_{instance}.png")
            visualize_graph(G, clique, clique_dom_title, clique_dom_filename)
            print(f"Saved visualization: {clique_dom_filename}")
    else:
        print("No clique found, cannot check for dominating set.")

    # Step 3: Find dominating set in G using the clique
    print("Searching for dominating set in original graph G using clique...")
    dom_set = find_dominating_set_from_clique(G, clique)
    dom_status = f"Dominating set found: {dom_set}" if dom_set else "No dominating set found."
    print(dom_status)

    # Visualize dominating set in G
    dom_title = f"Original Graph G\n{dom_status}"
    dom_filename = os.path.join(output_dir, f"extended_dominating_set_k{k}_{instance}.png")
    visualize_graph(G, dom_set, dom_title, dom_filename)
    print(f"Saved visualization: {dom_filename}")

    # Step 4: Transform to dominating set problem (only if max clique size < k)
    if clique and len(clique) < k:
        # Construct G' as complement graph
        print("Constructed complement graph G' for dominating set problem.")
        G_prime = nx.complement(G)

        # Find dominating set in G' (use clique size for consistency)
        clique_size = len(clique)
        print(f"Searching for dominating set of size {clique_size} in G'...")
        dom_set_prime = find_dominating_set(G_prime, clique_size)
        dom_status_prime = f"Dominating set of size {clique_size} found: {dom_set_prime}" if dom_set_prime else f"No dominating set of size {clique_size} found."
        print(dom_status_prime)

        # Visualize G' with dominating set
        dom_title_prime = f"Complement Graph G'\n{dom_status_prime}"
        dom_filename_prime = os.path.join(output_dir, f"complement_graph_k{k}_{instance}.png")
        visualize_graph(G_prime, dom_set_prime, dom_title_prime, dom_filename_prime)
        print(f"Saved visualization: {dom_filename_prime}")

        # Step 5: Convert dominating set back to clique in G
        if dom_set_prime:
            print("Converting dominating set back to clique in G...")
            recon_clique_status = f"Dominating set {dom_set_prime} is a clique in G." if is_clique(G, dom_set_prime) else f"Dominating set {dom_set_prime} is not a clique in G."
            print(recon_clique_status)

            # Visualize reconstructed clique
            recon_title = f"Original Graph G with Reconstructed Clique\n{recon_clique_status}"
            recon_filename = os.path.join(output_dir, f"reconstructed_clique_k{k}_{instance}.png")
            visualize_graph(G, dom_set_prime, recon_title, recon_filename)
            print(f"Saved visualization: {recon_filename}")
        else:
            print("No dominating set found, cannot convert back to clique.")
    else:
        print(f"Skipping dominating set transformation (maximum clique size {len(clique) if clique else 0} is not < {k}).")

if __name__ == "__main__":
    main()