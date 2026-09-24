from dotenv import load_dotenv
load_dotenv()  # must run BEFORE OpenAIEmbeddings is created below

from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 8})


@tool
def campaign_insights_lookup(question: str) -> str:
    """Look up narrative information about campaign performance from the
    campaign reports. Use this for 'why' and 'what happened' questions.
    Pass a specific search query that names the company, channel or city
    whenever they are known."""
    docs = retriever.invoke(question)
    return "\n\n".join(d.page_content for d in docs)


@tool
def compare_to_benchmark(campaign_name: str, metric: str, actual_value: float) -> str:
    """Compare a campaign's actual metric value against the benchmark for that
    metric. Use this for 'how did X compare to target/benchmark' questions.
    Supported metrics: conversion_rate, ctr, roi.
    Units: conversion_rate and ctr are in PERCENT (pass 12 for 12%, never 0.12);
    roi is a multiple (pass 5.6 for 5.6x)."""
    # Benchmarks = averages of campaign_data.csv (conversion ~8%, CTR ~14%, ROI ~5.0x)
    benchmarks = {"conversion_rate": 8.0, "ctr": 14.0, "roi": 5.0}
    key = metric.lower().strip().replace(" ", "_")
    benchmark = benchmarks.get(key)
    if benchmark is None:
        return (f"No benchmark defined for metric '{metric}'. "
                f"Supported metrics: {', '.join(benchmarks)}.")

    note = ""
    # Safety net: percent metrics passed as fractions (0.09 instead of 9).
    # Assumes no real conversion/CTR value is below 1%, true for this dataset.
    if key in ("conversion_rate", "ctr") and actual_value < 1:
        actual_value *= 100
        note = " (input looked like a fraction, so it was read as a percent)"

    diff_pct = ((actual_value - benchmark) / benchmark) * 100
    status = "above" if diff_pct > 0 else "below"
    return (f"{campaign_name}'s {metric} of {actual_value:g} is {abs(diff_pct):.1f}% "
            f"{status} the benchmark of {benchmark:g}{note}.")