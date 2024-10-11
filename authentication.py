from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '' 

# Temporary in-memory database for users
users_db = {}

@app.route('/')
def home():
    return "Welcome to Technique Tree! Go to /register to create an account or /login to login."

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            return "User already exists! Try logging in."
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')
        users_db[username] = hashed_password
        
        return redirect(url_for('login'))
    return '''
        <form method="POST">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Register">
        </form>
    '''

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username not in users_db:
            return "User not found! Please register first."
        
        # Check the hashed password
        if check_password_hash(users_db[username], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Incorrect password! Try again."
    
    return '''
        <form method="POST">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
    '''

# Dashboard after login
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Hello {session['user']}! Welcome to your dashboard."
    return redirect(url_for('login'))

# User Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
