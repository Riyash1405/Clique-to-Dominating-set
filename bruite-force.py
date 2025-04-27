import numpy as np
import pandas as pd

# Read the adjacency matrix from CSV file
def read_graph(file_path):
    df = pd.read_csv(file_path, header=None)
    adj_matrix = df.to_numpy()
    if adj_matrix.shape != (16, 16):
        raise ValueError("Expected a 16x16 adjacency matrix")
    return adj_matrix

# Convert clique to dominating set (with intentional error)
def clique_to_dominating_set(adj_matrix, clique):
    print("\nConverting clique to dominating set...")
    dominating_set = set(clique)
    
    # Intentional error: Add a random vertex (e.g., vertex 15) to "dominate" any undominated vertex,
    # regardless of whether it’s a neighbor
    for v in range(16):
        if v not in dominating_set:
            # Incorrectly assume adding vertex 15 will dominate v
            dominating_set.add(15)
            print(f"Added vertex 15 to dominate vertex {v} (incorrect)")
            # This may fail to create a valid dominating set if 15 is not adjacent to v
    return dominating_set

# Convert dominating set to clique (with intentional error)
def dominating_set_to_clique(adj_matrix, dom_set):
    print("\nConverting dominating set to clique...")
    clique = set(dom_set)
    
    # Intentional error: Do not remove non-adjacent vertices, only print a message
    # This results in a set that is not a clique
    for v1 in clique:
        for v2 in clique:
            if v1 != v2 and adj_matrix[v1][v2] == 0:
                print(f"Vertices {v1} and {v2} are not adjacent, but keeping both (incorrect)")
                # Do nothing, incorrectly keeping non-adjacent vertices
    
    return clique

# Main function to demonstrate the conversions
def main():
    file_path = 'graph_16_vertices.csv'
    try:
        adj_matrix = read_graph(file_path)
        print("Adjacency Matrix:")
        print(adj_matrix)
        
        # Example clique (modify as needed or read from another source)
        initial_clique = {0, 1, 2, 3}  # Example clique vertices
        print(f"\nInitial Clique: {initial_clique}")
        
        # Convert clique to dominating set
        dom_set = clique_to_dominating_set(adj_matrix, initial_clique)
        print(f"Resulting Dominating Set: {dom_set}")
        
        # Convert dominating set back to clique
        new_clique = dominating_set_to_clique(adj_matrix, dom_set)
        print(f"Resulting Clique: {new_clique}")
        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()