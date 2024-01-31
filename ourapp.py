from flask import Flask,redirect, url_for, request, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from plot import give_data, create_plot, get_index_data, get_performers, get_current_data
from news import get_stock_news
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
    data = get_current_data()
    return reversed(data)

@cache.cached(timeout=2000, key_prefix='news')
def get_news():
    return get_stock_news()

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

@app.route('/market/<symbol>', methods = ['GET', 'POST'])
def market_detail(symbol):
    global usr
    data = None
    if not usr:
        flash('Please login to access this page.')
        return redirect(url_for('home', usr = usr))
    pdv = None
    if request.method == 'POST':
        entity = request.form['options']
        typ = request.form['plottype']
        symbols = [symbol]
        if entity is not None and typ is not None:
            data = give_data(symbols)
            figure = create_plot(data, entity, 'stock',typ)
            pdv = po.plot(figure, output_type='div', include_plotlyjs=True)
    return render_template('singleplot.html', symbol = symbol, pdv = pdv, usr = usr, type = 'stock', data = data)

@app.route("/plot", methods = ['GET', 'POST'])
def plot():
    global usr
    if not usr:
        flash('Please login to access this page.')
        return redirect(url_for('home', usr = usr))
    if request.method == 'POST':
        if 'submit' in request.form:
            num = int(request.form['num_stocks'])
            typ = request.form['plottype']
            entity = request.form['options']
            return redirect(url_for('add_symbols', num=num, et = entity, usr = usr, typ = typ))
    return render_template('plot.html', error = None, usr = usr)

@app.route("/plot/stocks/<int:num>/<string:et>/<string:typ>", methods = ['GET', 'POST'])
def add_symbols(num, et, typ):
    global usr
    data = None
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
            data = give_data(symbols)
            figure = create_plot(data, et, 'stock', typ)
            pdv = po.plot(figure, output_type='div', include_plotlyjs=True)
            return render_template('num_stocks.html', num = num, pdv = pdv, error = None, usr = usr, data = data)
        if 'reset' in request.form:
            return redirect(url_for('plot', error = None, usr = usr))
    return render_template('num_stocks.html', num = num, pdv = None, error = None, usr = usr, data = data)
    
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
        news_data = get_news()
        return render_template('welcome.html', username=session['username'], usr = usr, news_data = news_data['articles'][:4])
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

@app.route("/news")
def latest_news():
    global usr
    news_data = get_news() 
    return render_template('news.html', news_articles=news_data['articles'], usr = usr)

@app.route('/nifty50', methods = ['GET', 'POST'])
def indices():
    global usr
    df = get_index_data()
    dataframe = None
    if not usr:
        flash('Please login to access this page.')
        return redirect(url_for('home', usr = usr))
    pdv = None
    if request.method == 'POST':
        entity = request.form['options']
        typ = request.form['plottype']
        dataframe = {'NIFTY50': df}
        if entity is not None and typ is not None:
            figure = create_plot(dataframe, entity, 'index', typ)
            pdv = po.plot(figure, output_type='div', include_plotlyjs=True)
    return render_template('singleplot.html', usr = usr, type = 'index', symbol = 'NIFTY50', pdv = pdv, data = dataframe)

@app.route("/performers", methods = ['GET'])
def gainers_and_losers():
    global usr
    gainers, losers = get_performers()
    return render_template("performers.html", usr = usr, gainers = gainers, losers = losers)

if __name__ == "__main__":
    app.run(debug=True)
    
    
