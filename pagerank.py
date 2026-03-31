import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def pagerank_sparse(adj_list, n, p=0.15, max_iter=100, tol=1e-6, return_errors=False):
    """
    Sparse PageRank using adjacency lists (no dense matrix)
    """

    # Initialize uniformly
    r = np.ones(n) / n
    errors = []

    # Precompute out-degrees
    out_degree = {node: len(adj_list[node]) for node in adj_list}

    for iteration in range(max_iter):
        r_new = np.ones(n) * (p / n)

        # Handle dangling nodes
        dangling_sum = sum(r[node] for node in adj_list if out_degree[node] == 0)
        r_new += (1 - p) * dangling_sum / n

        # Distribute PageRank
        for j in adj_list:
            if out_degree[j] > 0:
                share = (1 - p) * r[j] / out_degree[j]
                for i in adj_list[j]:
                    r_new[i] += share

        # Compute error
        error = np.linalg.norm(r_new - r, 1)
        errors.append(error)

        if error < tol:
            print(f"Converged in {iteration} iterations")
            r = r_new
            break

        r = r_new
    else:
        print(f"Did not fully converge within {max_iter} iterations")

    if return_errors:
        return r, errors
    return r


def load_graph(file_path):
    """
    Load graph from file and REMAP node IDs to compact indices
    (VERY IMPORTANT for memory efficiency)
    """
    edges = []
    nodes = set()

    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue

            src, dst = map(int, line.strip().split())
            edges.append((src, dst))
            nodes.add(src)
            nodes.add(dst)

    # Remap node IDs → 0 to n-1
    node_list = list(nodes)
    node_to_idx = {node: idx for idx, node in enumerate(node_list)}
    idx_to_node = {idx: node for node, idx in node_to_idx.items()}

    n = len(node_list)

    # Build adjacency list
    adj_list = {i: [] for i in range(n)}
    for src, dst in edges:
        adj_list[node_to_idx[src]].append(node_to_idx[dst])

    return adj_list, n, idx_to_node


def print_top_k(r, idx_to_node, k=10):
    top_indices = np.argsort(-r)[:k]

    print(f"\nTop {k} nodes by PageRank:")
    for rank, idx in enumerate(top_indices, start=1):
        original_id = idx_to_node[idx]
        print(f"{rank:2d}. Node {original_id}: {r[idx]:.6f}")


def plot_convergence(errors, title="Convergence of PageRank"):
    plt.figure()
    plt.plot(errors)
    plt.title(title)
    plt.xlabel("Iteration")
    plt.ylabel("L1 Error")
    plt.grid(True)
    plt.tight_layout()
    output_path = f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot to {output_path}")


if __name__ == "__main__":
    # =========================
    # SMALL TEST GRAPH
    # =========================
    print("=== Small Test Graph ===")

    adj_list_small = {
        0: [1, 2],
        1: [2],
        2: [0]
    }

    n_small = 3

    r_small, errors_small = pagerank_sparse(
        adj_list_small,
        n_small,
        return_errors=True
    )

    print("\nPageRank values (small graph):")
    for i, val in enumerate(r_small):
        print(f"Node {i}: {val:.6f}")

    plot_convergence(errors_small, title="Small Graph Convergence")

    # =========================
    # GOOGLE DATASET
    # =========================
    print("\n=== Google Dataset ===")

    file_path = "web-Google_10k.txt"

    adj_list_large, n_large, idx_to_node = load_graph(file_path)

    print(f"Loaded graph with {n_large} nodes")

    r_large, errors_large = pagerank_sparse(
        adj_list_large,
        n_large,
        p=0.15,
        max_iter=100,
        tol=1e-6,
        return_errors=True
    )

    print_top_k(r_large, idx_to_node, k=10)

    plot_convergence(errors_large, title="Google Dataset Convergence")
