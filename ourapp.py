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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import BytesIO
import base64
import pandas as pd
from flask_caching import Cache

syms = pd.read_csv('ind_nifty50list.csv')
stock_list = syms['Symbol'].tolist()
dataframe = None

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Cache Work!!
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@cache.cached(timeout=1000, key_prefix='stocks')
def get_stock():
    return get_stock_data()

insession = False
usr = None

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    global usr
    return render_template("index.html", usr = usr)

@app.route("/market")
def market():
    global usr
    if not usr:
        flash('Please login to access this page.')
        return redirect(url_for('home', usr = usr))
    pe_ratio_filter = request.args.get('pe-ratio', type=float)
    last_price_filter = request.args.get('last-price', type=float)
    filtered_stocks = get_stock()
    
    if pe_ratio_filter is not None:
        filtered_stocks = [stock for stock in filtered_stocks if stock['PE'] >= pe_ratio_filter]
    if last_price_filter is not None:
        filtered_stocks = [stock for stock in filtered_stocks if stock['LastPrice'] >= last_price_filter]
    if 'reset' in request.form:
        filtered_stocks = get_stock()

    return render_template('market.html', stocks=filtered_stocks, usr = usr)

@app.route('/market/<string:symbol>', methods = ['GET', 'POST'])
def market_detail(symbol):
    global usr
    if not usr:
        flash('Please login to access this page.')
        return redirect(url_for('home', usr = usr))
    pdv = None
    if request.method == 'POST':
        duration = request.form['duration']
        entity = request.form['options']
        symbols = [symbol]
        if duration is not None and entity is not None:
            data = give_data(symbols, duration)
            figure = create_plot(data, entity, duration)
            pdv = po.plot(figure, output_type='div', include_plotlyjs=True)
    return render_template('singleplot.html', pdv = pdv, usr = usr)

@app.route("/plot", methods = ['GET', 'POST'])
def plot():
    global usr
    if not usr:
        flash('Please login to access this page.')
        return redirect(url_for('home', usr = usr))
    if request.method == 'POST':
        if 'submit' in request.form:
            num = int(request.form['num_stocks'])
            duration = request.form['duration']
            entity = request.form['options']
            return redirect(url_for('add_symbols', num=num, duration = duration, et = entity, usr = usr))
    return render_template('plot.html', error = None, usr = usr)

@app.route("/plot/stocks/<int:num>/<string:duration>/<string:et>", methods = ['GET', 'POST'])
def add_symbols(num, duration, et):
    global usr
    if not usr:
        flash('Please login to access this page.')
        return redirect(url_for('home', usr = usr))
    if request.method == 'POST':
        if 'submit' in request.form:
            symbols = [request.form[f'stock{i}'] for i in range(num)]
            for sym in symbols:
                if sym not in stock_list or sym is None:
                    error = 'Please provide correct stock symbols.'
                    return redirect(url_for('plot', error = error, usr = usr))
            data = give_data(symbols, duration)
            figure = create_plot(data, et, duration)
            pdv = po.plot(figure, output_type='div', include_plotlyjs=True)
            return render_template('num_stocks.html', num = num, pdv = pdv, error = None, usr = usr)
        if 'reset' in request.form:
            return redirect(url_for('plot', error = None, usr = usr))
    return render_template('num_stocks.html', num = num, pdv = None, error = None, usr = usr)
    
@app.template_filter('range')
def _jinja_range(number):
    return range(number)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global usr
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pwd = generate_password_hash(password, method = 'pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login', usr = usr))
    return render_template('register.html', usr = usr)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global usr
    if(request.method=='POST'):
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['logged_in'] = True
            usr = user.username
            return redirect(url_for('dashboard', usr = usr))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login', usr = usr))
    else:
        if usr is not None:
            return redirect(url_for('dashboard', usr = usr))
    return render_template('login.html', usr = usr)

@app.route('/dashboard')
def dashboard():
    global usr
    if usr is not None:
        return render_template('welcome.html', username=session['username'], usr = usr)
    else:
        return redirect(url_for('login', usr = usr))

@app.route('/logout')
def logout():
    global usr
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('logged_in', None)
    usr = None
    return redirect(url_for('home', usr = usr))

@app.route("/contact")
def contact():
    return render_template("contact.html", usr = usr)

@app.route("/about")
def about():
    return render_template("about.html", usr = usr)

if __name__ == "__main__":
    app.run(debug=True)
    
    
