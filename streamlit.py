
import os
import sqlite3
import streamlit as st
import pandas as pd

from rag_core import text_to_sql  

st.set_page_config(page_title="RAG SQL Assistant - Chinook", page_icon="🗄️", layout="wide")

with st.sidebar:
    st.header("⚙️ Settings")
    k = st.slider("Top-K relevant tables", 1, 10, 3)
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"])
    st.caption("K controls how many Chinook tables are provided to the model.")

# Preflight: fail fast if API key missing
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not set. Add it to your environment or st.secrets and rerun.")
    st.stop()

st.title("🗄️ RAG SQL Assistant")
st.caption("🔗 Working exclusively with the **Chinook** dataset (SQLite music store).")

st.subheader("❓ Ask your question about Chinook")
question = st.text_area("Type your query:", placeholder="e.g. Top 5 customers by invoice amount", height=100)

clicked = st.button("🚀 Generate SQL", type="primary")
if clicked and question.strip():
    with st.spinner("Generating SQL..."):
        try:
            sql_text = text_to_sql(question, k=k, model_name=model)
            st.success("✅ SQL generated!")
        except Exception as e:
            msg = str(e).lower()
            if "quota" in msg or "rate limit" in msg:
                st.error(
                    "You're out of quota or hitting rate limits on this OpenAI project. "
                    "👉 Check billing/credits and that your API key/org/project env vars target the right project. "
                    "💡 You can also try switching to another model (e.g. `gpt-4o-mini` instead of `gpt-4o`)."
                )
            else:
                st.error("❌ Failed to generate SQL.")
            st.exception(e)
            st.stop()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📜 Generated SQL")
        st.code(sql_text, language="sql")

    with col2:
        st.subheader("📊 Query Preview")
        try:
            if sql_text.strip().lower().startswith("select"):
            
                from load_data import get_db_path 
                db_path = get_db_path()
                with sqlite3.connect(db_path, check_same_thread=False) as conn:
                    preview = pd.read_sql_query(sql_text, conn)
                st.dataframe(preview, use_container_width=True)
            else:
                st.info("Preview is only shown for SELECT queries.")
        except Exception as e:
            st.warning("⚠️ Could not preview results (maybe invalid SQL for SQLite).")
            st.exception(e)
