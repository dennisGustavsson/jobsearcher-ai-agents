# database_manager.py
import sqlite3
import json

DB_FILE = "job_search_agent.db"

def initialize_database():
    """Skapar databasen och tabellen om de inte redan finns."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        headline TEXT NOT NULL,
        stad TEXT,
        link TEXT,
        structured_data TEXT,
        bedomning TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def job_exists(job_id):
    """Kontrollerar om ett jobb-ID redan finns i databasen."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_job_analysis(job_details):
    """Lägger till ett analyserat jobb i databasen."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO jobs (id, headline, stad, link, structured_data, bedomning)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job_details['id'],
        job_details['job_title'],
        job_details['stad'],
        job_details['link'],
        # SQLite kan inte lagra JSON direkt, så vi gör om det till en textsträng
        json.dumps(job_details['structured_data']),
        json.dumps(job_details['bedomning'])
    ))
    conn.commit()
    conn.close()