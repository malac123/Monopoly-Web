from flask import Flask, render_template, request

app = Flask(__name__)

user_name = "Unbekannt"

@app.route('/', methods=['GET', 'POST'])
def index():
    global user_name
    if request.method == 'POST':
        user_name = request.form['name']
    return render_template('index.html', user_name=user_name)

@app.route('/mainpage')
def mainpage():
    global user_name
    if request.method == 'POST':
        user_name = request.form['name']
    return render_template('mainpage.html', user_name=user_name)
if __name__ == '__main__':
    app.run(debug=True)
