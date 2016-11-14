import os
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def mainIndex():
    return render_template('home.html')

@app.route('/order')
def order():
    return render_template('orderform.html')
    
@app.route('/login')
def login():
    return render_template('logIn.html')
    
@app.route('/about')
def about():
    return render_template('About.html')
    
@app.route('/premade')
def premade():
    return render_template('PremadeItems.html')
    
@app.route('/catalog')
def catalog():
    return render_template('catalog.html')
    
@app.route('/admin')
def admin():
    return render_template('Admin.html')

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
