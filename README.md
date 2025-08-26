# 🎵 RAG-SQL Assistant (Chinook)

A Retrieval-Augmented Generation (RAG) SQL assistant built with **Streamlit**, **FAISS**, and **OpenAI**.  
It converts natural-language questions into **SQLite queries executed with pandas** using schema-aware retrieval over the Chinook dataset.


## 🎯 Goal
Convert natural-language questions into **SQL queries** and run them on SQLite tables using **pandas**.


## ⚙️ Stack
- **Streamlit** (UI)  
- **SentenceTransformers** (embeddings)  
- **FAISS** (vector search)  
- **OpenAI** (SQL generation)  


## 🌍 Scope
- Works on the **Chinook SQLite dataset** by default  
- Easily swappable to other **KaggleHub SQLite datasets**  


## 🛠️ Main Steps
- 📑 Extract metadata → read tables and columns from the Chinook SQLite database.  
- 🔡 Vectorize schema → create SentenceTransformers embeddings of per-table schema text.  
- ⚡ Index with FAISS → store embeddings in a FAISS index for fast similarity search.  
- 🎯 RAG retrieval → fetch the top-K relevant tables for each user question.  
- 🤖 Generate SQL → build a focused prompt and produce SQL with ChatGPT.  
- 📊 Preview results → execute the SQL against SQLite and display in Streamlit.
  
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

## Dataset

The assistant is scoped to the Chinook dataset by default and is automatically downloaded via KaggleHub (no DB file committed).  

### Swap datasets
You can use other SQLite datasets by changing the KaggleHub slug in this line:
```python
import kagglehub
path = kagglehub.dataset_download("ranasabrii/chinook")  # change slug here
```

## 🖼️ Screenshot
<img width="2862" height="1032" alt="image" src="https://github.com/user-attachments/assets/040356b0-e697-4ed6-a6d4-c67a2c828a05" />


