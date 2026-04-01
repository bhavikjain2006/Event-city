# Event Registration System

A beginner-friendly Event Registration System built with **Flask (Python)**, **SQLite**, **HTML**, **CSS**, and **JavaScript**. This project is designed for college submissions and learning purposes.

## Features
- **User Registration**: Clean and responsive form with validation.
- **Data Storage**: Submissions are saved to a local SQLite database.
- **Admin Dashboard**: View all registered participants and delete entries.
- **Validation**: Client-side validation for emails and phone numbers.

## Tech Stack
- **Backend**: Python (Flask)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## Project Structure
```text
event_registration/
│
├── app.py                # Main Flask application
├── database.db           # SQLite database (auto-created)
├── templates/
│   ├── index.html        # Registration form
│   └── admin.html        # Admin dashboard
└── static/
    ├── style.css         # Styling
    └── script.js         # Validation script
```

## How to Run Locally

### 1. Prerequisites
- Install [Python](https://www.python.org/downloads/) (3.x recommended).

### 2. Setup
1.  Navigate to the project directory:
    ```bash
    cd "C:\Users\bhaviksuhaani\.gemini\antigravity\scratch\event_registration"
    ```

2.  Install Flask (if not installed):
    ```bash
    pip install Flask
    ```

### 3. Run the Application
1.  Start the Flask server:
    ```bash
    python app.py
    ```
2.  You should see output indicating the server is running (usually at `http://127.0.0.1:5000`).

### 4. Access the App
- **Registration Form**: Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
- **Admin Dashboard**: Go to [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin).

## Database Info
The `database.db` file will be automatically created when you run the app for the first time.
The table structure is:
```sql
CREATE TABLE participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    college TEXT NOT NULL,
    event TEXT NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
