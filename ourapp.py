from flask import Flask,redirect, url_for, request, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from plot import give_data, create_plot
from markets import get_stock_data
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as po
mpl.use('agg')
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import BytesIO
import base64
import pandas as pd

stock_list = ["ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", 
                "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", 
                "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", 
                "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "HDFC", "ICICIBANK", 
                "ITC", "IOC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", 
                "M&M", "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", 
                "SBILIFE", "SHREECEM", "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", 
                "TATASTEEL", "TECHM", "TITAN", "UPL", "ULTRACEMCO", "WIPRO"]

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/<name>/<entrynum>")
def user(name, entrynum):
    return f"Hello {name}! Your entry number is {entrynum}."

@app.route("/admin")
def admin():
    return render_template("second.html",content = "Testing")

@app.route("/market")
def market():
    stock_data = get_stock_data()
    return render_template("market.html", stocks= stock_data)

@app.route("/plot", methods = ['GET', 'POST'])
def plot():
    if request.method == 'POST':
        num = int(request.form['num_stocks'])
        duration = request.form['duration']
        entity = request.form['options']
        return render_template('num_stocks.html', num=num, duration = duration, et = entity)
    return render_template('plot.html')

@app.route("/plot/stocks", methods = ['GET', 'POST'])
def add_symbols():
    error = None
    pdv = None
    if request.method == 'POST':
        num = int(request.form['num'])
        duration = request.form['duration']
        entity = request.form['et']
        symbols = [request.form[f'stock{i}'] for i in range(num)]
        for sym in symbols:
            if(sym not in stock_list):
                return render_template('num_stocks.html', error = 1, num = num)
        data = give_data(symbols, duration)
        figure = create_plot(data, entity, duration)
        pdv = po.plot(figure, output_type='div', include_plotlyjs=True)

    return render_template('num_stocks.html', num = num, pdv = pdv, error = None)
    
@app.template_filter('range')
def _jinja_range(number):
    return range(number)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pwd = generate_password_hash(password, method = 'pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method=='POST'):
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
