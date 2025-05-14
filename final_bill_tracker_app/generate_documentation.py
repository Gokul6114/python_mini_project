from fpdf import FPDF

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Complete Project Documentation", ln=True, align="C")
pdf.ln(5)

# Define sections
sections = [
    ("1. Python Backend (app.py)", """from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bills.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )''')
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
    app.run(debug=True)"""),
    ("2. Template: index.html", """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Utility Bill Records</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light text-dark">
    <div class="container mt-5">
        <h1 class="mb-4 text-center text-primary">💡 Utility Bill Tracker</h1>
        <div class="mb-3 text-end">
            <a href="/add" class="btn btn-success">+ Add New Bill</a>
        </div>
        <table class="table table-bordered table-hover bg-white">
            <thead class="table-dark">
                <tr><th>ID</th><th>Name</th><th>Amount</th><th>Date</th><th>Actions</th></tr>
            </thead>
            <tbody>
                {% for bill in bills %}
                <tr>
                    <td>{{ bill[0] }}</td>
                    <td>{{ bill[1] }}</td>
                    <td>{{ bill[2] }}</td>
                    <td>{{ bill[3] }}</td>
                    <td>
                        <a href="/edit/{{ bill[0] }}" class="btn btn-sm btn-primary">Edit</a>
                        <a href="/delete/{{ bill[0] }}" class="btn btn-sm btn-danger">Delete</a>
                    </td>
                </tr>
                {% else %}
                <tr><td colspan="5" class="text-center">No bills yet</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>"""),
    ("3. Template: add.html", """<!DOCTYPE html>
<html>
<head>
    <title>Add Bill</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h2>Add New Bill</h2>
        <form method="post">
            <div class="mb-3"><label>Name</label><input name="name" class="form-control" required></div>
            <div class="mb-3"><label>Amount</label><input name="amount" type="number" step="0.01" class="form-control" required></div>
            <div class="mb-3"><label>Date</label><input name="date" type="date" class="form-control" required></div>
            <button class="btn btn-success">Add</button>
            <a href="/" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</body>
</html>"""),
    ("4. Template: edit.html", """<!DOCTYPE html>
<html>
<head>
    <title>Edit Bill</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h2>Edit Bill</h2>
        <form method="post">
            <div class="mb-3"><label>Name</label><input name="name" value="{{ bill[1] }}" class="form-control" required></div>
            <div class="mb-3"><label>Amount</label><input name="amount" type="number" value="{{ bill[2] }}" step="0.01" class="form-control" required></div>
            <div class="mb-3"><label>Date</label><input name="date" type="date" value="{{ bill[3] }}" class="form-control" required></div>
            <button class="btn btn-primary">Update</button>
            <a href="/" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</body>
</html>"""),
    ("5. SQL Queries", """-- Create Table
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_name TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
);

-- Insert Sample
INSERT INTO bills (bill_name, amount, date)
VALUES ('Electricity', 1500.00, '2025-05-01');

-- Read
SELECT * FROM bills;

-- Update
UPDATE bills SET amount = 2000.00 WHERE id = 1;

-- Delete
DELETE FROM bills WHERE id = 1;

-- Optional: Count
SELECT COUNT(*) FROM bills;

-- Optional: Greater than
SELECT * FROM bills WHERE amount > 1000;

-- Optional: Sort
SELECT * FROM bills ORDER BY date DESC;""")
]

# Write each section
for title, text in sections:
    pdf.set_font("Arial", "B", 14)
    pdf.ln(5)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(2)
    pdf.set_font("Courier", size=10)
    for line in text.splitlines():
        pdf.multi_cell(0, 5, line)
    pdf.ln(4)

# Save PDF
pdf.output("Complete_Project_Documentation.pdf")
