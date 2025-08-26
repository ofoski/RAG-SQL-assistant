🗄️ RAG-SQL-Assistant

A Retrieval-Augmented Generation (RAG) SQL Assistant built with Streamlit, FAISS, and OpenAI.
It converts natural language questions into SQL queries using database schema information.

This project demonstrates:

Vectorized schema retrieval with embeddings

FAISS indexing for similarity search

SQL generation with ChatGPT

A simple, interactive Streamlit UI

🚀 Features

Extracts table & column metadata from the Chinook SQLite dataset

Vectorizes schema text with SentenceTransformers embeddings

Builds a FAISS index for fast retrieval

Uses RAG (retrieved schema + user prompt) to generate SQL queries

Interactive Streamlit app where you type a question → get SQL → preview results

📂 Dataset

By default, the app uses the Chinook SQLite dataset, automatically downloaded from KaggleHub:

import kagglehub
path = kagglehub.dataset_download("ranasabrii/chinook")


You can replace this with any KaggleHub SQLite dataset for more complex testing by changing the dataset slug.

⚙️ Setup (Windows)
1. Clone the repository
git clone https://github.com/<your-username>/RAG-SQL-assistant.git
cd RAG-SQL-assistant

2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r Requirements.txt

4. Set your OpenAI API Key

The app requires an OpenAI API key. You can set it in two ways:

🔑 Method 1: Using a .env file (recommended)

In the project root, create a file named .env

Add your API key inside it:

OPENAI_API_KEY=sk-your-key-here


The app will automatically load this key when running

🔑 Method 2: Using Command Prompt

Set your API key directly in Windows:

setx OPENAI_API_KEY "sk-your-key-here"

▶️ Running the app

Start the Streamlit application:

streamlit run streamlit.py


Then open http://localhost:8501
 in your browser.
