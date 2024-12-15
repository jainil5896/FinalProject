from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tax_payments.db"
db = SQLAlchemy(app)

class TaxPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)

@app.route("/")
def index():
    payments = TaxPayment.query.all()
    return render_template("index.html", payments=payments)

@app.route("/add_payment", methods=["POST"])
def add_payment():
    company = request.form["company"]
    amount = float(request.form["amount"])
    payment_date = datetime.strptime(request.form["payment_date"], "%Y-%m-%d")
    status = request.form["status"]
    due_date = datetime.strptime(request.form["due_date"], "%Y-%m-%d")
    tax_rate = float(request.form["tax_rate"])

    payment = TaxPayment(company=company, amount=amount, payment_date=payment_date, status=status, due_date=due_date, tax_rate=tax_rate)
    db.session.add(payment)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/update_payment/<int:payment_id>", methods=["POST"])
def update_payment(payment_id):
    payment = TaxPayment.query.get(payment_id)
    payment.company = request.form["company"]
    payment.amount = float(request.form["amount"])
    payment.payment_date = datetime.strptime(request.form["payment_date"], "%Y-%m-%d")
    payment.status = request.form["status"]
    payment.due_date = datetime.strptime(request.form["due_date"], "%Y-%m-%d")
    payment.tax_rate = float(request.form["tax_rate"])
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete_payment/<int:payment_id>")
def delete_payment(payment_id):
    payment = TaxPayment.query.get(payment_id)
    db.session.delete(payment)
    db.session.commit()

    return redirect(url_for("index"))

@app.route('/filter_payments', methods=['POST'])
def filter_payments():
    due_date = request.form.get('due_date')
    payments, total_amount, tax_rate, tax_due = get_payments_by_due_date(due_date)
    
    return render_template('filtered_results.html', payments=payments, total_amount=total_amount, tax_rate=tax_rate, tax_due=tax_due)

def get_payments_by_due_date(due_date):
    payments = []  
    total_amount = sum(payment['amount'] for payment in payments)
    tax_rate = 6  
    tax_due = (total_amount * tax_rate) / 100  

    return payments, total_amount, tax_rate, tax_due

@app.route('/ajax_filter_payments', methods=['POST'])
def ajax_filter_payments():
    due_date = request.form.get('due_date')
    payments, total_amount = get_payments_by_due_date(due_date)

    return render_template('filtered_results.html', payments=payments, total_amount=total_amount)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)