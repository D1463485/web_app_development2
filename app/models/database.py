import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    建立並回傳 SQLite 資料庫連線。
    預設使用 dict_factory，讓查詢結果可以像 dict 一樣透過欄位名稱存取。
    """
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 啟用 Foreign Key 支援
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    """
    初始化資料庫，執行 schema.sql 建立資料表。
    """
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        return

    conn = get_db_connection()
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
