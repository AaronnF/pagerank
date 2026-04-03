import networkx as nx
import matplotlib.pyplot as plt

# 1. Initialize the directed graph
G = nx.DiGraph()

# 2. Add nodes with their specific attributes
# Green = Selected, Yellow = Low Quality, Red = Blocked (robots.txt)
nodes = {
    '/research': {'color': '#77DD77', 'label': 'Research\n(PR: 0.32)'},
    '/blog/ai': {'color': '#77DD77', 'label': 'Blog: AI\n(PR: 0.24)'},
    '/blog/ml': {'color': '#77DD77', 'label': 'Blog: ML\n(PR: 0.16)'},
    '/privacy': {'color': '#FDFD96', 'label': 'Privacy\n(Low Quality)'},
    '/login': {'color': '#FF6961', 'label': 'Login\n(Blocked)'}
}

for node, attrs in nodes.items():
    G.add_node(node, color=attrs['color'], label=attrs['label'])

# 3. Add some arbitrary edges to make it look like a real web graph
edges = [
    ('/blog/ai', '/research'),
    ('/blog/ml', '/research'),
    ('/research', '/privacy'),
    ('/research', '/login'),
    ('/blog/ai', '/login'),
    ('/login', '/privacy')
]
G.add_edges_from(edges)

# 4. Set up the plot
plt.figure(figsize=(9, 6))
pos = nx.spring_layout(G, seed=42)  # Spring layout looks organic

# Extract colors and labels
node_colors = [nx.get_node_attributes(G, 'color')[node] for node in G.nodes()]
labels = nx.get_node_attributes(G, 'label')

# Draw the graph
nx.draw(G, pos, labels=labels, with_labels=True, node_color=node_colors, 
        node_size=4000, font_size=10, font_weight='bold', 
        edge_color='gray', arrows=True, arrowsize=20)

plt.title("Crawl-Priority Selection (k=3)", fontsize=16, pad=20)

# Save the figure for your report
plt.savefig("crawl_priority_graph.png", dpi=300, bbox_inches='tight')
plt.show()