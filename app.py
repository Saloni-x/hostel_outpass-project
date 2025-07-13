from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ------------------ Database Setup ------------------
def init_db():
    conn = sqlite3.connect('outpass.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT,
            reason TEXT,
            out_date TEXT,
            return_date TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# ------------------ Routes ------------------

# 1. Student Form Page
@app.route('/')
def student_form():
    return render_template('outpass_form.html')

# 2. Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    roll = request.form['roll']
    reason = request.form['reason']
    out_date = request.form['out_date']
    return_date = request.form['return_date']

    # Insert into database
    conn = sqlite3.connect('outpass.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (name, roll, reason, out_date, return_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, roll, reason, out_date, return_date))
    conn.commit()
    conn.close()

    return render_template('student_success.html', name=name)

# 3. Admin Login Page
@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

# 4. Admin Dashboard
@app.route('/dashboard')
def admin_dashboard():
    conn = sqlite3.connect('outpass.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', requests=requests)

# 5. Approve or Reject Request
@app.route('/update/<int:request_id>/<string:status>')
def update_status(request_id, status):
    conn = sqlite3.connect('outpass.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status=? WHERE id=?", (status, request_id))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

# ------------------ Run App ------------------
if __name__ == '__main__':
    app.run(debug=True)