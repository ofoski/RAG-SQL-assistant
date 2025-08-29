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

from openai import OpenAI, RateLimitError
import os

def text_to_sql(question, k=3, model_name="gpt-4o-mini"):
    ctx_texts, _ = retrieve_tables(question, k=k)
    ctx = "\n".join(ctx_texts) if ctx_texts else ""

    prompt = (
        "Use **SQLite** only. Dates via STRFTIME('%Y',col)/STRFTIME('%m',col) "
        "(no YEAR/MONTH/DATE_TRUNC). Use LIMIT (not TOP). Case-insensitive match "
        "with LOWER(col) LIKE LOWER(:v) (not ILIKE). Concatenate with || (not CONCAT). "
        "Booleans 1/0. Use only given tables/columns. Output only one SQL ending with ';'.\n\n"
        f"Schemas:\n{ctx}\n\n"
        f"Question:\n{question}\n"
    )
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.responses.create(model=model_name, input=prompt)
    sql_text = resp.output_text.strip()
    sql_text = sql_text.replace("```sql", "").replace("```", "").strip()
    
    return sql_text

# COMMAND ----------


