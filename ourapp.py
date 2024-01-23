
from flask import Flask,redirect, url_for, request, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from plot import give_data

from markets import get_stock_data
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import BytesIO
import base64
import pandas as pd

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

@app.route("/")  # Going to the default domain automatically sends us here
def home():
    return render_template("index.html")

@app.route("/<name>/<entrynum>")
def user(name, entrynum):
    return f"Hello {name}! Your entry number is {entrynum}."

@app.route("/admin")
def admin():
    return render_template("second.html",content = "Testing")

@app.route("/admin1")
def admin1():
    return redirect(url_for("user", name="Aqweqd", entrynum="1212"))

@app.route("/market")
def market():
    stock_data = get_stock_data()
    return render_template("market.html", stocks= stock_data)

def plot_to_url(plt):
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    buffer = b''.join(buf)
    buffer_base64 = base64.b64encode(buffer)
    plt.close()
    return buffer_base64.decode('utf-8')

@app.route("/plot", methods = ['GET', 'POST'])
def plot():
    plot_url = None
    if request.method == 'POST':
        symbol = request.form['Stock Symbol']
        startdate = request.form['From']
        enddate = request.form['To']

        entity = request.form['options']
        colors = {'OPEN':'red', 'CLOSE':'green', 'LTP':'blue'}
        data = give_data(symbol, startdate, enddate)

        plt.figure(figsize=(10, 6))
        plt.style.use('ggplot')
        plt.plot(data["DATE"], data[entity], color = colors[entity])
        plt.title(f'{symbol} {entity} vs Date')
        plt.xlabel('Date')
        plt.ylabel(entity)
        plot_url = plot_to_url(plt)

    return render_template('plot.html', plot_url=plot_url)

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
        return redirect(url_for('home'))
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
