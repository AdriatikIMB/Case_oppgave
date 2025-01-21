from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Funksjon for å sette opp databasen
def start_db():
    # Sjekk om databasen allerede eksisterer
    if not os.path.exists("tilbakemeldinger.db"):
        conn = sqlite3.connect("tilbakemeldinger.db")
        cursor = conn.cursor()
        # Opprett tabellen med de riktige kolonnene
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS tilbakemeldinger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                navn TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

start_db()  # Start databasen ved oppstart av appen

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Lagre dataene i databasen
    conn = sqlite3.connect("tilbakemeldinger.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tilbakemeldinger (navn, email, message) VALUES (?, ?, ?)", 
                   (name, email, message))  # Bruker plassholdere
    conn.commit()
    conn.close()

    # Vis resultatet
    return render_template('result.html', name=name, email=email, message=message)

# Route for å vise alle tilbakemeldinger
@app.route('/feedbacks', methods=['GET'])
def feedbacks():
    conn = sqlite3.connect("tilbakemeldinger.db")
    cursor = conn.cursor()
    cursor.execute("SELECT navn, email, message FROM tilbakemeldinger")
    feedback_list = cursor.fetchall()
    conn.close()
    
    return render_template('feedbacks.html', feedbacks=feedback_list)

if __name__ == '__main__':
    app.run(debug=True)
