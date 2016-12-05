import os
import psycopg2.extras


from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit


app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24).encode('hex')
socketio = SocketIO(app)
 
def connect_to_dp(): 
    connectionString = 'dbname = rosarydb user = db_manager password = rosary host = localhost'
    print connectionString
    try: 
        return psycopg2.connect(connectionString)
    except: 
        print("Can't connect to database")

messages = [{'star': "1", 'review': 'this is shit'}, {'star': "5", 'review': 'best rosary ever'}]


@app.route('/')
def mainIndex():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
        
    return render_template('home.html', user = user)

@app.route('/order')
def order():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    return render_template('orderform.html', user = user)

@app.route('/ordercomplete', methods=['GET','POST'])   
def ordercomplete():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
        
    con = connect_to_dp()
    cur = con.cursor()
    if request.method == 'POST':
        try:
            cur.execute("""INSERT INTO customorders (user_name, hail_mary, our_father, Crucifix, center_piece, price)
            VALUES (%s, %s, %s, %s, %s, %s);""",
            (user, request.form['hail_mary_color'], request.form['our_father_color'], request.form['crucifix'], request.form['centerpiece'], '40') )
        except: 
            print 'Error: could not add order to the database'
            con.rollback()
        con.commit()
        print 'Order Added'
        
        try:
            print(cur.mogrify("""INSERT INTO payment (user_name, first_name, last_name, home_address, city, state, zipcode, card_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            (user, request.form['first_name'], request.form['last_name'], request.form['street'], request.form['city'],
             request.form['state'], request.form['zipcode'], request.form['card_number'] ) ) )
             
            cur.execute("""INSERT INTO payment (user_name, first_name, last_name, home_address, city, state, zipcode, card_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            (user, request.form['first_name'], request.form['last_name'], request.form['street'], request.form['city'],
             request.form['state'], request.form['zipcode'], request.form['card_number'] ) )
        except: 
            print 'Error: could not add payment method to the database'
            con.rollback()
        con.commit()
        
    return render_template('ordercomplete.html', user = user )
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    con = connect_to_dp()
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "User sent a POST request"
        username = request.form['username']
        pw = request.form['pw']
        try: 
            print cur.mogrify("select * from users WHERE username = %s AND password = crypt(%s, password)", (username, pw))
            cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (username, pw))
        except:
            print "Error: could not retrieve user info"
        
        if cur.fetchone():
            session['currentUser'] = request.form['username']
            currentUser = session['currentUser']
            print currentUser
            return redirect(url_for('mainIndex', user=currentUser))
            
    return render_template('logIn.html')
    
@app.route('/about')
def about():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    return render_template('About.html', user = user)
    
@app.route('/premade')
def premade():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    return render_template('PremadeItems.html', user = user)
    
@app.route('/catalog')
def catalog():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    return render_template('catalog.html', user = user)
    
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    
    con = connect_to_dp()
    cur = con.cursor()
    cur.execute("select payment.first_name, payment.last_name, payment.home_address, payment.city, payment.zipcode, payment.card_number, customorders.user_name, customorders.hail_mary, customorders.our_father, customorders.crucifix, customorders.center_piece, customorders.price from payment join customorders on (payment.user_name = customorders.user_name);")
    results = cur.fetchall()
    if request.method == 'POST':
        print("post admin")
        if request.form['submit'] == "Update Bead":
            print cur.mogrify("update stock_bead set quantity = quantity + %s where bead_color = '%s'" % (request.form['bead_number'], request.form['bead_color']))
            cur.execute("update stock_bead set quantity = quantity + %s where bead_color = '%s'" % (request.form['bead_number'], request.form['bead_color']))
            con.commit()
        elif request.form['submit'] == "update centerpiece":
            print cur.mogrify("update stock_center_piece set quantity = quantity + %s where centerpiece_type = '%s'" % (request.form['cp_amount'], request.form['cp_type']))
            cur.execute("update stock_center_piece set quantity = quantity + %s where centerpiece_type = '%s'" % (request.form['cp_amount'], request.form['cp_type']))
            con.commit()
        elif request.form['submit'] == "update crucifix":
            print cur.mogrify("update stock_crucifix set quantity = quantity + %s where crucifix_type = '%s'" % (request.form['cx_amount'], request.form['cx_type']))
            cur.execute("update stock_crucifix set quantity = quantity + %s where crucifix_type = '%s'" % (request.form['cx_amount'], request.form['cx_type']))
            con.commit()
    return render_template('Admin.html', user = user, results = results)
    

@app.route('/account', methods=['GET', 'POST'])
def account():  
    con = connect_to_dp()
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    
    pw =' '
    userName =' '
    firstName = ' '
    lastName = ' '
    admin = True
    
    if request.method == 'POST':
        print "User sent a POST request"
        userName = request.form['username']
        pw = request.form['pw']
        lastName = request.form['lastname']
        firstName = request.form['firstname']
        try:
            print cur.mogrify("INSERT INTO users (first_name, last_name, is_admin, username, password) VALUES (%s, %s, True, %s, crypt(%s, gen_salt('bf')));", (firstName, lastName, userName, pw))
            cur.execute("INSERT INTO users (first_name, last_name, is_admin, username, password) VALUES (%s, %s, 'True', %s, crypt(%s, gen_salt('bf')));", (firstName, lastName, userName, pw))
        except: 
            print "Error: could not insert new user into database"
            con.rollback()
        con.commit()
        return render_template('logIn.html')
        
    return render_template('createAccount.html', selectedMenu='account', firstname = firstName, lastname = lastName, pw = pw, username = userName, user = user)
   
   
@app.route('/review')
def review():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    
    return render_template('review.html')
    
# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
