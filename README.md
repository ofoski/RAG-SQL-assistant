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
