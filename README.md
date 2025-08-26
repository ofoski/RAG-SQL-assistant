# RAG-SQL Assistant (Chinook)

A Retrieval-Augmented Generation (RAG) SQL assistant built with **Streamlit**, **FAISS**, and **OpenAI**.  
It converts natural-language questions into **Spark SQL** using schema-aware retrieval over the **Chinook** dataset.

---

## Goal
Convert natural-language questions into **Spark SQL** using schema-aware retrieval.

---

## Stack
- **Streamlit** (UI)  
- **SentenceTransformers** (embeddings)  
- **FAISS** (vector search)  
- **OpenAI** (SQL generation)  

---

## Scope
- Works on the **Chinook SQLite dataset** by default  
- Easily swappable to other **KaggleHub SQLite datasets**  

---

## Main Steps
- Extract metadata → read tables and columns from the Chinook SQLite database.  
- Vectorize schema → create SentenceTransformers embeddings of per-table schema text.  
- Index with FAISS → store embeddings in a FAISS index for fast similarity search.  
- RAG retrieval → fetch the top-K relevant tables for each user question.  
- Generate SQL → build a focused prompt and produce Spark SQL with ChatGPT.  
- Preview results → optionally execute the SQL against SQLite and display in Streamlit.  

---

## Installation (Windows)

### 1) Clone the repo
```powershell
git clone https://github.com/<your-username>/RAG-SQL-assistant.git
cd RAG-SQL-assistant
```

### 2) Create and activate a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```
### 3) Install dependencies
```powershell
pip install -r Requirements.txt
```

## Setting the OpenAI API Key (Windows)
You can set the key in two ways:
### Method 1: .env file
```powershell
OPENAI_API_KEY=sk-your-key-here
```
Create a file named .env in the project root.
Add your key as shown above.
The app will automatically load this file.

### Method 2: Command Prompt
```powershell
setx OPENAI_API_KEY "sk-your-key-here"
```
Run the command in the terminal.

## Running the App
```powershell
streamlit run streamlit.py
```



