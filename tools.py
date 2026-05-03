import requests
import time


def search_papers(query: str, limit: int = 10) -> list[dict]:
    """
    Search for research papers using the Semantic Scholar API.
    Returns a list of papers with metadata.
    """
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,externalIds,abstract,url"
    }

    for attempt in range(3):
        response = requests.get(base_url, params=params)

        if response.status_code == 429:
            wait = 2 ** attempt  # 1s, 2s, 4s
            print(f"Rate limited. Waiting {wait}s before retry...")
            time.sleep(wait)
            continue

        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    return []


def filter_papers(
        papers: list[dict],
        min_citations: int = None,
        max_citations: int = None,
        year_after: int = None,
        year_before: int = None,
        exact_year: int = None
) -> list[dict]:
    """
    Filter papers by citation count and publication year.
    All constraints are optional.
    """
    filtered = []

    for paper in papers:
        year = paper.get("year")
        citations = paper.get("citationCount")

        if min_citations is not None:
            if citations is None or citations < min_citations:
                continue

        if max_citations is not None:
            if citations is None or citations > max_citations:
                continue

        if year_after is not None:
            if year is None or year <= year_after:
                continue

        if year_before is not None:
            if year is None or year >= year_before:
                continue

        if exact_year is not None:
            if year != exact_year:
                continue

        filtered.append(paper)

    return filtered

if __name__ == "__main__":
    results = search_papers("LLM agents software engineering", limit=3)
    for paper in results:
        print(paper.get("title"))
        print(paper.get("citationCount"))
        print("---")

    filtered = filter_papers(results, min_citations=10, year_after=2022)
    print(f"Filtered: {len(filtered)} papers")