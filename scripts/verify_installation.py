#!/usr/bin/env python3
"""
Installation Verification Script
Checks if all components are properly installed and configured
"""

import sys
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    packages = {
        'flask': 'Flask',
        'cv2': 'OpenCV (opencv-python)',
        'face_recognition': 'face_recognition',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'openpyxl': 'openpyxl',
        'PIL': 'Pillow',
    }
    
    all_installed = True
    
    for package, name in packages.items():
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                from PIL import Image
            else:
                __import__(package)
            print(f"✅ {name} - Installed")
        except ImportError:
            print(f"❌ {name} - Missing")
            all_installed = False
    
    return all_installed

def check_files():
    """Check if all required files exist"""
    print("\n🔍 Checking project files...")
    
    required_files = [
        'app.py',
        'database.py',
        'models.py',
        'face_recognition_module.py',
        'export_utils.py',
        'requirements.txt',
        'README.md',
    ]
    
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_exist = False
    
    return all_exist

def check_directories():
    """Check if all required directories exist"""
    print("\n🔍 Checking directories...")
    
    required_dirs = [
        'templates',
        'static',
        'student_images',
        'exports',
    ]
    
    all_exist = True
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ - Found")
        else:
            print(f"❌ {directory}/ - Missing")
            all_exist = False
    
    return all_exist

def check_templates():
    """Check if all template files exist"""
    print("\n🔍 Checking HTML templates...")
    
    required_templates = [
        'base.html',
        'index.html',
        'login.html',
        'mark_attendance.html',
        'admin_dashboard.html',
        'manage_students.html',
        'add_student.html',
        'manage_courses.html',
        'add_course.html',
        'view_attendance.html',
        'student_attendance.html',
        'course_attendance.html',
        'settings.html',
    ]
    
    all_exist = True
    
    for template in required_templates:
        filepath = os.path.join('templates', template)
        if os.path.exists(filepath):
            print(f"✅ {template} - Found")
        else:
            print(f"❌ {template} - Missing")
            all_exist = False
    
    return all_exist

def check_database():
    """Check if database can be initialized"""
    print("\n🔍 Checking database...")
    
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        required_tables = ['students', 'courses', 'attendance', 'admins', 'settings']
        
        if tables:
            print(f"✅ Database initialized with {len(tables)} tables")
            
            table_names = [t[0] for t in tables]
            for table in required_tables:
                if table in table_names:
                    print(f"  ✓ Table '{table}' exists")
                else:
                    print(f"  ✗ Table '{table}' missing")
        else:
            print("⚠️  Database exists but no tables found")
            print("   Run: python database.py")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database check failed: {str(e)}")
        print("   Run: python database.py")
        return False

def test_imports():
    """Test if modules can be imported"""
    print("\n🔍 Testing module imports...")
    
    modules = [
        'database',
        'models',
        'face_recognition_module',
        'export_utils',
    ]
    
    all_imported = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}.py - Importable")
        except Exception as e:
            print(f"❌ {module}.py - Import error: {str(e)}")
            all_imported = False
    
    return all_imported

def check_camera():
    """Check if camera is accessible"""
    print("\n🔍 Checking camera access...")
    
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        
        if camera.isOpened():
            print("✅ Camera - Accessible")
            camera.release()
            return True
        else:
            print("⚠️  Camera - Not accessible (may need permissions)")
            return False
    except Exception as e:
        print(f"❌ Camera check failed: {str(e)}")
        return False

def run_verification():
    """Run all verification checks"""
    print_header("Face Recognition Attendance System")
    print_header("Installation Verification")
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Project Files", check_files()))
    results.append(("Directories", check_directories()))
    results.append(("Templates", check_templates()))
    results.append(("Database", check_database()))
    results.append(("Module Imports", test_imports()))
    results.append(("Camera Access", check_camera()))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check}")
    
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{total} checks passed")
    print(f"{'=' * 60}\n")
    
    if passed == total:
        print("🎉 All checks passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run setup: python setup.py")
        print("2. Start app: python app.py")
        print("3. Visit: http://localhost:8181")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Initialize database: python database.py")
        print("3. Check file permissions")
    
    print()

if __name__ == '__main__':
    run_verification()
