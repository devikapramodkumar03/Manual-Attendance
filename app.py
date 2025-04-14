from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('manual_attendance'))

@app.route('/manual')
def manual_attendance():
    return render_template('manual_attendance.html')

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    name = request.form['name']
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)', (name, date, time))
    conn.commit()
    conn.close()

    return redirect(url_for('attendance_records'))

@app.route('/records')
def attendance_records():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance ORDER BY id DESC')
    records = c.fetchall()
    conn.close()
    return render_template('attendance_records.html', records=records)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
