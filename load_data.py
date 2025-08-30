# Databricks notebook source
import sqlite3
import pandas as pd
import kagglehub
import os

# COMMAND ----------

def get_db_path(dataset: str = "ranasabrii/chinook") -> str:
    path = kagglehub.dataset_download(dataset)   
    files = os.listdir(path)
    for f in files:
        # handle multiple data source
        if f.lower().endswith((".db", ".sqlite", ".sqlite3")):
            return os.path.join(path, f)
    raise FileNotFoundError(f"No SQLite file found in {path}. Saw: {files}")

# COMMAND ----------

def list_tables() -> pd.DataFrame:
    """Return all table names (lowercased) from the SQLite DB."""
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    try:
        names = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';", conn
        )['name'].tolist()
        return names
    finally:
        conn.close()

# COMMAND ----------

def preview_table(sqlite_file: str, table: str, n: int = 5) -> pd.DataFrame:
    """Preview the first n rows of a given table."""
    conn = sqlite3.connect(sqlite_file, check_same_thread=False)
    try:
        return pd.read_sql_query(f'SELECT * FROM "{table}" LIMIT {n};', conn).drop_duplicates().reset_index(drop=True)
    finally:
        conn.close()

# COMMAND ----------

# Optional: run any SQL
def run_query( sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()

# COMMAND ----------

# Check the function
if __name__=="__main__":
    db = get_db_path()
    print(list_tables())
    print(preview_table(db, "Track", 5))
    print(run_query("SELECT Name, Composer FROM Track LIMIT 5;"))


# COMMAND ----------

def get_metadata():
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    try:
        metadata = []
        for name in list_tables():
            info = pd.read_sql_query(f'PRAGMA table_info("{name}")', conn)  
            cols = [{"name": row["name"], "type": row["type"]} for _, row in info.iterrows()]
            metadata.append({"table": name, "columns": cols})
        return metadata
    finally:
        conn.close()



# COMMAND ----------

def get_text():
    text = ''
    for m in get_metadata():
        text += 'table:' + f"{m['table']} " + ' '.join(
            [f"{c['name']} {c['type']}," for c in m['columns']]
        )
        text += '\n'
    texts = [t.strip().rstrip(',') for t in text.split("\n") if t.strip()]
    return texts


# COMMAND ----------

