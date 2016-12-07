import os
import psycopg2.extras


from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit


app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24).encode('hex')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

prayer = [{'text':'my mom'}, {'text':'my dad'}]

def connect_to_db(): 
    connectionString = 'dbname = rosarydb user = db_manager password = rosary host = localhost'
    print connectionString
    try: 
        return psycopg2.connect(connectionString)
    except: 
        print("Can't connect to database")

@socketio.on('connect', namespace = '/rosary')
def makeConnection(): 
        print('connected')
        for p in prayer:
            print(p)
            emit('prayer', p)
            
@socketio.on('message', namespace = '/rosary')
def new_prayer(message): 
    tmp = {'text': message}
    print(tmp)
    prayer.append(tmp)
    emit('prayer', tmp, broadcast=True)

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
    empty_rosary = {
        'hail_mary': '',
        'our_father': '',
        'crucifix': '',
        'centerpiece': ''
    }
    return render_template('orderform.html', user = user, rosary = empty_rosary)

@app.route('/ordercomplete', methods=['GET','POST'])   
def ordercomplete():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
        
    con = connect_to_db()
    cur = con.cursor()
    if request.method == 'POST':
        try:
            cur.execute("""INSERT INTO customorders (user_name, hail_mary, our_father, crucifix, center_piece, price)
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
    con = connect_to_db()
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
    
@app.route('/catalog')
def catalog():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    
    con = connect_to_db()
    cur = con.cursor()
    
    rosaries = []
    
    query = cur.mogrify("SELECT primary_bead, secondary_bead, center_piece, crucifix, image FROM orders ORDER BY id;")
    cur.execute(query)
    results = cur.fetchall()
    
    for result in results:
        print(str(result[0]) + " " + str(result[1]) + " " + str(result[2]) + " " + str(result[3]) + " " + result[4])
    
    for result in results:
        total_price = 0
        
        query = cur.mogrify("SELECT bead_color, price_per_bead FROM stock_bead WHERE id = '%s';" % (result[0],))
        cur.execute(query)
        current_info = cur.fetchall()[0]
        primary_bead = current_info[0]
        total_price += current_info[1] * 30
        
        query = cur.mogrify("SELECT bead_color, price_per_bead FROM stock_bead WHERE id = '%s';" % (result[1],))
        cur.execute(query)
        current_info = cur.fetchall()[0]
        secondary_bead = current_info[0]
        total_price += current_info[1] * 8
        
        query = cur.mogrify("SELECT centerpiece_type, price_per_center_piece FROM stock_center_piece WHERE id = '%s';" % (result[2],))
        cur.execute(query)
        current_info = cur.fetchall()[0]
        center_piece = current_info[0]
        total_price += current_info[1]
        
        query = cur.mogrify("SELECT crucifix_type, price_per_crucifix FROM stock_crucifix WHERE id = '%s';" % (result[3],))
        cur.execute(query)
        current_info = cur.fetchall()[0]
        crucifix = current_info[0]
        total_price += current_info[1]
        
        rosaries.append({
            'primary_bead': primary_bead,
            'secondary_bead': secondary_bead,
            'center_piece': center_piece,
            'crucifix': crucifix,
            'image': "static/Image/" + result[4],
            'price': total_price
        })
    
    return render_template('catalog.html', user = user, rosaries = rosaries)
	
@app.route('/buy', methods=['GET','POST'])
def submit():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    
    if request.method == 'POST':
        print "User sent a POST request"
        
        rosary = {
            'hail_mary': request.form['primary_bead'],
            'our_father': request.form['secondary_bead'],
            'centerpiece': request.form['center_piece'],
            'crucifix': request.form['crucifix']
        }
        
        return render_template('orderform.html', user = user, rosary = rosary)
    
    print("Something went wrong; redirecting user to empty order form")
    
    empty_rosary = {
        'hail_mary': '',
        'our_father': '',
        'crucifix': '',
        'centerpiece': ''
    }
    
    return render_template('orderform.html', user = user, rosary = empty_rosary)
	
	
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    user = ' '
    if 'currentUser' in session: 
        print "there is a currentuser"
        user = session['currentUser']
        print user
    
    con = connect_to_db()
    cur = con.cursor()
    cur.execute("select distinct payment.first_name, payment.last_name, payment.home_address, payment.city, payment.zipcode, payment.card_number, customorders.user_name, customorders.hail_mary, customorders.our_father, customorders.crucifix, customorders.center_piece, customorders.price from payment join customorders on (payment.user_name = customorders.user_name);")
    results2 = cur.fetchall()
    if (len(results2) / 2 == 0):
        resultlen = len(results2) / 2;
    else:
        resultlen = len(results2) / 2 + 1;
    print(resultlen)
    cur.execute("select distinct payment.first_name, payment.last_name, payment.home_address, payment.city, payment.zipcode, payment.card_number, customorders.user_name, customorders.hail_mary, customorders.our_father, customorders.crucifix, customorders.center_piece, customorders.price from payment join customorders on (payment.user_name = customorders.user_name) limit %s;" % (resultlen))
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
    return render_template('Admin.html', user = user, results = results, resultlen = resultlen)
    

@app.route('/account', methods=['GET', 'POST'])
def account():  
    con = connect_to_db()
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
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
