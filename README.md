# RAG-SQL-assistant


This project is a **Retrieval-Augmented Generation (RAG) powered SQL Assistant**.  
It generates SQL queries from natural language questions using **ChatGPT** and a database schema.  
The project demonstrates **vectorized schema retrieval**, **FAISS indexing**, and a **Streamlit UI**.

---

## 🚀 Features
- Retrieve schema metadata from a dataset (tested with **Chinook DB** 🎶).  
- Vectorize schema information and store it in a **FAISS index** for fast retrieval.  
- Use **RAG** (retrieved schemas + question) to generate SQL queries.  
- Interactive **Streamlit app** where you type a question and get SQL instantly.  

---

## 📂 Dataset
The app is currently tested on the **Chinook SQLite dataset**.  
You can easily swap in other datasets (from **Kaggle Hub** or your own) by replacing the SQLite file.

---

## 🛠 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/RAG-SQL-assistant.git
cd RAG-SQL-assistant
