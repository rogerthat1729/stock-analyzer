from flask import Flask,redirect, url_for, request, render_template
from plot import give_data
from markets import get_stock_data
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import stock_df
from io import BytesIO
import base64
import pandas as pd
app = Flask(__name__)

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

@app.route("/login")
def login():
    return render_template("login.html")

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

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
