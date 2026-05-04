from agent import proxy, assistant

TEST_PROMPTS = [
    "Find a paper about machine learning published after 2020 with at least 50 citations.",
    "Find a paper about retrieval-augmented generation published after 2022 with at least 100 citations.",
    "Find a paper about AI agents published before 2019 with at least 500 citations.",
    "Find a paper about transformer architectures published in 2021 with at least 50 citations.",
    "Find a paper about deep learning with at least 1000 citations.",
    "Find a paper about quantum neural network optimization published after 2023 with at least 5000 citations.",
    "Find a recent paper about AI that would be useful for a software developer.",
    "Find a paper about fine-tuning large language models published after 2021 with at least 50 citations.",
    "Find a paper about convolutional neural networks published after 2021 with at least 50 citations.",
    "Find a paper about reasoning patterns in AI agents with at least 50 citations.",
]

CRITERIA = [
    "found_relevant_paper",
    "respected_year_constraint",
    "respected_citation_constraint",
    "provided_valid_source",
    "avoided_hallucination",
    "gave_useful_explanation",
]

def run_evaluation():
    results = []

    for i, prompt in enumerate(TEST_PROMPTS):
        print(f"\n{'='*60}")
        print(f"Test {i+1}/{len(TEST_PROMPTS)}")
        print(f"Prompt: {prompt}")
        print('='*60)

        chat_result = proxy.initiate_chat(
            assistant,
            message=prompt,
            clear_history=True,
        )

        # Get the last agent message
        last_message = chat_result.chat_history[-1]["content"]
        print(f"\nAgent answer:\n{last_message}")

        # Manual scoring - you review the output and fill this in
        print("\nScore this response (1=pass, 0=fail, -1=N/A):")
        scores = {}
        for criterion in CRITERIA:
            val = input(f"  {criterion}: ")
            scores[criterion] = int(val)

        results.append({
            "prompt": prompt,
            "answer": last_message,
            "scores": scores,
        })

    return results


def print_summary(results):
    print(f"\n{'='*60}")
    print("EVALUATION SUMMARY")
    print('='*60)

    for criterion in CRITERIA:
        passes = sum(
            1 for r in results
            if r["scores"].get(criterion) == 1
        )
        total = sum(
            1 for r in results
            if r["scores"].get(criterion) != -1
        )
        print(f"{criterion}: {passes}/{total} passed")


if __name__ == "__main__":
    results = run_evaluation()
    print_summary(results)