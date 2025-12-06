import sqlite3
from datetime import datetime
import os

DATABASE_PATH = 'attendance_system.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            image_path TEXT,
            face_encoding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            instructor TEXT,
            schedule TEXT,
            total_classes INTEGER NOT NULL DEFAULT 30,
            class_duration_minutes INTEGER NOT NULL DEFAULT 60,
            min_duration_minutes INTEGER NOT NULL DEFAULT 45,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_code TEXT NOT NULL,
            date DATE NOT NULL,
            check_in_time TIME NOT NULL,
            check_out_time TIME,
            duration_minutes INTEGER,
            status TEXT DEFAULT 'Checked In',
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_code) REFERENCES courses(course_code),
            UNIQUE(student_id, course_code, date)
        )
    ''')
    
    # Create Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Settings table for attendance threshold
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    
    # Insert default attendance threshold if not exists
    cursor.execute('''
        INSERT OR IGNORE INTO settings (key, value) 
        VALUES ('min_attendance_percentage', '75')
    ''')
    
    # Insert default minimum class duration setting
    cursor.execute('''
        INSERT OR IGNORE INTO settings (key, value) 
        VALUES ('default_min_duration_minutes', '45')
    ''')
    
    # Insert default admin (username: admin, password: admin123)
    cursor.execute('''
        INSERT OR IGNORE INTO admins (username, password, email) 
        VALUES ('admin', 'admin123', 'admin@example.com')
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
