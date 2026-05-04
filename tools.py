import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def search_papers(query: str, limit: int = 5) -> list[dict]:
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,externalIds,abstract,url"
    }

    headers = {
        "x-api-key": os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    }

    time.sleep(1)

    for attempt in range(3):
        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 429:
            wait = 5 * (2 ** attempt)
            print(f"Rate limited. Waiting {wait}s before retry...")
            time.sleep(wait)
            continue

        response.raise_for_status()
        data = response.json()
        clean = []
        for paper in data.get("data", []):
            clean.append({
                "title": paper.get("title"),
                "year": paper.get("year"),
                "citationCount": paper.get("citationCount"),
                "url": paper.get("url"),
                "abstract": (paper.get("abstract") or "")[:300],
                "authors": [a["name"] for a in paper.get("authors", [])]
            })
        return clean

    return [{"error": "No results found. Do not invent papers. Tell the user the search failed."}]


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