from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import campaign_insights_lookup, compare_to_benchmark

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [campaign_insights_lookup, compare_to_benchmark]

SYSTEM_PROMPT = """You are a marketing analyst agent working from campaign reports.

Rules:
1. For any question about what happened or why, call campaign_insights_lookup first.
2. When a specific metric (conversion rate, CTR, ROI) is given or found and the
   question asks how it compares to benchmark or target, call
   compare_to_benchmark. Never do the comparison yourself.
3. Units: conversion_rate and ctr are in percent (12 means 12%); roi is a
   multiple (5.6 means 5.6x).
4. Use only facts from the lookup results. If the reports do not contain the
   answer, say so plainly instead of guessing. If no benchmark is defined for a
   metric, say that too.
5. Entity check: before using any retrieved fact, confirm the company, channel
   and location in the retrieved text match the ones in the question. If the
   text is about a different campaign, do NOT borrow its numbers. Say the
   reports do not cover the campaign asked about.
6. Format for a slide: lead with the headline finding, then supporting detail,
   and name the company/campaign each fact comes from."""

agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

if __name__ == "__main__":
    result = agent.invoke({
        "messages": [{"role": "user", "content":
            "How did TechCorp's Facebook campaign for men 25-34 perform, and "
            "how does its conversion rate compare to benchmark?"}]
    })
    print(result["messages"][-1].content)