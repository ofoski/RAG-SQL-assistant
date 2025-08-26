## **RAG-SQL Assistant (Chinook)**

A **Retrieval-Augmented Generation (RAG)** SQL assistant built with **Streamlit**, **FAISS**, and **OpenAI**.  
It converts **natural-language questions** into **Spark SQL** using **schema-aware retrieval** over the **Chinook** dataset.

---

### **✅ Main Steps**
- **Extract metadata:** read **tables** and **columns** from the Chinook SQLite database.  
- **Vectorize schema:** create **SentenceTransformers embeddings** of per-table schema text.  
- **Index with FAISS:** store embeddings in a **FAISS** index for fast **similarity search**.  
- **RAG retrieval:** fetch the **top-K relevant tables** for each user question.  
- **Generate SQL:** build a focused prompt and produce **Spark SQL** with **ChatGPT**.  
- **Preview results:** optionally run the SQL against SQLite to **preview** in **Streamlit**.

---

## **Installation (Windows)**

**1) Clone the repo**
```powershell
git clone https://github.com/<your-username>/RAG-SQL-assistant.git
cd RAG-SQL-assistant
2) Create and activate a virtual environment

powershell
Copy
Edit
python -m venv venv
venv\Scripts\activate
3) Install dependencies

powershell
Copy
Edit
pip install -r Requirements.txt
Setting the OpenAI API Key (Windows)
You can set the key in two ways:

Method 1 (recommended): .env file

Create a file named .env in the project root.

Add:

ini
Copy
Edit
OPENAI_API_KEY=sk-your-key-here
The app automatically loads this file.

Method 2: Command Prompt

powershell
Copy
Edit
setx OPENAI_API_KEY "sk-your-key-here"
(Close and reopen your terminal after running setx.)

Running the App
powershell
Copy
Edit
streamlit run streamlit.py
Open http://localhost:8501 in your browser.

Dataset
This assistant is scoped to the Chinook dataset.

The code downloads Chinook automatically via KaggleHub (no DB file committed).

You can test other, more complex SQLite datasets by changing the KaggleHub slug—the same RAG + FAISS pipeline applies.

Example (inside code):

python
Copy
Edit
import kagglehub
path = kagglehub.dataset_download("ranasabrii/chinook")  # swap slug to test other datasets
