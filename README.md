# AI Research Agent

An AutoGen-based research agent that finds academic papers using the 
Semantic Scholar API based on natural language requests with constraints 
on topic, publication year, and citation count.

## Setup

### Requirements
- Python 3.10+
- Git

### Installation

1. Clone the repository:
   git clone https://github.com/your-username/ai-research-agent.git
   cd ai-research-agent

2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate     # Windows

3. Install dependencies:
   pip install -r requirements.txt

### API Keys

Create a .env file in the project root:

   MISTRAL_API_KEY=your_mistral_key_here
   SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key_here

- Mistral AI free tier: https://console.mistral.ai
- Semantic Scholar API: https://www.semanticscholar.org/product/api

Never commit your .env file. It is listed in .gitignore.

## Running the Agent

Run a single query:

   python agent.py

To change the query, edit the message at the bottom of agent.py:

   proxy.initiate_chat(
       assistant,
       message="Your query here"
   )

Example queries:
- "Find a paper about LLM agents published after 2022 with at least 50 citations."
- "Find a paper about deep learning with at least 1000 citations."
- "Find a paper about RAG published before 2021 with at least 500 citations."

## Running the Evaluation

   python evaluate.py

This runs 10 test prompts interactively. For each result you score 
6 criteria manually (1=pass, 0=fail, -1=N/A). A summary is printed 
at the end.

## Agent Workflow

See WORKFLOW.md for a detailed breakdown of the agent's decision process.

## Evaluation Results

| Criterion                  | Result  |
|---------------------------|---------|
| Found relevant paper       | 5/9     |
| Respected year constraint  | 3/5     |
| Respected citation constraint | 5/7  |
| Provided valid source      | 8/8     |
| Avoided hallucination      | 10/10   |
| Gave useful explanation    | 6/10    |

### Key Findings
- The agent never hallucinated - all results came from real API data
- Year constraints were inconsistently respected, especially "before year" 
  and "exact year" requests
- Citation constraints occasionally ignored when search results were scarce
- Ambiguous prompts returned results but with low citation counts
- The impossible case (test 6) was correctly handled with a failure message

## Group Contributions

- Tobias Hougs Kjær: Full implementation and evaluation

## Reflection

### What worked well?
- Hallucination prevention was reliable throughout all 10 tests
- The Semantic Scholar API provided real, verifiable paper data
- Rate limiting with exponential backoff handled API constraints well
- The impossible case was handled correctly without inventing papers

### What failed or was unreliable?
- Year constraints were inconsistently extracted by the LLM, especially 
  "before" and "exact year" requests
- Narrow or niche topics returned few results, sometimes causing the 
  agent to ignore citation constraints rather than report failure
- The search limit of 5 papers occasionally caused valid papers to be 
  missed entirely

### How often did the agent need tool calls?
Every query required exactly 2 tool calls - search_papers followed by 
filter_papers. No query required more or fewer calls.

### Did the LLM ever hallucinate?
No. The combination of the error message returned on failed searches 
and the explicit system prompt instruction prevented all hallucination 
across 10 tests.

### How did you prevent incorrect answers?
Two mechanisms worked together: returning a structured error message 
from search_papers when results were empty, and explicitly instructing 
the agent in the system prompt never to invent papers or citation counts.

### What would you improve with more time?
- **Increase search limit** to 10-15 results to reduce missed papers 
  on saturated topics like CNNs (observed in test 9)
- **Add a fallback query** with a broader topic when the first search 
  returns too few results above the citation threshold
- **Add deterministic constraint verification** after the LLM formats 
  its answer, to catch cases where citation constraints are ignored 
  when results are scarce (observed in test 10)
- **Implement a default minimum citation threshold** for ambiguous 
  prompts to avoid returning low-quality results (observed in test 7)
- **Implement advanced reasoning patterns** such as ReAct or LLM 
  reflection. For example, ReAct would allow
  the agent to reason about whether the results satisfy the constraints 
  before returning them, and retry with a different query if not. 
  LLM reflection could catch cases where year constraints were 
  misextracted, which caused 2 out of 5 year constraint failures 
  in evaluation.

