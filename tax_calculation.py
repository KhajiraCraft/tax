import sqlite3
from flask import Flask, render_template, request, jsonify,Blueprint, redirect, url_for
from models import *
from tax_record_service import *
import json
tax_calculation = Blueprint('tax_calculation', __name__)


# @tax_calculation.route('/taxes', methods=['POST'])
# def handle_tax_form():
#     company = request.form['company']
#     amount = float(request.form['amount'])
#     payment_date = request.form['paymentDate']
#     status = request.form['status']
#     due_date = request.form['dueDate']
    
#     # Calculate tax due based on tax rate (assuming tax rate is provided in the form)
#     tax_rate = float(request.form.get('taxRate', 0.0))
#     tax_due = amount * tax_rate
    
#     # Insert the record into the database
#     insert_tax_record(company, amount, payment_date, status, due_date, tax_due)
    
#     return 'Record added successfully.'

@tax_calculation.route('/taxes', methods=['POST'])
def handle_tax_form():
    company = request.form['company']
    amount = float(request.form['amount'])
    payment_date = request.form['paymentDate']
    status = request.form['status']
    due_date = request.form['dueDate']
    tax_rate = float(request.form.get('taxRate', 0.0))
    tax_due = amount * tax_rate

    
    all_records_json = get_tax_records()
    
    # Parse JSON response
    all_records = json.loads(all_records_json)
    
    # Render the template with tax records data
    return render_template('all_records.html', records=all_records)
# render_template('all_records.html', records=all_records)


  