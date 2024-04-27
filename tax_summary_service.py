import sqlite3
from flask import Flask, render_template, request, jsonify,Blueprint
from models import *


tax_summary_service = Blueprint('tax_summary_service', __name__)


@tax_summary_service.route('/get_tax_summary_records')
def get_tax_summary_records():
    due_date = request.args.get('due_date')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    
    c.execute('''SELECT * FROM tax_records WHERE due_date=?''', (due_date,))
    

    records = c.fetchall()
    conn.close()

    # Convert records to list of dictionaries
    tax_records = []
    for record in records:
        tax_records.append({
            'id': record[0],
            'company': record[1],
            'amount': record[2],
            'status': record[3],
            'due_date': record[4]
        })

    return jsonify(tax_records)