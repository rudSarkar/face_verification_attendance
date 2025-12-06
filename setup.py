#!/usr/bin/env python3
"""
Quick Start Script for Face Recognition Attendance System
This script helps you set up the system with sample data
"""

import os
import sys
from database import init_db
from models import Course, Student, Settings

def setup_system():
    """Initialize the system with sample data"""
    
    print("=" * 60)
    print("Face Recognition Attendance System - Quick Setup")
    print("=" * 60)
    print()
    
    # Step 1: Initialize Database
    print("📦 Step 1: Initializing database...")
    init_db()
    print("✅ Database initialized!\n")
    
    # Step 2: Add Sample Courses
    print("📚 Step 2: Adding sample courses...")
    sample_courses = [
        ('CS101', 'Introduction to Computer Science', 'Dr. Alice Johnson', 'Mon/Wed 10:00-11:30'),
        ('MATH201', 'Advanced Mathematics', 'Prof. Bob Smith', 'Tue/Thu 14:00-15:30'),
        ('PHY101', 'Physics Fundamentals', 'Dr. Carol White', 'Mon/Wed/Fri 9:00-10:00'),
        ('ENG101', 'English Literature', 'Prof. David Brown', 'Tue/Thu 10:00-11:30'),
        ('CHEM101', 'General Chemistry', 'Dr. Emily Davis', 'Mon/Wed 14:00-16:00'),
    ]
    
    courses_added = 0
    for course_code, course_name, instructor, schedule in sample_courses:
        if Course.add_course(course_code, course_name, instructor, schedule):
            print(f"  ✓ Added: {course_code} - {course_name}")
            courses_added += 1
        else:
            print(f"  ⚠ Skipped: {course_code} (already exists)")
    
    print(f"✅ {courses_added} courses added!\n")
    
    # Step 3: Set Attendance Threshold
    print("⚙️  Step 3: Configuring settings...")
    current_threshold = Settings.get_min_attendance_percentage()
    print(f"  Minimum attendance threshold: {current_threshold}%")
    print("✅ Settings configured!\n")
    
    # Step 4: Instructions for Adding Students
    print("👥 Step 4: Adding Students")
    print("-" * 60)
    print("To add students, you need to:")
    print("  1. Place student photos in the 'student_images/' folder")
    print("  2. Use the admin panel at http://localhost:8181/admin/login")
    print("  3. Or run the Jupyter notebook: face_recognition_attendance.ipynb")
    print()
    print("Admin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print()
    
    # Step 5: Next Steps
    print("=" * 60)
    print("🚀 Setup Complete! Next Steps:")
    print("=" * 60)
    print()
    print("1. Start the Flask application:")
    print("   python app.py")
    print()
    print("2. Access the application:")
    print("   - Home: http://localhost:8181")
    print("   - Admin: http://localhost:8181/admin/login")
    print("   - Mark Attendance: http://localhost:8181/mark-attendance")
    print()
    print("3. Add students using the admin panel")
    print()
    print("4. Start marking attendance!")
    print()
    print("For detailed instructions, see README.md")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'cv2',
        'face_recognition',
        'numpy',
        'pandas',
        'openpyxl',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                __import__('cv2')
            elif package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print()
        print("⚠️  Missing packages detected!")
        print("Please install them using:")
        print("  pip install -r requirements.txt")
        print()
        return False
    
    print("✅ All dependencies installed!\n")
    return True

if __name__ == '__main__':
    print()
    
    # Check dependencies first
    if check_dependencies():
        # Setup the system
        setup_system()
    else:
        print("Please install missing dependencies before proceeding.")
        sys.exit(1)
