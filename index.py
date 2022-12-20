from flask import Flask, render_template, request, session ,redirect
import psycopg2
from psycopg2.extras import RealDictCursor #Used for accesing data using column name
app = Flask(__name__)
app.secret_key = "exotics"
#DB Connection
conn = psycopg2.connect("dbname='ewebsite' host='localhost' user='sammueltuliao' password='sam1234' port='5432'")

#main
@app.route('/')
def index():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    psql = "select * from products"
    cursor.execute(psql)
    products = cursor.fetchall()
    return render_template('/index.html',products=products)

#home
@app.route('/home')
def home():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    psql = "select * from products"
    cursor.execute(psql)
    products = cursor.fetchall()
    return render_template('home.html',products=products)
#login
@app.route('/login', methods=['POST' , 'GET'])
def login():
  try:
    if request.method =="POST":  
        cursor = conn.cursor()
        username = request.form['username'];
        password = request.form['password'];
        Duser ="select username from customers where username ='"+username+"'";
        Dpass ="select password from customers where password ='"+password+"'";
        cursor.execute(Duser)
        Duser1 = cursor.fetchone()[0]
        cursor.execute(Dpass)
        Dpass1 = cursor.fetchone()[0]
        
        if (username == Duser1) and (password == Dpass1):
            session['logged_in'] = True;
            session['username'] = username;
            return "<script>alert('logged in Successfully!');window.location.href='/home';</script>"
        else :
            return  "<script>alert('log in Failed');window.location.href='/login';</script>"
    return render_template('login.html')
  except Exception as e: 
        return "<script>alert('log in Failed');window.location.href='/login';</script>"
        
  return render_template('login.html')
   
#register
@app.route('/register' , methods=['POST' , 'GET'])
def register():
  
  try:
    if request.method =="POST":
        fname = request.form['fname'];
        lname = request.form['lname'];
        gender = request.form['gender'];
        birthday = request.form['bday'];
        email_address = request.form['email'];
        username = request.form['username'];
        password = request.form['password'];
        contact = request.form['contact'];
        cursor = conn.cursor()
        psql = '''INSERT INTO customers (first_name, last_name, gender, birthday, email_address, username, password, contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
        data = (fname, lname, gender, birthday, email_address, username, password, contact)
        cursor.execute(psql, data)
        conn.commit()
        cursor.close()
        #conn.close()
        return "<script>alert('Register Successfully!');window.location.href='/login';</script>"
    return render_template('register.html')
  except Exception as e:
    return "<script>alert('Register failed');window.location.href='/register';</script>"
  
    return render_template('register.html')

#update
@app.route('/update', methods =['POST','GET'])
def update():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from customers where username='"+session['username']+ "'"
        cursor.execute(psql, id)
        customers = cursor.fetchone()
        return  render_template('edit.html',customers=customers) #(str(customers))
    except Exception as e:
        return  "<script>alert('Update failed');window.location.href='/update';</script>"
    return render_template('edit.html',customers=customers)



    #edit
@app.route('/edit' , methods=['POST' , 'GET'])
def edit():
  if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
  try:
    if request.method =="POST":
        fname = request.form['fname'];
        lname = request.form['lname'];
        gender = request.form['gender'];
        birthday = request.form['bday'];
        email_address = request.form['email'];
        username = request.form['username'];
        password = request.form['password'];
        contact = request.form['contact'];
        cursor = conn.cursor()
        psql = "update customers set first_name=%s,last_name=%s, gender=%s, birthday=%s, email_address=%s, username=%s, password=%s, contact=%s where username='"+session['username']+"'"
        data = (fname, lname, gender, birthday, email_address, username, password, contact)
        cursor.execute(psql, data)
        conn.commit()
        cursor.close()
        #conn.close()
        return "<script>alert('Update Successfully!');window.location.href='/edit';</script>"
    return render_template('edit.html')
  except Exception as e:
    return "<script>window.location.href='/update';</script>"
  
    return render_template('edit.html')




#logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')

#products
@app.route('/products', methods=['POST' , 'GET'])
def products():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        if request.method =="POST":
            name = request.form['name'];
            description = request.form['description'];
            price = request.form['price'];
            sku = request.form['sku'];
            stock = request.form['stock'];
            type = request.form['type'];
            category_name = request.form['category'];
            
            cursor = conn.cursor()
            psql = '''INSERT INTO products (name, description, price, sku, stock, brand, category_name) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
            data = (name, description, price, sku, stock, type, category_name)
            cursor.execute(psql, data)
            conn.commit()
            cursor.close()
            #conn.close()
            return "<script>alert('Product Listed Successfully!');window.location.href='/products';</script>"
        return render_template('products.html')
    except Exception as e:
        return "<script>alert('Product Listing Failed');window.location.href='/products';</script>"

    return render_template('products.html')
    
    
