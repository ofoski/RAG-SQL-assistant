# tests/test_pipeline_mocked.py
from rag_core import text_to_sql
from load_data import run_query

def test_pipeline_from_text_mocked(monkeypatch):
    """Mock LLM step so pipeline can run without OpenAI key"""
    fake_sql = """
    SELECT Artist.Name, COUNT(Album.AlbumId) AS AlbumCount
    FROM Artist
    JOIN Album ON Artist.ArtistId = Album.ArtistId
    GROUP BY Artist.Name
    ORDER BY AlbumCount DESC
    LIMIT 1;
    """
    monkeypatch.setattr("rag_core.text_to_sql", lambda _: fake_sql)

    sql = text_to_sql("Which artist has the most albums?")
    df = run_query(sql)

    assert df.shape[0] == 1
    assert "AlbumCount" in df.columns
