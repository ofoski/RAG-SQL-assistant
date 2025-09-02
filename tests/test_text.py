from load_data import get_metadata, run_query

def test_simple_count_query():
    df = run_query("SELECT COUNT(*) as n FROM Customer;")
    assert "n" in df.columns
    assert df.shape[0] == 1

def test_artist_table_exists():
    tables = {m["table"] for m in get_metadata()}
    assert "Artist" in tables

def test_run_query_returns_dataframe():
    """Verify run_query returns a DataFrame"""
    df = run_query("SELECT Name FROM Artist LIMIT 1;")
    import pandas as pd
    assert isinstance(df, pd.DataFrame)


