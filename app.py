from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Participants Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            college TEXT NOT NULL,
            event TEXT NOT NULL,
            reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Events Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            date TEXT NOT NULL,
            venue TEXT NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT,
            event_type TEXT DEFAULT 'Technical'
        )
    ''')

    # Migration: Add event_type column if it doesn't exist (for existing DBs)
    try:
        cursor.execute('ALTER TABLE events ADD COLUMN event_type TEXT DEFAULT "Technical"')
        print("Migrated: Added event_type column to events table.")
    except sqlite3.OperationalError:
        # Column likely already exists
        pass

    # Feedback Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            rating INTEGER
        )
    ''')
    
    # Check if events are empty, if so, add some defaults
    cursor.execute('SELECT count(*) FROM events')
    if cursor.fetchone()[0] == 0:
        default_events = [
            ('Tech Talk 2024', 'Oct 15, 2024', 'Main Auditorium', 'A deep dive into AI and Future Tech.', 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&q=80&w=1000', 'Technical'),
            ('Coding Hackathon', 'Nov 05, 2024', 'Computer Labs', '24-hour coding marathon. Win big prizes!', 'https://images.unsplash.com/photo-1504384308090-c54be3855833?auto=format&fit=crop&q=80&w=1000', 'Technical'),
            ('Gaming Tournament', 'Dec 01, 2024', 'Student Center', 'Valorant, FIFA, and more. Register to play.', 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=1000', 'Entertainment'),
            ('Comedy Night', 'Jan 20, 2025', 'City Hall', 'Stand-up comedy special.', 'https://images.unsplash.com/photo-1585699324551-f6089501104d?auto=format&fit=crop&q=80&w=1000', 'Entertainment')
        ]
        cursor.executemany('INSERT INTO events (event_name, date, venue, description, image_url, event_type) VALUES (?, ?, ?, ?, ?, ?)', default_events)
        conn.commit()
        print("Default events added.")

    conn.commit()
    conn.close()

# Ensure DB exists
if not os.path.exists(DB_NAME):
    init_db()
else:
    init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/events')
def events():
    return redirect(url_for('index', _anchor='events'))

@app.route('/about')
def about():
    return redirect(url_for('index', _anchor='about'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Simulate sending email
        name = request.form['name']
        flash(f'Thanks for contacting us, {name}! We will get back to you shortly.', 'success')
        return redirect(url_for('index', _anchor='contact'))
    return redirect(url_for('index', _anchor='contact'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        rating = request.form.get('rating')
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO feedback (name, message, rating) VALUES (?, ?, ?)', (name, message, rating))
        conn.commit()
        conn.close()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('index', _anchor='feedback'))
    return redirect(url_for('index', _anchor='feedback'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        selected_event = request.args.get('event')
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT event_name FROM events')
        events = [row[0] for row in cursor.fetchall()]
        conn.close()
        return render_template('register.html', events=events, selected_event=selected_event)
    
    if request.method == 'POST':
        try:
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form['phone']
            college = request.form['college']
            event = request.form['event']

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO participants (full_name, email, phone, college, event)
                VALUES (?, ?, ?, ?, ?)
            ''', (full_name, email, phone, college, event))
            conn.commit()
            conn.close()

            flash('Registration successful! See you at the event.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('register'))

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM participants ORDER BY reg_date DESC')
    participants = cursor.fetchall()
    
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()

    cursor.execute('SELECT * FROM feedback ORDER BY id DESC')
    feedback = cursor.fetchall()
    
    conn.close()
    return render_template('admin.html', participants=participants, events=events, feedback=feedback)

@app.route('/admin/delete_participant/<int:id>', methods=['POST'])
def delete_participant(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM participants WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Participant deleted.', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/add_event', methods=['POST'])
def add_event():
    name = request.form['event_name']
    date = request.form['date']
    venue = request.form['venue']
    desc = request.form['description']
    event_type = request.form.get('event_type', 'Technical')
    image_url = 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&q=80&w=1000' 
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (event_name, date, venue, description, image_url, event_type) VALUES (?, ?, ?, ?, ?, ?)',
                   (name, date, venue, desc, image_url, event_type))
    conn.commit()
    conn.close()
    flash('Event added successfully.', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/delete_event/<int:id>', methods=['POST'])
def delete_event(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE event_id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Event deleted.', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)
