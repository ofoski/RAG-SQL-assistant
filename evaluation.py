# Databricks notebook source
import json
with open("sql_eval_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)



# COMMAND ----------

try:
    from rage_core import text_to_sql
except ImportError:
    print("⚠️ Could not import load_data as a Python module.")
    print("👉 If you are in Databricks, run this in a separate cell at the very top:")
    print("%run ./load_data")
    # then re-run this cell after running the above
    raise


# COMMAND ----------

from rouge_score import rouge_scorer
from openai import RateLimitError
import time

def rouge_scores():
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rouge_scores = []
    def safe_text_to_sql(prompt, max_retries=5, wait_time=20):
        for attempt in range(max_retries):
            try:
                return text_to_sql(prompt)
            except RateLimitError as e:
                print(f"Rate limit hit. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
        raise Exception("Max retries exceeded due to rate limits.")
    
    for example in dataset[0:2]:
        prompt = example["prompt"]
        expected_sql = example["gold_sql"].lower()
        sql = safe_text_to_sql(prompt).lower()
        score = scorer.score(expected_sql, sql)
        rouge_l = score['rougeL'].fmeasure
        rouge_scores.append(rouge_l)
    return sum(rouge_scores) / len(rouge_scores)


# COMMAND ----------

