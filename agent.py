import os
from dotenv import load_dotenv
import autogen
from tools import search_papers, filter_papers, verify_paper

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

    When given a request, you must follow these steps in order:
    1. Call search_papers with a relevant query
    2. Call filter_papers with ALL constraints from the request
    3. If filter_papers returns an empty list, report failure and TERMINATE
    4. Call verify_paper on the first paper from the filtered list
    5. If verify_paper returns an error, try the next paper in the filtered list
    6. If all papers are rejected, report failure and TERMINATE
    7. If verify_paper confirms a paper, return it as your final answer

    Never call verify_paper on papers that were already rejected.
    Never call verify_paper on papers not in the filtered list.
    Never invent citation counts or paper details. Always use tool results.
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

autogen.register_function(
    verify_paper,
    caller=assistant,
    executor=proxy,
    description="Verify a single paper meets year and citation constraints before returning it to the user."
)

if __name__ == "__main__":
    proxy.initiate_chat(
        assistant,
        message="Find a paper about convolutional neural networks published after 2021 with at least 50 citations."
    )