from urllib import request
from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import quote_plus 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
password = quote_plus("mysql@2023")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@localhost/userdetails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)



with app.app_context():
    db.create_all()

@app.route("/" , methods=['GET','POST'])
def signup2():
    message = None
    if request.method =='POST':
         email = request.form.get('email')
         password = request.form.get('password')
         renterpassword = request.form.get("renterpassword")

         if not email or not password:
             message = "Please enter both email and password."
         elif password != renterpassword:
             message = "password do not match!"
         else:
             existing_user = UserDetails.query.filter_by(email=email).first()
             if existing_user:
                 return redirect('login2')
             else:
            
         
                credentials = UserDetails(email=email, password=password)
                db.session.add(credentials)
                db.session.commit() 
                return redirect('login2') 
    return render_template('signup2.html', alert_message=message )

@app.route("/dashboard2", methods=['GET', 'POST'])
def dashboard2():
    if request.method == 'POST':
       
        mel = float(request.form['mel'])
        expenses = {
            "Grocery": float(request.form['grocery']),
            "Transport": float(request.form['transport']),
            "Education": float(request.form['education']),
            "Electricity": float(request.form['electricity']),
            "Water": float(request.form['water']),
            "Gas": float(request.form['gas']),
            "Others": float(request.form['others'])
        }

       
        for category, amount in expenses.items():
            expense_entry = Expense(category=category, amount=amount)
            db.session.add(expense_entry)
        db.session.commit()

    expenses_data = Expense.query.all()

    total_expenses = sum(exp.amount for exp in expenses_data)
    expense_summary = [
        {
            "category": exp.category,
            "amount": exp.amount,
            "percentage": (exp.amount / total_expenses) * 100 if total_expenses > 0 else 0
        }
        for exp in expenses_data
    ]

    
    mel = 50000  
    expenses_within_limit = total_expenses <= mel

    return render_template('dashboard2.html', 
                           expense_summary=expense_summary, 
                           total_expenses=total_expenses,
                           mel=mel, 
                           expenses_within_limit=expenses_within_limit)

@app.route('/login2', methods= ['GET','POST'])
def login2():
    
    message = None
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            message = "Please enter both email and password."
        else:
            user = UserDetails.query.filter_by(email=email, password=password).first()
            if not user:
                message = "User not found. Please sign up."
            elif user.password != password: 
                message = "Incorrect password."
            else:
                return redirect('dashboard2')

    return render_template('login2.html', alert_message=message)

if __name__ ==  "__main__":
    app.run(debug=True, use_reloader=True)
