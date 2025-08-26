import streamlit as st
import pandas as pd
from rag_core import text_to_sql, conn  # your existing code

# Page config
st.set_page_config(
    page_title="RAG SQL Assistant - Chinook",
    page_icon="🗄️",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    k = st.slider("Top-K relevant tables", 1, 10, 3)
    st.info("K controls how many tables from the Chinook schema are given to ChatGPT.")

# Main title
st.title("🗄️ RAG SQL Assistant")
st.caption("🔗 Working exclusively with the **Chinook** dataset (SQLite music store).")

# Input area
st.subheader("❓ Ask your question about Chinook")
question = st.text_area(
    "Type your query:",
    placeholder="e.g. Show the top 5 customers by total invoice amount",
    height=100
)

# Generate button
if st.button("🚀 Generate SQL", type="primary") and question.strip():
    with st.spinner("Generating SQL with ChatGPT..."):
        try:
            sql_text = text_to_sql(question, k=k)
            st.success("✅ SQL generated using the Chinook dataset!")
        except Exception as e:
            st.error("❌ Failed to generate SQL (likely quota or API issue).")
            st.exception(e)
            st.stop()

    # Layout with two columns: SQL on left, results on right
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📜 Generated SQL (Chinook)")
        st.code(sql_text, language="sql")

    with col2:
        st.subheader("📊 Query Preview (Chinook)")
        try:
            preview = pd.read_sql_query(sql_text, conn)
            st.dataframe(preview, use_container_width=True)
        except Exception as e:
            st.warning("⚠️ Could not preview results (maybe invalid SQL for SQLite).")
            st.exception(e)
