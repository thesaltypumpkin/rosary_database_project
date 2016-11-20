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
            cur.execute("""INSERT INTO customorders (user_name, hail_mary, our_father, price)
            VALUES (%s, %s, %s, %s);""",
            (user, request.form['hail_mary_color'], request.form['our_father_color'], '40') )
        except: 
            print 'nope'
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
            print 'nope'
            con.rollback()
        con.commit()
        
    return render_template('ordercomplete.html', user = user )
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    con = connect_to_dp()
    cur = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        username = request.form['username']
        pw = request.form['pw']
        try: 
            print 'got this far'
            print cur.mogrify("select * from users WHERE username = %s' AND password = crypt(%s, password)", (username, pw))
            cur.execute("select * from users WHERE username = %s AND password = crypt(%s, password)", (username, pw))
        except:
            print "no"
        
        if cur.fetchone():
            session['currentUser'] = request.form['username']
            currentUser = session['currentUser']
            print currentUser
            return redirect(url_for('mainIndex', user=currentUser))
            
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
        
    return render_template('createAccount.html', selectedMenu='account', firstname = firstName, lastname = lastName, pw = pw, username = userName, user = user)
   

# start the server
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
