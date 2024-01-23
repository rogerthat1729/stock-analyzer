from flask import Flask,redirect, url_for, request, render_template

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
    items = [
        {"id": 1, "name": "Phone", "barcode": "893212299897", "price": 500},
        {"id": 2, "name": "Laptop", "barcode": "123985473165", "price": 900},
        {"id": 3, "name": "Keyboard", "barcode": "231985128446", "price": 150}
    ]
    return render_template("market.html", items=items)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/plot", methods = ['GET', 'POST'])
def plot():
    if request.method == 'POST':
        text_input = request.form['Stock Symbol']
        date_input1 = request.form['From']
        date_input2 = request.form['To']

        plot_url = plot(text_input, date_input1, date_input2)

        return render_template('plot.html', plot_url=plot_url)
    
    return render_template('plot.html', plot_url=None)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True)
