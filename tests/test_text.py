from rag_core import text_to_sql
from load_data import run_query
import pandas as pd

def test_pipeline_from_text():
    """Full pipeline: text → SQL → result"""
    question = "Which artist has the most albums?"
    sql = text_to_sql(question)
    df = run_query(sql)

    # Should return exactly one row with album count
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert "AlbumCount" in df.columns or "AlbumCount".lower() in [c.lower() for c in df.columns]
