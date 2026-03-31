import networkx as nx
import matplotlib.pyplot as plt

# Create a figure with two subplots side-by-side
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ==========================================
# Graph 1: The Cyclic Graph
# ==========================================
G1 = nx.DiGraph()
# A links to B, B links to C, C links back to A
G1.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])

plt.sca(axes[0]) # Set the current axis to the first subplot
# A circular layout works best to show a cycle visually
pos1 = nx.circular_layout(G1) 

nx.draw(G1, pos1, with_labels=True, node_color='#AEC6CF', # Pastel blue
        node_size=2500, font_size=14, font_weight='bold', 
        arrows=True, arrowsize=25, edge_color='gray', width=2)
axes[0].set_title("Cyclic Graph\n(Mutual Reinforcement)", fontsize=16, pad=15)

# ==========================================
# Graph 2: The Authoritative Graph
# ==========================================
G2 = nx.DiGraph()
# Many pages point to A (D, E, F, G), A links to only a few (H, I)
edges2 = [('D', 'A'), ('E', 'A'), ('F', 'A'), ('G', 'A'), ('A', 'H'), ('A', 'I')]
G2.add_edges_from(edges2)

plt.sca(axes[1]) # Set the current axis to the second subplot
# A spring layout naturally puts the most connected node (A) in the center
pos2 = nx.spring_layout(G2, seed=42) 

# Let's highlight the authoritative node 'A' in a different color
node_colors = ['#FFB347' if node == 'A' else '#CFCFCF' for node in G2.nodes()]

nx.draw(G2, pos2, with_labels=True, node_color=node_colors, 
        node_size=2500, font_size=14, font_weight='bold', 
        arrows=True, arrowsize=25, edge_color='gray', width=2)
axes[1].set_title("Authoritative Graph\n(High in-degree for Node A)", fontsize=16, pad=15)

# ==========================================
# Final Formatting and Saving
# ==========================================
plt.tight_layout()
# Save as a high-res PNG for your report
plt.savefig("pagerank_illustrative_examples.png", dpi=300, bbox_inches='tight')
print("Graph saved successfully as 'pagerank_illustrative_examples.png'")

# Display the plot
plt.show()