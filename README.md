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

## 🖼️ Screenshot
<img width="2846" height="1528" alt="image" src="https://github.com/user-attachments/assets/1ee5a42e-b6b6-4e71-aaf5-4ae323d8dfaa" />

## 🎥 Demo Video
https://github.com/user-attachments/assets/a270f159-479f-4efe-a708-0e4fa615780d

## 📏 Evaluation  

ROUGE was first used to evaluate the similarity between the generated SQL text and the reference (gold) SQL.  
To measure real-time effectiveness, a **JSON evaluation dataset** (`sql_eval_dataset.json`) was created, pairing natural-language prompts with gold SQL queries.  

Each prompt in the dataset is labeled with a difficulty level:  

- 🟢 **Easy** → basic listing, ordering, or counting queries  
- 🟡 **Medium** → queries involving joins, grouping, or simple aggregations  
- 🔴 **Difficult** → queries with multiple joins, revenue calculations, or more complex conditions  

The generated SQL was executed and compared against this dataset. In many cases, the model produced queries that returned the **exact same results** as the reference SQL, while also achieving high ROUGE scores.  

This demonstrates both the **textual accuracy** and the **practical effectiveness** of the assistant in converting natural-language questions into correct SQL statements.  
 



