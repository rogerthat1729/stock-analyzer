from flask import Flask,redirect,url_for, render_template
from markets import get_stock_data
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

@app.route("/plot")
def plot():
    return render_template("plot.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True)
