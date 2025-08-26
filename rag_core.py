# Databricks notebook source
#%pip install streamlit openai faiss-cpu sentence-transformers numpy pandas rouge-score pyspark kagglehub "threadpoolctl==3.5.0"

# COMMAND ----------

import kagglehub

path = kagglehub.dataset_download("ranasabrii/chinook")
print("Downloaded to:", path)

# COMMAND ----------

import os

files = os.listdir(path)
files

# COMMAND ----------

import os
import sqlite3
import pandas as pd


# Build SQLite file path
sqlite_file = os.path.join(path, files[0])

# Connect to SQLite
conn = sqlite3.connect(sqlite_file)

# Get all table names
table_names = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table';", conn
)['name'].str.lower().tolist()
if __name__ == "__main__":
    print("Tables found:", table_names)

# Load each table as a pandas DataFrame
for table in table_names:
    pdf = pd.read_sql_query(f'SELECT * FROM "{table}";', conn)
    if __name__ == "__main__":
        print(f"✅ Loaded table into pandas DataFrame: {table}")


# Verify tables (SQLite equivalent of SHOW TABLES)
tables_df = pd.DataFrame(table_names, columns=["table_name"])
if __name__ == "__main__":
    print(tables_df)


# COMMAND ----------

result = pd.read_sql_query("SELECT * FROM artist LIMIT 5;", conn)
if __name__ == "__main__":
    print(result)


# COMMAND ----------

metadata = []
for name in table_names:
    info = pd.read_sql_query(f'PRAGMA table_info("{name}")', conn)  # columns: cid, name, type, notnull, dflt_value, pk
    cols = [{"name": row["name"], "type": row["type"]} for _, row in info.iterrows()]
    metadata.append({"table": name, "columns": cols})


# COMMAND ----------

text = ''
for m in metadata:
    text  += 'table:' + f"{m['table']} " + ' '.join(
        [f"{c['name']} {c['type']}," for c in m['columns']]
    )
    text += '\n'
texts = [t.strip().rstrip(',') for t in text.split("\n") if t.strip()]

# COMMAND ----------

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(texts, normalize_embeddings=True).astype("float32")

# Build FAISS index

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
if __name__ == "__main__":
    print("\n✅ Embeddings created!")
    print(f"Shape: {embeddings.shape}")  # should be (number_of_tables, 384)
    print("\n🔍 Example embedding AFTER transformation (first table):\n")
    print(embeddings[0][:20])  # show first 20 dimensions for readability
    print(f"\n✅ Indexed {index.ntotal} tables into FAISS.")

# COMMAND ----------

def retrieve_tables(question, k=3):
    q_vec = model.encode([question], normalize_embeddings=True).astype("float32")
    Distance, Index = index.search(q_vec, k)
    return [texts[i] for i in Index[0]], Index[0].tolist()  # schemas + their indices

# example test the function
question = "List invoice totals by customer with full name and billing city."
ctx_texts, ctx_ids = retrieve_tables(question, k=3)
if __name__ == "__main__":
    print("\n".join(ctx_texts))

# COMMAND ----------

from openai import OpenAI

client = OpenAI()
if __name__ == "__main__":
    resp = client.responses.create(
        model="gpt-4o-mini",
        input="Hello, can you confirm I am connected from Databricks?"
    )
    print(resp.output_text)


# COMMAND ----------

def text_to_sql(question, k=3, model_name="gpt-3.5-turbo"):
    # 1) retrieve relevant schemas
    ctx_texts, _ = retrieve_tables(question, k=k)
    ctx = "\n".join(ctx_texts) if ctx_texts else ""

    # 2) build prompt (no leading spaces)
    prompt = (
        "You are a SQL assistant for Spark SQL.\n"
        "Use ONLY the columns present in the provided schemas. "
        "Output ONLY the SQL query (no explanations).\n\n"
        f"Schemas:\n{ctx}\n\n"
        f"User question:\n{question}\n"
    )

    # 3) call OpenAI
    resp = client.responses.create(model=model_name, input=prompt)
    sql_text = resp.output_text.strip()
    sql_text = sql_text.replace("```sql", "").replace("```", "").strip()
    
    return sql_text

# COMMAND ----------

from openai import OpenAI
import json
if __name__ == "__main__":
    client = OpenAI()
    # use your existing per-table schema strings
    # example: texts = ['table:album AlbumId bigint, Title string, ArtistId bigint', ...]
    assert isinstance(texts, list) and len(texts) > 0
    schema_block = "\n".join(texts)

    system_msg = (
        "You are a data eval helper. Create 15 SQL evaluation items for Spark SQL. "
        "Use ONLY the provided schemas. Return STRICT JSON (array) with objects: "
        "{id (1..15), difficulty ('easy'|'medium'|'hard'), prompt, gold_sql}. "
        "Make 5 easy, 5 medium, 5 hard. No extra text."
    )

    user_msg = f"""Schemas:
    {schema_block}

    Task:
    Create 15 items. Rules:
    - easy: single table, simple SELECT, LIMIT
    - medium: 2-table join OR simple aggregation
    - hard: multi-join and/or GROUP BY/HAVING/ORDER, LIMIT
    - Use only provided tables/columns.
    - Return STRICT JSON only.
    """

    resp = client.responses.create(
        model="gpt-3.5-turbo",
        input=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )

    raw = resp.output_text.strip()

    json_text = raw.replace("```json", "").replace("```", "").strip()
    dataset = json.loads(json_text)


# COMMAND ----------

import time
from openai import RateLimitError
from rouge_score import rouge_scorer
if __name__ == "__main__":

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

