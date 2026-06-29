import sqlite3
import json

DB_PATH = "rag.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            content TEXT,
            embedding TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Veritabanı hazır.")

def insert_chunk(source, content, embedding):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chunks (source, content, embedding) VALUES (?, ?, ?)",
        (source, content, json.dumps(embedding))
    )
    conn.commit()
    conn.close()

def get_all_chunks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, content, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chunks")
    conn.commit()
    conn.close()
    print("Veritabanı temizlendi.")