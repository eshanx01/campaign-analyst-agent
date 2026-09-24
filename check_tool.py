from tools import compare_to_benchmark as t

for v in (9, 0.09):
    print(v, "->", t.invoke({"campaign_name": "TechCorp", "metric": "conversion rate", "actual_value": v}))