
from flask import Flask,redirect, url_for, request, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from plot import give_data

from markets import get_stock_data
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import BytesIO
import base64
import pandas as pd

from flask_caching import Cache


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
stocks = []


#Cache Work!!
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@cache.cached(timeout=1000, key_prefix='stocks')
def get_stock():
    return get_stock_data()

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
    
    pe_ratio_filter = request.args.get('pe-ratio', type=float)
    last_price_filter = request.args.get('last-price', type=float)
    filtered_stocks = get_stock()

    if pe_ratio_filter is not None:
        filtered_stocks = [stock for stock in filtered_stocks if stock['PE'] >= pe_ratio_filter]
    if last_price_filter is not None:
        filtered_stocks = [stock for stock in filtered_stocks if stock['LastPrice'] >= last_price_filter]
    # Add more filter conditions as needed

    return render_template('market.html', stocks=filtered_stocks)


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
    if request.method == 'POST':
        num = int(request.form['num_stocks'])
        startdate = request.form['From']
        enddate = request.form['To']
        entity = request.form['options']
        return render_template('num_stocks.html', num=num, sd = startdate, ed = enddate, et = entity, plot_url = None)
    return render_template('plot.html')

@app.route("/plot/stocks", methods = ['GET', 'POST'])
def add_symbols():
    plot_url = None
    if request.method == 'POST':
        num = int(request.form['num'])
        startdate = request.form['sd']
        enddate = request.form['ed']
        entity = request.form['et']
        symbols = [request.form[f'stock{i}'] for i in range(num)]
        data = give_data(symbols, startdate, enddate)
        plt.figure(figsize=(10, 6))
        plt.style.use('ggplot')
        for i, sym in enumerate(data):
            plt.plot(data[sym]["DATE"], data[sym][entity], color = mpl.colormaps.get_cmap('tab10')(i), label = sym)
        plt.title(f'{entity} vs Date for these stocks')
        plt.xlabel('Date')
        plt.ylabel(entity)
        plt.grid(visible=False)
        plt.legend()
        plot_url = plot_to_url(plt)

    return render_template('num_stocks.html', num = num, plot_url = plot_url)
    
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
    stocks = get_stock()
    
