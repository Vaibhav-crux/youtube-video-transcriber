import sqlite3
import os

# Define the path to the database file
DATABASE_PATH = os.path.join(os.path.dirname(os.getcwd()), 'database', 'transcriptions.db')

def save_transcript(transcript, file_name):
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transcriptions (id INTEGER PRIMARY KEY, transcript TEXT, file_name TEXT)''')
    c.execute("INSERT INTO transcriptions (transcript, file_name) VALUES (?, ?)", (transcript, file_name))
    conn.commit()
    conn.close()

def fetch_saved_transcript():
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transcriptions (id INTEGER PRIMARY KEY, transcript TEXT, file_name TEXT)''')
    c.execute("SELECT transcript FROM transcriptions ORDER BY id DESC LIMIT 1")
    transcript = c.fetchone()[0]
    conn.close()
    return transcript
