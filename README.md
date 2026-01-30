# 🎵 RAG-SQL Assistant (Chinook)

[![Python](https://img.shields.io/badge/python-blue.svg)](https://www.python.org/downloads/release/python-310/)
![Build](https://github.com/ofoski/RAG-SQL-assistant/actions/workflows/python-app.yml/badge.svg)

### 🔍 At a glance
- **Problem:** Translating natural-language questions into correct SQL queries  
- **Solution:** Schema-aware Retrieval-Augmented Generation (RAG) pipeline over database metadata 
- **Outcome:** 100% execution accuracy on a curated evaluation set of reference SQL queries  
- Stack: Python · Streamlit · FAISS · SentenceTransformers · OpenAI · SQLite


A schema-aware **Retrieval-Augmented Generation (RAG)** SQL assistant that converts natural-language questions into executable SQL queries and runs them against SQLite databases.

## ✨ Features
- 🔎 **Natural Language → SQL** conversion  
- 🧠 **Schema-Aware Retrieval** with FAISS embeddings  
- 📊 **Interactive UI** powered by Streamlit  
- 🌍 **Dataset Flexibility** – works with Chinook by default, easily swappable to other KaggleHub datasets  
- 🧪 **Evaluation Framework** with prompts + gold SQL pairs  

## ⚙️ Stack
- **Streamlit** – UI  
- **SentenceTransformers** – embeddings  
- **FAISS** – vector search  
- **OpenAI** – SQL generation  
- **SQLite + pandas** – execution  


## 🛠️ Pipeline Overview
1. 📑 **Extract metadata** → read tables and columns from the SQLite database.  
2. 🔡 **Vectorize schema** → create SentenceTransformers embeddings of per-table schema text.  
3. ⚡ **Index with FAISS** → store embeddings in FAISS for fast similarity search.  
4. 🎯 **RAG retrieval** → fetch the top-K relevant tables for each question.  
5. 🤖 **Generate SQL** → build a focused prompt and produce SQL with OpenAI.  
6. 📊 **Preview results** → execute SQL against SQLite and display in Streamlit.  


## Installation (Windows)

### 1) Clone the repo
```powershell
git clone https://github.com/ofoski/RAG-SQL-assistant.git
cd RAG-SQL-assistant
```

### 2) Create and activate a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```
### 3) Install dependencies
```powershell
pip install -r requirements.txt
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

## Dataset

The assistant is scoped to the Chinook dataset by default and is automatically downloaded via KaggleHub (no DB file committed).  

### Swap datasets
You can use other SQLite datasets by changing the KaggleHub slug in this line:
```python
import kagglehub
path = kagglehub.dataset_download("ranasabrii/chinook")  # change slug here
```

## 📊 Example Usage

**Question:**  
*"Which artist has the most albums?"*

**Generated SQL:**  
```sql
SELECT Artist.Name, COUNT(Album.AlbumId) AS AlbumCount
FROM Artist
JOIN Album ON Artist.ArtistId = Album.ArtistId
GROUP BY Artist.Name
ORDER BY AlbumCount DESC
LIMIT 1;
```

## 🖼️ Screenshot
<img width="2846" height="1528" alt="image" src="https://github.com/user-attachments/assets/1ee5a42e-b6b6-4e71-aaf5-4ae323d8dfaa" />

## 🎥 Demo Video
https://github.com/user-attachments/assets/a270f159-479f-4efe-a708-0e4fa615780d


## 📏 Evaluation

- **ROUGE** → used to evaluate SQL similarity  
- **Execution Accuracy** → compared against reference outputs  
- **Evaluation dataset** → [`sql_eval_dataset.json`](./sql_eval_dataset.json)  

**Difficulty levels:**  
- 🟢 **Easy** → simple queries  
- 🟡 **Medium** → joins & grouping  
- 🔴 **Difficult** → multi-joins, aggregations, revenue calculations

**Results:**  
✅ The assistant successfully generated correct SQL queries for **all examples** in the evaluation dataset,  
returning the same results as the gold SQL.
 



