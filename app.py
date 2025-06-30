from flask import Flask, render_template, request

app = Flask(__name__)

user_age = 25
user_name = "Unknown"

@app.route('/', methods=['GET', 'POST'])
def index():
    global user_age, user_name

    if request.method == 'POST':
        user_age = int(request.form.get('age', user_age))
        user_name = request.form.get('name', user_name)

    return render_template('index.html', user_age=user_age, user_name=user_name)

if __name__ == '__main__':
    app.run(debug=True)
