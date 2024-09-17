from flask import Flask, jsonify, redirect, render_template, url_for, request, session
# from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import timedelta
import psycopg2


# Establish a connection to the database
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="DarulShifaClinic",
        user="postgres",
        password="..."
    )
    return conn

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'elixir' # Used to secure session cookie
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session timeout to 30 minutes

@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f'Select "fname", "pswd" from patient where email=\'{request.form["email"]}\';')
        data = cur.fetchone()
        if data:
            if bcrypt.check_password_hash(data[1], request.form["password"]):
                session["username"] = data[0]
                return redirect(url_for("go"))
            else:
                cur.close()
                conn.close()
                return "Invalid password!"
        else:
            cur.close()
            conn.close()
            return "Invalid username or password!"
    next_page = request.args.get('next')
    print(f'Next page on GET request: {next_page}') 
    return render_template("login.html", title="Login")

@app.route("/about")
def about():
    return "About page"

# Logout
@app.route('/logout')
def logout():
    session["username"] = None
    return redirect(url_for('login'))


# Accessing the account
@app.route('/home')
def go():
    if 'username' not in session or session["username"] == None:
        return redirect(url_for("login"))
    return render_template("index.html", title="Home")

# Register Page
@app.route("/register")
def register():
    return render_template("register.html", title="Register")

# Verify registration
@app.route("/abc", methods=["POST"])
def verify():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"Select * from patient where email='{request.form['email']}';")
    data = cursor.fetchone()
    if data:
        cursor.close()
        conn.close()
        return "This email is already in use!"
    hashed_password = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
    cursor.execute(f"INSERT INTO patient (fname, lname, dateofbirth, email, pswd, description)\nVALUES ('{request.form["first_name"]}', '{request.form["last_name"]}', TO_DATE('{request.form["birthdate"]}', 'YYYY-MM-DD'), '{request.form["email"]}', '{hashed_password}', 'Not verified');")
    conn.commit()
    if cursor.rowcount > 0:
        return "Check your Email"
    cursor.close()
    conn.close()
    return "Check your Email"

if __name__ == "__main__":
    app.run(debug=True)
