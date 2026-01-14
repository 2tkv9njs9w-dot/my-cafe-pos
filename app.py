from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    conn = sqlite3.connect('cafe_pos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    
    if user:
        session['username'] = user['username']
        # ບັນທັດນີ້ຈະພາເຈົ້າໄປໜ້າ POS ທັນທີ
        return redirect(url_for('pos')) 
    
    return "Login Failed! ກະລຸນາກວດຄືນ Username ຫຼື Password."

@app.route('/pos')
def pos():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('pos.html', products=products)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    total = data.get('total')
    if total and total > 0:
        conn = get_db_connection()
        conn.execute('INSERT INTO orders (total_price) VALUES (?)', (total,))
        conn.commit()
        conn.close()
        return {'status': 'success'}
    return {'status': 'error'}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)