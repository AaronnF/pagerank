# PageRank Assignment Submission

This project implements PageRank for a directed web graph, validates the method on a small example, evaluates it on the `web-Google_10k.txt` dataset, and includes a small crawl-prioritization example motivated by AI web crawling.

## Contents

- `pagerank.py`: Sparse PageRank implementation using power iteration.
- `crawl_priority.py`: Toy crawler-prioritization script using precomputed PageRank scores plus a simple quality heuristic.
- `web-Google_10k.txt`: Google web graph sample dataset.
- `small_graph_convergence.png`: Convergence plot for the small example graph.
- `google_dataset_convergence.png`: Convergence plot for the Google dataset.

## Problem Overview

Given a column-stochastic link matrix `M`, teleport probability `p`, and uniform teleport vector `u = (1/n) * 1`, the PageRank vector `r` satisfies

```math
r = (1-p)Mr + pu
```

Rearranging gives the closed-form expression

```math
(I - (1-p)M)r = pu
```

so

```math
r = p(I - (1-p)M)^{-1}u
```

with the normalization condition that the entries of `r` sum to 1.

## Effect of the Teleport Probability `p`

- When `p` is large, PageRank becomes closer to the uniform distribution because the surfer teleports more often.
- When `p` is small, PageRank depends more strongly on the web graph structure, so highly connected or authoritative pages receive more weight.
- As `p -> 1`, `r -> u`.
- As `p -> 0`, the ranking becomes increasingly dominated by the link structure and is more sensitive to dangling nodes and tightly connected clusters.

Illustrative intuition:

- In a star-shaped graph, smaller `p` strongly favors the hub.
- In multiple weakly connected communities, smaller `p` tends to concentrate rank inside denser communities.
- Increasing `p` smooths these differences and makes scores more uniform.

## Implementation Approach

The implementation in `pagerank.py` uses sparse adjacency lists and power iteration instead of constructing a dense `n x n` matrix.

This design is important because the Google dataset uses sparse node IDs. A dense matrix approach would waste a very large amount of memory and be impractical for the assignment dataset.

Main implementation details:

- Node IDs are remapped to contiguous indices `0..n-1`.
- Dangling nodes are handled by redistributing their rank uniformly.
- The algorithm iterates until the L1 difference between successive rank vectors is below a tolerance.
- Convergence plots are saved as PNG files.

## Numerical Method

The iterative update used in the code is

```math
r^{(t+1)} = (1-p)Mr^{(t)} + pu
```

with the dangling-node adjustment applied in each iteration.

The code stops when

```math
||r^{(t+1)} - r^{(t)}||_1 < 10^{-6}
```

or when the maximum number of iterations is reached.

## Small Example

The file includes a built-in 3-node test graph:

- `0 -> {1, 2}`
- `1 -> {2}`
- `2 -> {0}`

Observed output:

```text
Node 0: 0.387790
Node 1: 0.214811
Node 2: 0.397400
```

This example is useful for sanity-checking the iterative implementation against the analytical formulation on a graph small enough to inspect directly.

## Google Dataset Evaluation

Dataset:

- File: `web-Google_10k.txt`
- Reported size in the file header: 10,000 nodes and 78,323 edges

Observed run:

- Loaded graph with 10,000 nodes
- Converged in 58 iterations for `p = 0.15`

Top 10 nodes by PageRank from the current implementation:

```text
1. Node 486980: 0.006999
2. Node 285814: 0.004748
3. Node 226374: 0.003396
4. Node 163075: 0.003331
5. Node 555924: 0.002686
6. Node 32163: 0.002383
7. Node 828963: 0.002190
8. Node 504140: 0.002148
9. Node 396321: 0.002114
10. Node 599130: 0.002104
```

The convergence behavior is saved in `google_dataset_convergence.png`.

## Comparison Between Closed Form and Numerical Method

The closed form

```math
r = p(I - (1-p)M)^{-1}u
```

is useful analytically and for small graphs, but it is not the practical way to compute PageRank on large datasets because explicitly forming and inverting the matrix is expensive.

For large graphs, power iteration is the standard scalable numerical method. In this project:

- The closed form provides the theoretical basis.
- The iterative method provides the practical computation.

For a small graph, both should agree up to numerical tolerance.

## AI Crawling Extension

The file `crawl_priority.py` addresses the crawler extension of the assignment.

It assumes:

- a directed web graph represented as a dictionary of URLs and outlinks
- precomputed PageRank scores
- a simple `robots` permission dictionary

The script returns the top `k` URLs to crawl based on:

```text
final_score = pagerank_score * quality_score
```

Current heuristic:

- pages containing low-value keywords such as `login`, `signup`, `cart`, `privacy`, `terms`, `account`, and `admin` are penalized
- pages disallowed by the `robots` rules are skipped

Rationale:

- High-PageRank pages are often more authoritative, better connected, and more central in the web graph.
- For AI training or indexing, such pages may be more likely to contain broadly referenced or useful content.
- Filtering with a simple quality heuristic avoids prioritizing obvious low-value or utility pages.

One reasonable heuristic for finding high-quality pages that permit crawling is:

- prioritize URLs with high PageRank that are allowed by `robots.txt` and do not match low-value or account-related URL patterns

## How to Run

Create or activate a Python environment, then install dependencies:

```bash
python3 -m pip install numpy matplotlib
```

Run the PageRank implementation:

```bash
python3 pagerank.py
```

Run the crawl-prioritization example:

```bash
python3 crawl_priority.py
```

## Notes

- `pagerank.py` uses the non-interactive Matplotlib backend `Agg`, so plots are saved to files instead of opening a GUI window.
- The implementation is designed for the provided `web-Google_10k.txt` dataset and can be extended to larger sparse web graphs.

## Summary

This submission provides:

- the analytical closed-form PageRank equation
- a scalable sparse PageRank implementation
- evaluation on the Google 10k web graph
- convergence plots
- a simple AI crawler-prioritization extension based on PageRank and crawl permission filtering
