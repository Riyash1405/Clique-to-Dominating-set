
# 🧩 Graph Clique and Dominating Set Transformation

This project analyzes a given graph to:
- Find a **maximum clique** using an efficient method
- Transform the **clique into a dominating set**
- Try to find a **maximum clique back inside** the dominating set
- **Visualize** all key results (input graph, clique, dominating set, maximum clique)

All steps are optimized — **no brute force** methods are used.

---

## 📂 Project Structure

| File | Purpose |
|:-----|:--------|
| `graph_16_vertices.csv` | Input adjacency matrix (CSV file) for the graph (16x16 matrix) |
| `main.py` | Main Python script performing the transformations |
| `input_graph.png` | Visualization of the original input graph |
| `clique_graph.png` | Visualization highlighting the maximum clique |
| `dominating_set_graph.png` | Visualization highlighting the dominating set |
| `max_clique_in_domset_graph.png` | Visualization highlighting the maximum clique found inside the dominating set |

---

## 📜 How It Works

1. **Input**:
   - Graph is loaded from a CSV file containing the **adjacency matrix**.

2. **Maximum Clique Finding**:
   - Uses `networkx.find_cliques()` to **efficiently** find all cliques and select the largest one.

3. **Clique to Dominating Set Transformation**:
   - Expands the clique to a dominating set by covering all nodes in the graph.

4. **Dominating Set to Maximum Clique Search**:
   - Even if the dominating set isn't a clique, the code extracts the **largest clique inside** it.

5. **Visualizations**:
   - Graphs are drawn using `matplotlib` and saved as `.png` files.

---

## 🚀 Requirements

Install the necessary Python packages:

```bash
pip install networkx matplotlib numpy
```

---

## 📈 Running the Project

1. **Prepare the input file**:
   - Ensure `graph_16_vertices.csv` is in the project folder.
   - Format: 16×16 CSV matrix with `0` (no edge) or `1` (edge).

2. **Run the script**:

```bash
python main.py
```

3. **Output**:
   - Check the console for:
     - Maximum clique
     - Dominating set
     - Maximum clique inside dominating set
   - Check the generated PNG files for visualizations.

---

## 📸 Example Console Output

```
Clique: [0, 1, 2, 3]
Is Clique Valid? Yes
Dominating Set: [0, 1, 2, 3]
Is Dominating Set Valid? Yes
Maximum Clique inside Dominating Set: [0, 1, 2, 3]
Is New Clique Valid? Yes
```

---

## 🛠️ Technologies Used

- **Python 3.x**
- **NetworkX** (graph algorithms)
- **Matplotlib** (visualization)
- **NumPy** (matrix operations)
- **CSV** (input data reading)

---

## 📚 Notes

- The clique search is based on the **Bron–Kerbosch algorithm** (no brute-force over all subsets).
- The maximum clique found is not guaranteed to be globally maximum if the graph is extremely large — but for 16 vertices, it's very accurate.
- The project is designed for **easy expansion** to larger graphs (e.g., 50-100 vertices).

---

## 📬 Contact

For any questions, improvements, or suggestions, feel free to reach out!

---

# 🎯 Final Tip:
If you want to test on your **own graphs**, just update the `graph_16_vertices.csv` file!

---

Would you also like me to generate a **sample `graph_16_vertices.csv`** you can directly use (with a built-in clique)? 📄🚀  
If yes, I can attach that too!
