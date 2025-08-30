# Databricks notebook source
import json
import pandas as pd
with open("sql_eval_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)



# COMMAND ----------

try:
    from rag_core import text_to_sql 
    from load_data import run_query

except ImportError:
    print("⚠️ Could not import load_data as a Python module.")
    print("👉 If you are in Databricks, run this in a separate cell at the very top:")
    print("%run ./rag_core")
    # then re-run this cell after running the above
    raise


# COMMAND ----------

from openai import RateLimitError
def get_prediction():
    pred_sql = []
    
    def safe_text_to_sql(prompt, max_retries=5, wait_time=20):
        for attempt in range(max_retries):
            try:
                return text_to_sql(prompt)
            except RateLimitError as e:
                print(f"Rate limit hit. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
        raise Exception("Max retries exceeded due to rate limits.")

    for example in dataset:
        prompt = example["prompt"]
        pred_sql.append(safe_text_to_sql(prompt))
    return pred_sql

# COMMAND ----------

from rouge_score import rouge_scorer
from openai import RateLimitError
import time

def rouge_accuracy_scores():
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rouge_scores = []
    accuracy = 0
    for i in range(len(dataset)):
        gold_sql = dataset[i]["gold_sql"]
        pred_sql = get_prediction()[i]
        score = scorer.score(gold_sql.lower(), pred_sql.lower())
        rouge_l = score['rougeL'].fmeasure
        rouge_scores.append(rouge_l)
        try:
            if np.array_equal(run_query(result[i]).values, run_query(dataset[i]["gold_sql"]).values):
                accuracy += 1
        except Exception:
            pass

    return sum(rouge_scores) / len(rouge_scores), accuracy / len(dataset)



# COMMAND ----------

rouge_accuracy_scores()
