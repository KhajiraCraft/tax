import sqlite3
from flask import Flask, render_template, request, jsonify,Blueprint

models = Blueprint('models', __name__)

# SQLite database file path
DB_FILE = 'tax_records.db'



# Create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tax_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    amount REAL NOT NULL,
                    payment_date DATE NOT NULL,
                    status TEXT NOT NULL,
                    due_date DATE NOT NULL,
                    tax_due REAL NOT NULL
                )''')
    conn.commit()
    conn.close()

create_table()