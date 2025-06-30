from flask import Flask, render_template

app = Flask(__name__)

first_launch = True 

@app.route('/')
def index():
    global first_launch
    
    if first_launch:
        user = "Ivano"
        first_launch = False
    else:
        user = "Liam"
        first_launch = True

        
    return render_template('index.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
