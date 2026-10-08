# Multi-Step Campaign Analyst Agent

An agentic AI workflow that orchestrates a RAG lookup tool and a benchmark
comparison tool to reason across campaign data in multiple steps, with full
observability via MLflow tracing.

## Architecture
User question → ReAct agent (GPT-4o-mini, LangGraph) → decides which tool(s)
to call → campaign_insights_lookup (RAG over campaign reports, Chroma) and/or
compare_to_benchmark → synthesizes a slide-style answer. Every step is traced
with MLflow autologging.

## Why an agent instead of a fixed pipeline
The agent decides the sequence and number of tool calls at run time. A "why"
question uses only the RAG tool; a benchmark question adds the comparison
tool; a multi-part question chains several calls.

## Average Scores & What tracing revealed
Faithfulness - 0.937500
Answer Relevancy - 0.771422
Context Precision - 0.892014

## Run locally
1. Python 3.12, then `pip install -r requirements.txt`
2. Add `OPENAI_API_KEY=...` to a `.env` file
3. `python agent_traced.py` runs the 8 test questions
4. `mlflow ui`, then open http://127.0.0.1:5000

## Tech Stack
Python, LangGraph, LangChain, OpenAI, Chroma, MLflow, Streamlit

## Demo
https://github.com/user-attachments/assets/74002798-4121-48f0-8e8e-8a953565bfbc

https://github.com/user-attachments/assets/b03a0960-0b8a-481f-a7dd-3407780d1573







