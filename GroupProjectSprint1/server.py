import os
import psycopg2.extras


from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

 
def connect_to_dp(): 
    connectionString = 'dbname = rosarydb user = postgres password = 12345 host = localhost'
    print connectionString
    try: 
        return psycopg2.connect(connectionString)
    except: 
        print('nope')


@app.route('/')
def mainIndex():
    return render_template('home.html')

@app.route('/order')
def order():
    return render_template('orderform.html')
    
@app.route('/login')
def login():
    return render_template('login.html')
    
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

@app.route('/account', methods=['GET', 'POST'])
def account():  
    con = connect_to_dp()
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    pw =' '
    userName =' '
    firstName = ' '
    lastName = ' '
    admin = True
    
    if request.method == 'POST':
        print "post"
        userName = request.form['username']
        pw = request.form['pw']
        lastName = request.form['lastname']
        firstName = request.form['firstname']
        try:
            print cur.mogrify("INSERT INTO users (first_name, last_name, is_admin, username, password) VALUES (%s, %s, 'True', %s, crypt(%s, gen_salt('bf')));", (firstName, lastName, userName, pw))
            cur.execute("INSERT INTO users (first_name, last_name, is_admin, username, password) VALUES (%s, %s, 'True', %s, crypt(%s, gen_salt('bf')));", (firstName, lastName, userName, pw))
        except: 
            print "suck it nerd"
            con.rollback()
        con.commit()
        return render_template('logIn.html')
        
    return render_template('createAccount.html', selectedMenu='account', firstname = firstName, lastname = lastName, pw = pw, username = userName)
   

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
