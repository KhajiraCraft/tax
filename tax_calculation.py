import sqlite3
from flask import Flask, render_template, request, jsonify,Blueprint
from models import *
from tax_record_service import *

tax_calculation = Blueprint('tax_calculation', __name__)


@tax_calculation.route('/taxes', methods=['POST'])
def handle_tax_form():
    company = request.form['company']
    amount = float(request.form['amount'])
    payment_date = request.form['paymentDate']
    status = request.form['status']
    due_date = request.form['dueDate']
    
    # Calculate tax due based on tax rate (assuming tax rate is provided in the form)
    tax_rate = float(request.form['taxRate'])
    tax_due = amount * tax_rate
    
    # Insert the record into the database
    insert_tax_record(company, amount, payment_date, status, due_date, tax_due)
    
    # return redirect(url_for('tax_record_ui.allrecords'))
    return redirect(url_for('tax_record_ui.allrecord'))