#searchindex
@app.route('/searchindex', methods=['POST' , 'GET'])
def searchindex():
    
    try:
        if request.method == "POST":
            search_query = request.form['search_query'];
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            psql = "select * from products where name like '%"+search_query+"%'"
            cursor.execute(psql)
            products = cursor.fetchall()
            return render_template('index.html',products=products) 
        return "<script>alert('No query');window.location.href='/';</script>" #(str(products))
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/';</script>"
    
    
    return render_template('index.html',products=products)
    
#searchhome
@app.route('/searchhome', methods=['POST' , 'GET'])
def searchhome():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        if request.method == "POST":
            search_query = request.form['search_query'];
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            psql = "select * from products where name like '%"+search_query+"%'"
            cursor.execute(psql)
            products = cursor.fetchall()
            return render_template('index.html',products=products) 
        return "<script>alert('No query');window.location.href='/';</script>" #(str(products))
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/';</script>"
    
    
    return render_template('index.html',products=products)

#Iarachnids
@app.route('/Iarachnids', methods=['POST' , 'GET'])
def Iarachnids():
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Arachnid%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('index.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/';</script>"
    
    return render_template('index.html',products=products)

#Ireptiles
@app.route('/Ireptiles', methods=['POST' , 'GET'])
def Ireptiles():
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Reptile%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('index.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/';</script>"
    
    return render_template('index.html',products=products)
    
 #Ifeeders
@app.route('/Ifeeders', methods=['POST' , 'GET'])
def Ifeeders():
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Feeder%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('index.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/';</script>"
    
    return render_template('index.html',products=products)
  
   #Imiscs
@app.route('/Imiscs', methods=['POST' , 'GET'])
def Imiscs():
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Miscellaneous%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('index.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/';</script>"
    
    return render_template('index.html',products=products)
    
    
    

#Harachnids
@app.route('/Harachnids', methods=['POST' , 'GET'])
def Harachnids():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Arachnid%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('home.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/home';</script>"
    
    return render_template('home.html',products=products)

#Hreptiles
@app.route('/Hreptiles', methods=['POST' , 'GET'])
def Hreptiles():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Reptile%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('home.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/home';</script>"
    
    return render_template('home.html',products=products)
    
 #Hfeeders
@app.route('/Hfeeders', methods=['POST' , 'GET'])
def Hfeeders():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Feeder%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('home.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/home';</script>"
    
    return render_template('home.html',products=products)
  
   #Hmiscs
@app.route('/Hmiscs', methods=['POST' , 'GET'])
def Hmiscs():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        psql = "select * from products where category_name like '%Miscellaneous%'"
        cursor.execute(psql)
        products = cursor.fetchall()           
        return render_template('home.html',products=products)
    except Exception as e:
        return  "<script>alert('No query');window.location.href='/home';</script>"
    
    return render_template('home.html',products=products)    
    
    
    
 #Irange
@app.route('/Irange', methods=['POST' , 'GET'])
def Irange():
    try:
        if request.method == "POST":
            min = request.form['price-min'];
            max = request.form['price-max'];
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            psql = "select * from products where price between " +min+ " and " +max+ ""
            cursor.execute(psql)
            products = cursor.fetchall()
            return render_template('index.html',products=products) 
        return "<script>alert('No query');window.location.href='/';</script>" #(str(products))
    except Exception as e:
        return " <script>alert('No query');window.location.href='/';</script>"
    
    
    return render_template('index.html',products=products)   
    
 
#Hrange
@app.route('/Hrange', methods=['POST' , 'GET'])
def Hrange():
    if session.get('logged_in') == None:
        return "<script>alert('You must be Logged In');window.location.href='/login';</script>"
    try:
        if request.method == "POST":
            min = request.form['price-min'];
            max = request.form['price-max'];
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            psql = "select * from products where price between " +min+ " and " +max+ ""
            cursor.execute(psql)
            products = cursor.fetchall()
            return render_template('home.html',products=products) 
        return "<script>alert('No query');window.location.href='/home';</script>" #(str(products))
    except Exception as e:
        return " <script>alert('No query');window.location.href='//home';</script>"
    
    
    return render_template('home.html',products=products) 
    
#copy
@app.route('/copy')
def copy():
    
    return render_template('copy.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
