import os
from dotenv import load_dotenv
import autogen
from tools import search_papers, filter_papers

load_dotenv()

LLM_CONFIG = {
    "config_list": [
        {
            "model": "open-mistral-nemo",
            "api_key": os.getenv("MISTRAL_API_KEY"),
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "repeat_penalty": 1.1,
            "temperature": 0.0,
            "seed": 42,
            "stream": False,
            "native_tool_calls": False,
            "cache_seed": None,
        }
    ]
}

# The LLM-powered assistant
assistant = autogen.AssistantAgent(
    name="ResearchAgent",
    llm_config=LLM_CONFIG,
    system_message="""You are a research assistant that finds academic papers.

    When given a request, you must:
    1. Call search_papers with a relevant query
    2. Call filter_papers with the constraints from the request
    3. Return a structured answer with: title, authors, year,
       citation count, source (Semantic Scholar), URL, and why it matches.

    CRITICAL RULES:
    - Never invent or fabricate papers, authors, URLs or citation counts
    - If search_papers returns empty or an error, tell the user no results were found
    - Only report papers that came from tool results

    When you have returned your final answer, end your reply with TERMINATE."""
)

# The user proxy - executes tool calls
proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")
)

# Register tools on the proxy
autogen.register_function(
    search_papers,
    caller=assistant,
    executor=proxy,
    description="Search for research papers by topic.",
)

autogen.register_function(
    filter_papers,
    caller=assistant,
    executor=proxy,
    description="Filter papers by year and citation count."
)

if __name__ == "__main__":
    proxy.initiate_chat(
        assistant,
        message="Find a research paper about LLM agents for software engineering published after 2022 with at least 5 citations."
    )