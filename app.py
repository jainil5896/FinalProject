from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('tax_payments.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/payments', methods=['GET', 'POST'])
def manage_payments():
    if request.method == 'POST':
        # Insert new payment record
        print("POST call")
        data = request.json
        conn = get_db_connection()
        conn.execute('INSERT INTO payments (company, amount, payment_date, status, due_date) VALUES (?, ?, ?, ?, ?)',
                     (data['company'], data['amount'], data['payment_date'], data['status'], data['due_date']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Payment added'}), 201
    else:
        # Retrieve all payment records
        conn = get_db_connection()
        payments = conn.execute('SELECT * FROM payments').fetchall()
        conn.close()
        return jsonify([dict(payment) for payment in payments])

if __name__ == '__main__':
    app.run(debug=True)