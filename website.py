from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

TEMPLATE_OPTION = 0

# Function to create the database and necessary table(s)
def initialize_database():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Create the 'users' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            special_code TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the home page with a form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        special_code = request.form['special_code']
        
        # Save data to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, special_code) VALUES (?, ?)', (username, special_code))
        conn.commit()
        conn.close()    
    if(TEMPLATE_OPTION == 0):
        return render_template('./index.html')
    else:
        return render_template('./login.html')
        

# Route for the secondary page
@app.route('/login')
def secondary():
    global TEMPLATE_OPTION
    TEMPLATE_OPTION = 1
    return render_template('./login.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)