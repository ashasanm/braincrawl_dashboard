from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ===================== DB SETTINGS ==========================================================

# connecting to mongoDB
cluster = MongoClient("mongodb+srv://hasan:hasan1030@cluster0.b0ahy.gcp.mongodb.net/brainly?retryWrites=true&w=majority")

# select database and collection
db = cluster['brainly']
collection = db['user']
col_acc = db['account']

# ====================== INDEX ======================================================

@app.route('/')
def index():
    # check if session exist
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    return redirect(url_for('login'))

# ======================= LOGIN ===============================================================

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # getting data from login.html
        username = request.form['username']
        password = request.form['password']
        # find data collection by username
        acc_data = col_acc.find({'username': username})
        for data in acc_data:
            # username from db
            db_username = data['username']
            # password from db
            db_password = data['password']
            # check username and password
            if db_username == username and check_password_hash(db_password, password) == True:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Incorrect Email or Password!!!', 'info')
                return render_template('login.html')
    return render_template('login.html')

# ======================= REGISTER ============================================================

@app.route('/register', methods=['POST', 'GET'])
def registration():
    # get email from register form
    res = request.args.get('user_email')
    user_data = {'email': res}
    # get data from db by email
    search_res = col_acc.find(user_data)
    
    if request.method == "POST":
        if res not in search_res:
            print('acc created')
            # get data from registration form
            user_email = request.form.get('user_email')
            username = request.form.get('username')
            password = request.form.get('password')
            # encrypt password
            hashed_password = generate_password_hash(password)
            user_data = {'email': user_email, 'username': username, 'password':hashed_password}
            # save user info to db
            col_acc.save(user_data)
            return render_template('login.html')
        else:
            print('acc creation failed')
            flash('Email already registered!!!', 'info')
            return render_template('register.html')
    else:
        return render_template('register.html')
                
#=========================== DASHBOARD ========================================================

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')    

# ========================== USER LIST ========================================================

@app.route('/brainly_user_list', methods=['GET'])
def user_list():
    # get all data in collection
    all_data = collection.find()
    return render_template('user_list.html', datas=all_data)

# ============================ SEARCH ========================================================       

@app.route("/find_user", methods=['GET'])
def search():
    return render_template('find_user.html')

# ========================= SEARCH RESULT ======================================================

@app.route("/result")
def result():
    # get data from html form
    res = request.args.get('user_url')
    user_data = {'url': res}
    # mongoDB query for finding data
    search_res = collection.find(user_data)
    return render_template('result.html', content=search_res)

# ========================= LOGOUT    

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template('logout.html')

if __name__ == "__main__":
    app.secret_key = 'rahasiaIlahI'
    app.run(debug=True)
