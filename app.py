from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, Response
import os
import sys
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime
import base64
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Automatic startup initialization
try:
    from src.utils.startup import initialize_app
    logger.info("Running startup initialization...")
    if not initialize_app(silent=False):
        logger.error("Startup initialization failed! Please fix errors before continuing.")
        sys.exit(1)
except Exception as e:
    logger.warning(f"Could not run startup initialization: {e}")
    logger.info("Continuing with manual initialization...")

from database import init_db
from models import Student, Course, Attendance, Admin, Settings
from face_recognition_module import FaceRecognitionSystem, process_student_images
from export_utils import export_attendance_to_excel, export_student_attendance_summary

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['UPLOAD_FOLDER'] = 'student_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database (backup if startup didn't run)
try:
    init_db()
except:
    pass

# Global face recognition system
fr_system = FaceRecognitionSystem()

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============= PUBLIC ROUTES =============

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/mark-attendance')
def mark_attendance_page():
    """Attendance marking page for students"""
    courses = Course.get_all_courses()
    return render_template('mark_attendance.html', courses=courses)

@app.route('/video-feed')
def video_feed():
    """Video streaming route for face detection with liveness detection"""
    def generate():
        camera = cv2.VideoCapture(0)
        
        # Reset liveness detector for new session
        if fr_system.enable_liveness and fr_system.liveness_detector:
            fr_system.liveness_detector.reset_blink_counter()
        
        while True:
            success, frame = camera.read()
            if not success:
                break
            
            # Detect and recognize face with liveness check
            student_id, confidence, face_location, is_live = fr_system.recognize_face_from_frame(frame, check_liveness=True)
            
            # Get blink count if liveness detection is enabled
            blink_count = 0
            if fr_system.enable_liveness and fr_system.liveness_detector:
                blink_count = fr_system.liveness_detector.total_blinks
            
            if student_id and confidence > 0.5:
                # Determine if liveness is verified (at least 1 blink detected)
                is_verified = blink_count >= 1 if fr_system.enable_liveness else True
                # Draw face box with liveness status
                frame = fr_system.draw_face_box(frame, face_location, student_id, confidence, is_verified)
            
            # Add liveness instructions overlay
            if fr_system.enable_liveness:
                cv2.putText(frame, "Please blink naturally", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, f"Blinks detected: {blink_count}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        camera.release()
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get-blink-count')
def get_blink_count():
    """Get current blink count from liveness detector"""
    blink_count = 0
    if fr_system.enable_liveness and fr_system.liveness_detector:
        blink_count = fr_system.liveness_detector.total_blinks
    return jsonify({'blink_count': blink_count})

@app.route('/capture-attendance', methods=['POST'])
def capture_attendance():
    """Capture and mark attendance from webcam with liveness verification"""
    data = request.get_json()
    course_code = data.get('course_code')
    action = data.get('action', 'check_in')  # 'check_in' or 'check_out'
    blink_count = data.get('blink_count', 0)  # Blinks detected from video feed
    
    if not course_code:
        return jsonify({'success': False, 'message': 'Course code required'})
    
    # Check liveness requirement
    if fr_system.enable_liveness and blink_count < 1:
        return jsonify({
            'success': False, 
            'message': 'Liveness check failed. Please blink naturally and try again.',
            'liveness_required': True
        })
    
    # Capture frame from webcam
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    camera.release()
    
    if not success:
        return jsonify({'success': False, 'message': 'Failed to capture image'})
    
    # Recognize face (skip liveness check here as it's already done)
    student_id, confidence, face_location, _ = fr_system.recognize_face_from_frame(frame, check_liveness=False)
    
    if not student_id or confidence < 0.5:
        return jsonify({'success': False, 'message': 'Face not recognized. Please try again.'})
    
    # Get student details
    student = Student.get_student_by_id(student_id)
    
    if action == 'check_in':
        # Check in
        success = Attendance.check_in(student_id, course_code)
        
        if success:
            return jsonify({
                'success': True, 
                'message': f'Checked in successfully!',
                'student_name': student['name'],
                'student_id': student_id,
                'confidence': f'{confidence:.2%}',
                'action': 'check_in'
            })
        else:
            # Check if already checked in
            status = Attendance.get_today_status(student_id, course_code)
            if status:
                if status['check_out_time']:
                    return jsonify({
                        'success': False, 
                        'message': 'Already checked out for today',
                        'student_name': student['name'],
                        'student_id': student_id,
                        'status': status['status']
                    })
                else:
                    return jsonify({
                        'success': False, 
                        'message': 'Already checked in. Please check out.',
                        'student_name': student['name'],
                        'student_id': student_id,
                        'can_checkout': True
                    })
            return jsonify({
                'success': False, 
                'message': 'Failed to check in',
                'student_name': student['name'],
                'student_id': student_id
            })
    
    elif action == 'check_out':
        # Check out
        success, status = Attendance.check_out(student_id, course_code)
        
        if success:
            return jsonify({
                'success': True, 
                'message': f'Checked out successfully! Status: {status}',
                'student_name': student['name'],
                'student_id': student_id,
                'confidence': f'{confidence:.2%}',
                'status': status,
                'action': 'check_out'
            })
        else:
            return jsonify({
                'success': False, 
                'message': status,  # Error message from check_out
                'student_name': student['name'],
                'student_id': student_id
            })

# ============= ADMIN ROUTES =============

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if Admin.verify_admin(username, password):
            session['admin_logged_in'] = True
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/admin/logout')
def logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    total_students = len(Student.get_all_students())
    total_courses = len(Course.get_all_courses())
    total_attendance = len(Attendance.get_all_attendance())
    
    # Get recent attendance
    recent_attendance = Attendance.get_all_attendance()[:10]
    
    return render_template('admin_dashboard.html', 
                         total_students=total_students,
                         total_courses=total_courses,
                         total_attendance=total_attendance,
                         recent_attendance=recent_attendance)

# ============= STUDENT MANAGEMENT =============

@app.route('/admin/students')
@login_required
def manage_students():
    """Manage students page"""
    students = Student.get_all_students()
    return render_template('manage_students.html', students=students)

@app.route('/admin/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add new student"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Handle file upload
        if 'image' not in request.files:
            return render_template('add_student.html', error='No image uploaded')
        
        file = request.files['image']
        
        if file.filename == '':
            return render_template('add_student.html', error='No image selected')
        
        if file:
            # Save file
            filename = secure_filename(f"{student_id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process and train face
            success = process_student_images(student_id, name, email, phone, filepath)
            
            if success:
                # Reload face recognition system
                fr_system.load_known_faces()
                return redirect(url_for('manage_students'))
            else:
                return render_template('add_student.html', 
                                     error='Failed to process image. Make sure face is clearly visible.')
    
    return render_template('add_student.html')

@app.route('/admin/students/delete/<student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    """Delete student"""
    Student.delete_student(student_id)
    fr_system.load_known_faces()
    return redirect(url_for('manage_students'))

# ============= COURSE MANAGEMENT =============

@app.route('/admin/courses')
@login_required
def manage_courses():
    """Manage courses page"""
    courses = Course.get_all_courses()
    return render_template('manage_courses.html', courses=courses)

@app.route('/admin/courses/add', methods=['GET', 'POST'])
@login_required
def add_course():
    """Add new course"""
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        instructor = request.form.get('instructor')
        schedule = request.form.get('schedule')
        total_classes = request.form.get('total_classes', type=int, default=30)
        class_duration = request.form.get('class_duration_minutes', type=int, default=60)
        min_duration = request.form.get('min_duration_minutes', type=int, default=45)
        
        success = Course.add_course(course_code, course_name, instructor, schedule, 
                                    total_classes, class_duration, min_duration)
        
        if success:
            return redirect(url_for('manage_courses'))
        else:
            return render_template('add_course.html', 
                                 error='Course code already exists')
    
    return render_template('add_course.html')

@app.route('/admin/courses/delete/<course_code>', methods=['POST'])
@login_required
def delete_course(course_code):
    """Delete course"""
    Course.delete_course(course_code)
    return redirect(url_for('manage_courses'))

# ============= ATTENDANCE MANAGEMENT =============

@app.route('/admin/attendance')
@login_required
def view_attendance():
    """View all attendance records"""
    attendance_records = Attendance.get_all_attendance()
    return render_template('view_attendance.html', records=attendance_records)

@app.route('/admin/attendance/student/<student_id>')
@login_required
def view_student_attendance(student_id):
    """View attendance for a specific student"""
    student = Student.get_student_by_id(student_id)
    attendance_records = Attendance.get_attendance_by_student(student_id)
    courses = Course.get_all_courses()
    
    # Calculate percentages
    percentages = {}
    for course in courses:
        percentages[course['course_code']] = Attendance.get_student_attendance_percentage(
            student_id, course['course_code']
        )
    
    threshold = Settings.get_min_attendance_percentage()
    
    return render_template('student_attendance.html', 
                         student=student,
                         records=attendance_records,
                         percentages=percentages,
                         threshold=threshold)

@app.route('/admin/attendance/course/<course_code>')
@login_required
def view_course_attendance(course_code):
    """View attendance for a specific course"""
    course = Course.get_course_by_code(course_code)
    attendance_records = Attendance.get_attendance_by_course(course_code)
    return render_template('course_attendance.html', 
                         course=course,
                         records=attendance_records)

# ============= EXPORT ROUTES =============

@app.route('/admin/export/attendance')
@login_required
def export_attendance():
    """Export all attendance to Excel"""
    filename = export_attendance_to_excel()
    if filename:
        return send_file(filename, as_attachment=True)
    else:
        return "No data to export", 404

@app.route('/admin/export/attendance/<course_code>')
@login_required
def export_course_attendance(course_code):
    """Export course attendance to Excel"""
    filename = export_attendance_to_excel(course_code)
    if filename:
        return send_file(filename, as_attachment=True)
    else:
        return "No data to export", 404

@app.route('/admin/export/summary')
@login_required
def export_summary():
    """Export attendance summary to Excel"""
    filename = export_student_attendance_summary()
    if filename:
        return send_file(filename, as_attachment=True)
    else:
        return "No data to export", 404

# ============= SETTINGS =============

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Admin settings"""
    if request.method == 'POST':
        min_percentage = int(request.form.get('min_attendance_percentage'))
        Settings.set_min_attendance_percentage(min_percentage)
        return redirect(url_for('settings'))
    
    current_threshold = Settings.get_min_attendance_percentage()
    return render_template('settings.html', threshold=current_threshold)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('student_images', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=8181)
