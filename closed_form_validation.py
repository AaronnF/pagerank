import numpy as np

# Number of nodes
n = 3

# Teleportation probability (assuming you used the standard 0.15, adjust if needed!)
p = 0.15

M = np.array([
    [0.0, 0.0, 1.0], # Node 0 receives links from Node 2
    [0.5, 0.0, 0.0], # Node 1 receives links from Node 0
    [0.5, 1.0, 0.0]  # Node 2 receives links from Node 0 and Node 1
])

# 1. Create the Identity matrix (I) and the all-ones vector
I = np.eye(n)
ones = np.ones((n, 1))

# 2. Calculate the core matrix: (I - (1-p)M)
core_matrix = I - (1 - p) * M

# 3. Invert the core matrix: (I - (1-p)M)^-1
inverted_matrix = np.linalg.inv(core_matrix)

# 4. Multiply it all together: r = p * inverted_matrix * (1/n) * ones
r_closed_form = p * np.dot(inverted_matrix, (1 / n) * ones)

# Print the final vector (flattened for easy reading)
print("Analytical Closed-Form PageRank Vector:")
print(np.round(r_closed_form.flatten(), 4))