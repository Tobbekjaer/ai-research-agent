# Agent Workflow

## Overview
An AutoGen-based research agent that takes natural language requests 
and returns real, constraint-verified academic papers using the 
Semantic Scholar API - without hallucinating results.

## Step-by-step Flow
1. User submits a natural language request
2. LLM parses intent and extracts constraints: topic, year, citation count
3. LLM calls search_papers with a relevant query string
4. LLM calls filter_papers with the extracted constraints
5. LLM reasons about relevance of the filtered results
6. Returns a structured answer: title, authors, year, citation count,
   source, URL, and explanation
7. If no results found, reports failure honestly without inventing data

## LLM Responsibilities
- Understand the user's natural language request
- Extract search constraints (topic, year operator, citation threshold)
- Choose an appropriate search query for the API
- Reason about whether a returned paper is relevant to the request
- Format and explain the final answer

## Deterministic Code Responsibilities
- Call the Semantic Scholar API with the query (search_papers)
- Enforce rate limit handling with exponential backoff
- Filter papers by exact year and citation count constraints (filter_papers)
- Return a clear error message if the API fails or returns no results

## Failure Handling
- Rate limiting: retries with exponential backoff (5s, 10s, 20s)
- Empty results: returns structured error message to prevent hallucination
- No matching papers: agent reports failure honestly and terminates