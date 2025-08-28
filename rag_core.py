# Databricks notebook source
#%pip install streamlit openai faiss-cpu sentence-transformers numpy pandas rouge-score pyspark kagglehub #threadpoolctl==3.5.0

# COMMAND ----------

try:
    from load_data import get_text
except ImportError:
    print("⚠️ Could not import load_data as a Python module.")
    print("👉 If you are in Databricks, run this in a separate cell at the very top:")
    print("%run ./load_data")
    # then re-run this cell after running the above
    raise

texts = get_text()


# COMMAND ----------

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def transform_embeddings():
    embeddings = model.encode(texts, normalize_embeddings=True).astype("float32")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index
   

# COMMAND ----------

index = transform_embeddings()
def retrieve_tables(question, k=3):
    q_vec = model.encode([question], normalize_embeddings=True).astype("float32")
    Distance, Index = index.search(q_vec, k)
    return [texts[i] for i in Index[0]], Index[0].tolist()  # schemas + their indices


# COMMAND ----------

def build_context(question, k=3):
    ctx_texts, ctx_in = retrieve_tables(question, k=k)
    ctx = "\n".join(ctx_texts) 
    return ctx

# COMMAND ----------

from openai import OpenAI
import os

def text_to_sql(question, k=3, model_name="gpt-4o-mini"):
    ctx_texts, _ = retrieve_tables(question, k=k)
    ctx = "\n".join(ctx_texts) if ctx_texts else ""

    prompt = (
        "You are a SQL assistant for Spark SQL.\n"
        "Use ONLY the columns present in the provided schemas. "
        "Output ONLY the SQL query (no explanations).\n\n"
        f"Schemas:\n{ctx}\n\n"
        f"User question:\n{question}\n"
    )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.responses.create(model=model_name, input=prompt)
    sql_text = resp.output_text.strip()
    sql_text = sql_text.replace("```sql", "").replace("```", "").strip()
    
    return sql_text

# COMMAND ----------


from rouge_score import rouge_scorer
if __name__ == "__main__":

    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    rouge_scores = []

    def safe_text_to_sql(prompt, max_retries=5, wait_time=20):
        for attempt in range(max_retries):
            try:
                return text_to_sql(prompt)
            except openai.RateLimitError as e:
                print(f"Rate limit hit. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
        raise Exception("Max retries exceeded due to rate limits.")

    for query in dataset:
        generated_sql = safe_text_to_sql(query["prompt"])
        score = scorer.score(query["gold_sql"], generated_sql)
        rouge_l = score['rougeL'].fmeasure
        rouge_scores.append(rouge_l)
        if __name__ == "__main__":
            print(f"Q: {query['prompt']}")
            print(f"Expected SQL:\n{query['gold_sql']}")
            print(f"Generated SQL:\n{generated_sql}")
            print(f"ROUGE-L: {rouge_l:.4f}")
            print("-" * 50)

    avg_rouge = sum(rouge_scores) / len(rouge_scores)
    print(f"✅ Average ROUGE-L Score (Clean SQL): {avg_rouge:.4f}")

# COMMAND ----------

