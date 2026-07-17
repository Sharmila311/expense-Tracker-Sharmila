from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("expenses.db")

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    total = sum([row[1] for row in expenses]) if expenses else 0

    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cur.fetchall()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    conn.close()

    return render_template("index.html", expenses=expenses, total=total, labels=labels, values=values)

@app.route('/add', methods=['POST'])
def add():
    amount = request.form['amount']
    category = request.form['category']
    description = request.form['description']
    date = request.form['date']

    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                (amount, category, description, date))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)