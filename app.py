from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import hashlib


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a more secure secret key


# Database initialization and table creation
def start_db():
    db_path = os.path.join(os.path.dirname(__file__), 'tilbakemeldinger.db')
    # if not os.path.exists(db_path):
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            cursor = conn.cursor()
            print("Creating database and tables...")  # Debugging print
            # Create the "brukere" (users) table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS brukere (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()
            # Create the "tilbakemeldinger" (feedbacks) table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tilbakemeldinger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    navn TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            ''')
            conn.commit()
        print("Database and tables created successfully.")  # Debugging print
    except Exception as e:
        print(f"Error creating database: {e}")
    # else:
        # print("Database already exists.")
# start_db()

# Function to execute database queries
def execute_query(query, params=(), fetchone=False, fetchall=False):
    try:
        with sqlite3.connect("tilbakemeldinger.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    if not name or not email or not message:
        return "Alle feltene må fylles ut! <a href='/'>Gå tilbake</a>"
    
    execute_query("INSERT INTO tilbakemeldinger (navn, email, message) VALUES (?, ?, ?)", 
                  (name, email, message))

    return render_template('result.html', name=name, email=email, message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password before storing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Check if email is already registered
        existing_user = execute_query("SELECT id FROM brukere WHERE email = ?", (email,), fetchone=True)
        if existing_user:
            return "E-posten er allerede registrert! <a href='/login'>Logg inn her</a>"

        # Store the new user
        execute_query("INSERT INTO brukere (email, password) VALUES (?, ?)", (email, hashed_password))
        
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')

        # Hash the password to compare with the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Debugging: print hashed password
        print("Hashed password from input:", hashed_password)

        # Check if user exists in the database with the correct password
        user = execute_query("SELECT id, password FROM brukere WHERE email = ?", (email,), fetchone=True)
        
        if user:
            stored_password = user[1]  # The stored hashed password
            print("Stored hashed password:", stored_password)  # Debugging stored password
            
            if hashed_password == stored_password:
                # Set the user in session to keep them logged in
                session['user_id'] = user[0]
                print("Session user_id:", session.get('user_id'))  # Debugging session
                # Redirect to the feedbacks page after login
                return redirect(url_for('feedbacks'))
            else:
                # If passwords don't match, show error message
                return render_template('login.html', error_message="Feil e-post eller passord! Prøv igjen.")
        else:
            return render_template('login.html', error_message="Feil e-post eller passord! Prøv igjen.")
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/feedbacks', methods=['GET'])
def feedbacks():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # If not logged in, send user to login page
    
    # Fetch feedbacks from the database
    feedback_list = execute_query("SELECT navn, email, message FROM tilbakemeldinger", fetchall=True)
    
    # Return feedbacks page with the feedback list
    return render_template('feedbacks.html', feedbacks=feedback_list)


if __name__ == '__main__':
    start_db()  # Ensure the database is initialized before starting the app
    app.run(debug=False, use_reloader=False)
