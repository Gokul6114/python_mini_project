from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS bills (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, amount REAL NOT NULL, date TEXT NOT NULL)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bills')
    bills = cursor.fetchall()
    conn.close()
    return render_template('index.html', bills=bills)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date = request.form['date']
        conn = sqlite3.connect('bills.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bills (name, amount, date) VALUES (?, ?, ?)', (name, amount, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date = request.form['date']
        cursor.execute('UPDATE bills SET name=?, amount=?, date=? WHERE id=?', (name, amount, date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM bills WHERE id=?', (id,))
    bill = cursor.fetchone()
    conn.close()
    return render_template('edit.html', bill=bill)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bills WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
