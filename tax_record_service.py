
import sqlite3
from flask import Flask, render_template, request, jsonify,Blueprint,redirect, url_for
from models import *


tax_record_service = Blueprint('tax_record_service', __name__)

# Function to insert a tax record into the database
def insert_tax_record(company, amount, payment_date, status, due_date, tax_due):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO tax_records (company, amount, payment_date, status, due_date, tax_due)
                VALUES (?, ?, ?, ?, ?, ?)''', (company, amount, payment_date, status, due_date, tax_due))
    conn.commit()
    conn.close()

@tax_record_service.route('/get_tax_records')
def get_tax_records():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT * FROM tax_records''')
    records = c.fetchall()
    conn.close()

    # Convert records to list of dictionaries
    tax_records = []
    for record in records:
        tax_records.append({
            'id': record[0],
            'company': record[1],
            'amount': record[2],
            'payment_date': record[3],
            'status': record[4],
            'due_date': record[5],
            'tax_due': record[6]
        })
    print("Function Triggered")

    return jsonify(tax_records)



@tax_record_service.route('/taxes', methods=['POST'])
def handle_tax_form():
    company = request.form['company']
    amount = float(request.form['amount'])
    payment_date = request.form['paymentDate']
    status = request.form['status']
    due_date = request.form['dueDate']
    # tax_rate = float(request.form['taxRate'])

    # # Calculate tax due based on tax rate
    # tax_rate = float(request.form['taxRate'])
    tax_rate = float(request.form.get('taxRate', 0.0))
    tax_due = amount * tax_rate
    
    # # Insert the record into the database
    insert_tax_record(company, amount, payment_date, status, due_date, tax_due)

  
    return 'Record added successfully.'


@tax_record_service.route('/delete_tax_record', methods=['DELETE'])
def delete_tax_record():
    id = request.args.get('id')
    # Delete the record from the database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''DELETE FROM tax_records WHERE id=?''', (id,))
    conn.commit()
    conn.close()
    return 'Record deleted successfully.'


@tax_record_service.route('/get_tax_record')
def get_tax_record():
    id = request.args.get('id')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT * FROM tax_records WHERE id=?''', (id,))
    record = c.fetchone()
    conn.close()

    if record:
        tax_record = {
            'id': record[0],
            'company': record[1],
            'amount': record[2],
            'payment_date': record[3],
            'status': record[4],
            'due_date': record[5]
        }
        return jsonify([tax_record])
    else:
        return jsonify([])
    
@tax_record_service.route('/update_tax_record', methods=['POST'])
def update_tax_record():
    id = request.form['id']
    company = request.form['company']
    amount = request.form['amount']
    payment_date = request.form['paymentDate']
    status = request.form['status']
    due_date = request.form['dueDate']

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''UPDATE tax_records SET company=?, amount=?, payment_date=?, status=?, due_date=? WHERE id=?''',
            (company, amount, payment_date, status, due_date, id))
    conn.commit()
    conn.close()

    return 'Record updated successfully.'