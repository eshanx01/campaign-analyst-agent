import sys

import mlflow
from dotenv import load_dotenv

load_dotenv()

# Turn on tracing BEFORE the agent is imported/used
mlflow.langchain.autolog()
mlflow.set_experiment("Campaign Analyst Agent")

from agent import agent  # same agent as agent.py, now traced

# (what this question tests, question)
QUESTIONS = [
    (
        "RAG lookup only (root cause)",
        "Why did Innovate Industries' influencer campaign for the Foodies "
        "segment underperform?",
    ),
    (
        "Both tools (lookup + one benchmark)",
        "How did TechCorp's Facebook campaign for men 25-34 perform, and how "
        "does its conversion rate compare to benchmark?",
    ),
    (
        "Both tools (two benchmarks + lookup)",
        "NexGen's email campaign for women aged 35-44 in New York converted at "
        "12% with a 5.6x ROI. How do those two numbers compare to benchmark, "
        "and what else did the report highlight?",
    ),
    (
        "Multi-step (four benchmarks + lookup)",
        "Compare Innovate Industries' influencer campaign (5% conversion, 3.6x "
        "ROI) and Alpha Innovations' Facebook campaign in Chicago (9% "
        "conversion, 6.7x ROI) against benchmark, then explain why stakeholders "
        "questioned Alpha's result.",
    ),
    (
        "Cross-report synthesis (lookup only)",
        "Which campaigns show that high engagement does not guarantee "
        "conversions?",
    ),
    (
        "Pattern across reports (lookup only)",
        "How does campaign duration relate to performance, and is there an "
        "exception?",
    ),
    (
        "Unanswerable (should NOT invent numbers)",
        "What was the conversion rate of Microsoft's search campaign in Tokyo?",
    ),
    (
        "Tool edge case (no benchmark defined for the metric)",
        "How does the engagement score of 1 on Innovate Industries' influencer "
        "campaign compare to benchmark?",
    ),
]


def tools_used(result):
    """Names of the tools the agent called, in order."""
    return [m.name for m in result["messages"] if getattr(m, "type", "") == "tool"]


def ask(question):
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content, tools_used(result)


def main():
    # python agent_traced.py     -> run all questions
    # python agent_traced.py 4   -> run only question 4
    items = list(enumerate(QUESTIONS, 1))
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        if not 1 <= n <= len(QUESTIONS):
            sys.exit(f"Pick a number from 1 to {len(QUESTIONS)}.")
        items = [items[n - 1]]

    for n, (label, question) in items:
        print("=" * 78)
        print(f"Q{n} [{label}]\n{question}\n")
        try:
            answer, used = ask(question)
        except Exception as e:  # keep going if one question fails
            print(f"ERROR: {type(e).__name__}: {e}\n")
            continue
        print(f"Tools called: {used or 'none'}\n")
        print(answer, "\n")


if __name__ == "__main__":
    main()