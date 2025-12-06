import sqlite3
from database import get_db_connection
import pickle
from datetime import datetime, date

class Student:
    @staticmethod
    def add_student(student_id, name, email, phone, image_path, face_encoding):
        """Add a new student to the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Serialize face encoding
        encoding_blob = pickle.dumps(face_encoding) if face_encoding is not None else None
        
        try:
            cursor.execute('''
                INSERT INTO students (student_id, name, email, phone, image_path, face_encoding)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, name, email, phone, image_path, encoding_blob))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    @staticmethod
    def get_all_students():
        """Get all students"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY name')
        students = cursor.fetchall()
        conn.close()
        return students
    
    @staticmethod
    def get_student_by_id(student_id):
        """Get student by student_id"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student
    
    @staticmethod
    def update_student(student_id, name, email, phone):
        """Update student information"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students 
            SET name = ?, email = ?, phone = ?
            WHERE student_id = ?
        ''', (name, email, phone, student_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_student(student_id):
        """Delete a student"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_face_encodings():
        """Get all face encodings with student IDs"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT student_id, face_encoding FROM students WHERE face_encoding IS NOT NULL')
        rows = cursor.fetchall()
        conn.close()
        
        encodings = []
        student_ids = []
        for row in rows:
            student_ids.append(row['student_id'])
            encodings.append(pickle.loads(row['face_encoding']))
        
        return student_ids, encodings

class Course:
    @staticmethod
    def add_course(course_code, course_name, instructor, schedule, total_classes=30, class_duration_minutes=60, min_duration_minutes=45):
        """Add a new course"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO courses (course_code, course_name, instructor, schedule, total_classes, class_duration_minutes, min_duration_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (course_code, course_name, instructor, schedule, total_classes, class_duration_minutes, min_duration_minutes))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    @staticmethod
    def get_all_courses():
        """Get all courses"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses ORDER BY course_code')
        courses = cursor.fetchall()
        conn.close()
        return courses
    
    @staticmethod
    def get_course_by_code(course_code):
        """Get course by course code"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses WHERE course_code = ?', (course_code,))
        course = cursor.fetchone()
        conn.close()
        return course
    
    @staticmethod
    def update_course(course_code, course_name, instructor, schedule, total_classes=30, class_duration_minutes=60, min_duration_minutes=45):
        """Update course information"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE courses 
            SET course_name = ?, instructor = ?, schedule = ?, total_classes = ?, class_duration_minutes = ?, min_duration_minutes = ?
            WHERE course_code = ?
        ''', (course_name, instructor, schedule, total_classes, class_duration_minutes, min_duration_minutes, course_code))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_course(course_code):
        """Delete a course"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM courses WHERE course_code = ?', (course_code,))
        conn.commit()
        conn.close()

class Attendance:
    @staticmethod
    def check_in(student_id, course_code):
        """Check in a student for attendance"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        today = date.today().isoformat()
        current_time = datetime.now().strftime('%H:%M:%S')
        
        try:
            cursor.execute('''
                INSERT INTO attendance (student_id, course_code, date, check_in_time, status)
                VALUES (?, ?, ?, ?, 'Checked In')
            ''', (student_id, course_code, today, current_time))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Already checked in for today
            conn.close()
            return False
    
    @staticmethod
    def check_out(student_id, course_code):
        """Check out a student and calculate attendance status"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        today = date.today().isoformat()
        current_time = datetime.now()
        
        # Get attendance record for today
        cursor.execute('''
            SELECT * FROM attendance
            WHERE student_id = ? AND course_code = ? AND date = ?
        ''', (student_id, course_code, today))
        record = cursor.fetchone()
        
        if not record:
            conn.close()
            return False, "No check-in record found for today"
        
        if record['check_out_time']:
            conn.close()
            return False, "Already checked out"
        
        # Get course minimum duration
        cursor.execute('SELECT min_duration_minutes FROM courses WHERE course_code = ?', (course_code,))
        course = cursor.fetchone()
        min_duration = course['min_duration_minutes'] if course else 45
        
        # Calculate duration
        check_in_time = datetime.strptime(record['check_in_time'], '%H:%M:%S')
        current_date = date.today()
        check_in_datetime = datetime.combine(current_date, check_in_time.time())
        duration_minutes = int((current_time - check_in_datetime).total_seconds() / 60)
        
        # Determine status
        if duration_minutes >= min_duration:
            status = 'Present'
        else:
            status = 'Absent (Left Early)'
        
        # Update record
        cursor.execute('''
            UPDATE attendance
            SET check_out_time = ?, duration_minutes = ?, status = ?
            WHERE student_id = ? AND course_code = ? AND date = ?
        ''', (current_time.strftime('%H:%M:%S'), duration_minutes, status, student_id, course_code, today))
        
        conn.commit()
        conn.close()
        return True, status
    
    @staticmethod
    def get_today_status(student_id, course_code):
        """Get today's attendance status for a student"""
        conn = get_db_connection()
        cursor = conn.cursor()
        today = date.today().isoformat()
        
        cursor.execute('''
            SELECT * FROM attendance
            WHERE student_id = ? AND course_code = ? AND date = ?
        ''', (student_id, course_code, today))
        record = cursor.fetchone()
        conn.close()
        return record
    
    @staticmethod
    def mark_attendance(student_id, course_code, status='Present'):
        """Legacy method - now redirects to check_in"""
        return Attendance.check_in(student_id, course_code)
    
    @staticmethod
    def get_attendance_by_course(course_code):
        """Get all attendance records for a course"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, s.name 
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            WHERE a.course_code = ?
            ORDER BY a.date DESC, a.check_in_time DESC
        ''', (course_code,))
        records = cursor.fetchall()
        conn.close()
        return records
    
    @staticmethod
    def get_attendance_by_student(student_id):
        """Get all attendance records for a student"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, c.course_name 
            FROM attendance a
            JOIN courses c ON a.course_code = c.course_code
            WHERE a.student_id = ?
            ORDER BY a.date DESC, a.check_in_time DESC
        ''', (student_id,))
        records = cursor.fetchall()
        conn.close()
        return records
    
    @staticmethod
    def get_student_attendance_percentage(student_id, course_code):
        """Calculate attendance percentage for a student in a course"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total classes from course
        cursor.execute('''
            SELECT total_classes
            FROM courses
            WHERE course_code = ?
        ''', (course_code,))
        course = cursor.fetchone()
        total = course['total_classes'] if course else 0
        
        # Get attended classes
        cursor.execute('''
            SELECT COUNT(*) as attended
            FROM attendance
            WHERE student_id = ? AND course_code = ? AND status = 'Present'
        ''', (student_id, course_code))
        attended = cursor.fetchone()['attended']
        
        conn.close()
        
        if total == 0:
            return 0
        
        return round((attended / total) * 100, 2)
    
    @staticmethod
    def get_all_attendance():
        """Get all attendance records"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, s.name, c.course_name 
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN courses c ON a.course_code = c.course_code
            ORDER BY a.date DESC, a.check_in_time DESC
        ''')
        records = cursor.fetchall()
        conn.close()
        return records

class Settings:
    @staticmethod
    def get_min_attendance_percentage():
        """Get minimum attendance percentage threshold"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', ('min_attendance_percentage',))
        result = cursor.fetchone()
        conn.close()
        return int(result['value']) if result else 75
    
    @staticmethod
    def set_min_attendance_percentage(percentage):
        """Set minimum attendance percentage threshold"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE settings 
            SET value = ?
            WHERE key = ?
        ''', (str(percentage), 'min_attendance_percentage'))
        conn.commit()
        conn.close()

class Admin:
    @staticmethod
    def verify_admin(username, password):
        """Verify admin credentials"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ?', 
                      (username, password))
        admin = cursor.fetchone()
        conn.close()
        return admin is not None
