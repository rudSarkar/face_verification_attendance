"""
Database Migration Script for Check-in/Check-out System
This script migrates the database from the old single-time attendance system
to the new check-in/check-out system with duration tracking.
"""

import sqlite3
from database import DATABASE_PATH, get_db_connection

def migrate_database():
    """Migrate database to new schema"""
    print("Starting database migration...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if migration is needed
        cursor.execute("PRAGMA table_info(attendance)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'check_in_time' in columns:
            print("Database already migrated!")
            conn.close()
            return
        
        print("Migrating attendance table...")
        
        # Step 1: Rename old table
        cursor.execute('ALTER TABLE attendance RENAME TO attendance_old')
        
        # Step 2: Create new attendance table
        cursor.execute('''
            CREATE TABLE attendance (
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
        
        # Step 3: Migrate old data
        cursor.execute('''
            INSERT INTO attendance (id, student_id, course_code, date, check_in_time, status, marked_at)
            SELECT id, student_id, course_code, date, time, 
                   CASE WHEN status = 'Present' THEN 'Present' ELSE status END,
                   marked_at
            FROM attendance_old
        ''')
        
        # Step 4: Drop old table
        cursor.execute('DROP TABLE attendance_old')
        
        print("Attendance table migrated successfully!")
        
        # Migrate courses table
        cursor.execute("PRAGMA table_info(courses)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'class_duration_minutes' not in columns:
            print("Migrating courses table...")
            
            # Add new columns to courses
            cursor.execute('ALTER TABLE courses ADD COLUMN class_duration_minutes INTEGER NOT NULL DEFAULT 60')
            cursor.execute('ALTER TABLE courses ADD COLUMN min_duration_minutes INTEGER NOT NULL DEFAULT 45')
            
            print("Courses table migrated successfully!")
        
        # Add default minimum duration setting
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value) 
            VALUES ('default_min_duration_minutes', '45')
        ''')
        
        conn.commit()
        print("\nDatabase migration completed successfully!")
        print("\nNew features:")
        print("  - Students must check in at class start")
        print("  - Students must check out when leaving")
        print("  - Minimum duration required for 'Present' status")
        print("  - Early departure tracked as 'Absent (Left Early)'")
        
    except Exception as e:
        conn.rollback()
        print(f"\nMigration failed: {str(e)}")
        raise
    
    finally:
        conn.close()

def check_migration_status():
    """Check if migration is needed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(attendance)")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    
    if 'check_in_time' in columns:
        return "already_migrated"
    else:
        return "needs_migration"

if __name__ == '__main__':
    status = check_migration_status()
    
    if status == "already_migrated":
        print("Database is already up to date!")
    else:
        print("Database migration required...")
        response = input("Do you want to proceed with migration? (yes/no): ")
        
        if response.lower() in ['yes', 'y']:
            migrate_database()
        else:
            print("Migration cancelled.")
