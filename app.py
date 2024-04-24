import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

# Function to insert a tax record into the database
def insert_tax_record(company, amount, payment_date, status, due_date, tax_due):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO tax_records (company, amount, payment_date, status, due_date, tax_due)
                VALUES (?, ?, ?, ?, ?, ?)''', (company, amount, payment_date, status, due_date, tax_due))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/taxes', methods=['POST'])
# def handle_tax_form():
#     company = request.form['company']
#     amount = float(request.form['amount'])
#     payment_date = request.form['paymentDate']
#     status = request.form['status']
#     due_date = request.form['dueDate']
    
#     # Calculate tax due based on tax rate (assuming tax rate is provided in the form)
#     tax_rate = float(request.form['taxRate'])
#     tax_due = amount * tax_rate
    
#     # Insert the record into the database
#     insert_tax_record(company, amount, payment_date, status, due_date, tax_due)
    
#     return 'Record added successfully.'

@app.route('/get_tax_records')
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

# #Start of Code Test
# @app.route('/get_tax_records')
# def get_tax_records():
#     due_date = request.args.get('due_date')
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()

#     if due_date:
#         c.execute('''SELECT * FROM tax_records WHERE due_date=?''', (due_date,))
#     else:
#         c.execute('''SELECT * FROM tax_records''')

#     records = c.fetchall()
#     conn.close()

#     # Convert records to list of dictionaries
#     tax_records = []
#     for record in records:
#         tax_records.append({
#             'id': record[0],
#             'company': record[1],
#             'amount': record[2],
#             'status': record[3],
#             'due_date': record[4]
#         })

#     return jsonify(tax_records)


#End Code Test

#Start Code Test
@app.route('/taxes', methods=['POST'])
def handle_tax_form():
    company = request.form['company']
    amount = float(request.form['amount'])
    payment_date = request.form['paymentDate']
    status = request.form['status']
    due_date = request.form['dueDate']
    tax_rate = float(request.form['taxRate'])

    # Calculate tax due based on tax rate
    tax_due = amount * tax_rate

    # Insert the record into the database
    insert_tax_record(company, amount, payment_date, status, due_date, tax_due)

    return 'Record added successfully.'


#End of code test

@app.route('/delete_tax_record', methods=['DELETE'])
def delete_tax_record():
    id = request.args.get('id')
    # Delete the record from the database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''DELETE FROM tax_records WHERE id=?''', (id,))
    conn.commit()
    conn.close()
    return 'Record deleted successfully.'


@app.route('/get_tax_record')
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

@app.route('/update_tax_record', methods=['POST'])
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




if __name__ == '__main__':
    app.run(debug=True)
