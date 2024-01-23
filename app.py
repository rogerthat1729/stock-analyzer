from flask import Flask, render_template, request, redirect
from plot import plot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form['Stock Symbol']
        date_input1 = request.form['From']
        date_input2 = request.form['To']

        plot_url = plot(text_input, date_input1, date_input2)

        return render_template('plot.html', plot_url=plot_url)
    
    return render_template('plot.html', plot_url=None)

if __name__ == "__main__":
    app.run(debug=True)