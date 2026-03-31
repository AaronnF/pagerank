def is_allowed(url, robots_rules):
    return robots_rules.get(url, True)


def quality_score(url):
    low_value_keywords = ["login", "signup", "cart", "privacy", "terms", "account", "admin"]
    score = 1.0
    for kw in low_value_keywords:
        if kw in url.lower():
            score *= 0.3
    return score


def top_k_urls_to_crawl(web_graph, pagerank_scores, robots_rules, k=5):
    candidates = []

    for url in web_graph:
        if not is_allowed(url, robots_rules):
            continue

        pr = pagerank_scores.get(url, 0.0)
        q = quality_score(url)
        final_score = pr * q
        candidates.append((url, final_score, pr, q))

    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[:k]


if __name__ == "__main__":
    web_graph = {
        "https://example.org/research": [
            "https://example.org/blog/ai",
            "https://example.org/about"
        ],
        "https://example.org/blog/ai": [
            "https://example.org/research",
            "https://example.org/blog/ml"
        ],
        "https://example.org/login": [
            "https://example.org/research"
        ],
        "https://example.org/blog/ml": [
            "https://example.org/research"
        ],
        "https://example.org/privacy": []
    }

    pagerank_scores = {
        "https://example.org/research": 0.32,
        "https://example.org/blog/ai": 0.24,
        "https://example.org/login": 0.18,
        "https://example.org/blog/ml": 0.16,
        "https://example.org/privacy": 0.10
    }

    robots_rules = {
        "https://example.org/research": True,
        "https://example.org/blog/ai": True,
        "https://example.org/login": False,
        "https://example.org/blog/ml": True,
        "https://example.org/privacy": True
    }

    top_urls = top_k_urls_to_crawl(web_graph, pagerank_scores, robots_rules, k=3)

    print("Top URLs to crawl:")
    for rank, item in enumerate(top_urls, start=1):
        url, final_score, pr, q = item
        print(f"{rank}. {url}")
        print(f"   PageRank={pr:.3f}, Quality={q:.2f}, Final Score={final_score:.3f}")