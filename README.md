## **RAG-SQL Assistant (Chinook)**

- **Goal:** Convert **natural-language questions** into **Spark SQL** using **schema-aware retrieval**.
- **Stack:** **Streamlit** (UI), **SentenceTransformers** (embeddings), **FAISS** (vector search), **OpenAI** (SQL generation).
- **Scope:** Works on the **Chinook** SQLite dataset by default; easily swappable to other **KaggleHub** SQLite datasets.

---

### **✅ Main Steps**
- **Extract metadata** → read **tables** and **columns** from the Chinook SQLite database.  
- **Vectorize schema** → create **SentenceTransformers embeddings** of per-table schema text.  
- **Index with FAISS** → store embeddings in a **FAISS** index for fast **similarity search**.  
- **RAG retrieval** → fetch the **top-K relevant tables** for each user question.  
- **Generate SQL** → build a focused prompt and produce **Spark SQL** with **ChatGPT**.  
- **Preview results** → optionally execute the SQL against SQLite and display in **Streamlit**.

---

## **Installation (Windows)**

**1) Clone the repo**
```powershell
git clone https://github.com/<your-username>/RAG-SQL-assistant.git
cd RAG-SQL-assistant

2) Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate


3) Install dependencies

pip install -r Requirements.txt

Setting the OpenAI API Key (Windows)

You can set the key in two ways:

Method 1 (recommended): .env file

OPENAI_API_KEY=sk-your-key-here


Create a file named .env in the project root.

Add your key as shown above.

The app will automatically load this file.

Method 2: Command Prompt

setx OPENAI_API_KEY "sk-your-key-here"


Run the command in PowerShell.

Close and reopen your terminal after running setx.

Running the App
streamlit run streamlit.py


After running, open http://localhost:8501
 in your browser.

Dataset

Default: The assistant is scoped to the Chinook dataset.

Download: The code downloads Chinook automatically via KaggleHub (no DB file committed).

Swap datasets: You can test other, more complex SQLite datasets by changing the KaggleHub slug — the same RAG + FAISS pipeline applies.

Example (inside code)

import kagglehub
path = kagglehub.dataset_download("ranasabrii/chinook")  # swap slug to test other datasets

Example Questions

List 5 artists

Find all invoices from customers in Brazil

Top 10 tracks by length

Which employees report to a manager?

Show album titles with their artist names (limit 10)

Top 5 customers by total invoice amount

Keywords & Concepts

Vectorize data

Embeddings

FAISS (similarity search)

RAG (retrieval-augmented generation)

Prompt-to-SQL

Spark SQL

Streamlit UI

Chinook dataset (extendable with KaggleHub)

Libraries Used

streamlit

openai

sentence-transformers

faiss-cpu

pandas, numpy

kagglehub

python-dotenv

sqlite3 (Python standard library)
