from load_data import get_metadata, run_query

def test_simple_count_query():
    """Run a basic query on the Chinook DB"""
    df = run_query("SELECT COUNT(*) as n FROM Customer;")
    assert "n" in df.columns
    assert df.shape[0] == 1


