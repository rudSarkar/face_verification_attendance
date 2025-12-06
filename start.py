#!/usr/bin/env python3
"""
Cross-platform startup script for Face Recognition Attendance System
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print welcome header"""
    print("=" * 60)
    print("Face Recognition Attendance System")
    print("=" * 60)
    print()

def get_python_command():
    """Get the appropriate Python command for the current OS"""
    if platform.system() == "Windows":
        return "python"
    else:
        return "python3"

def get_venv_activate_command():
    """Get the virtual environment activation command for the current OS"""
    if platform.system() == "Windows":
        if os.path.exists("venv\\Scripts\\activate.bat"):
            return "venv\\Scripts\\activate.bat"
        elif os.path.exists("venv\\Scripts\\Activate.ps1"):
            return "venv\\Scripts\\Activate.ps1"
    else:
        return "venv/bin/activate"
    return None

def get_venv_python():
    """Get the path to the Python executable in the virtual environment"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

def check_python():
    """Check if Python is installed"""
    python_cmd = get_python_command()
    try:
        result = subprocess.run(
            [python_cmd, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print(f"✓ Python found: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Python is not installed or not in PATH.")
        print("   Please install Python 3.8 or higher from https://www.python.org/")
        return False

def create_venv():
    """Create virtual environment if it doesn't exist"""
    if not os.path.exists("venv"):
        print("📦 Creating virtual environment...")
        python_cmd = get_python_command()
        try:
            subprocess.run([python_cmd, "-m", "venv", "venv"], check=True)
            print("✓ Virtual environment created")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    else:
        print("✓ Virtual environment already exists")
        return True

def install_dependencies():
    """Install dependencies if not already installed"""
    marker_file = os.path.join("venv", ".requirements_installed")
    
    if not os.path.exists(marker_file):
        print("📥 Installing dependencies...")
        venv_python = get_venv_python()
        
        if not os.path.exists(venv_python):
            print(f"❌ Virtual environment Python not found at {venv_python}")
            return False
        
        try:
            subprocess.run(
                [venv_python, "-m", "pip", "install", "--upgrade", "pip"],
                check=True
            )
            subprocess.run(
                [venv_python, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True
            )
            # Create marker file
            with open(marker_file, "w") as f:
                f.write("installed")
            print("✓ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("\nTrying to continue anyway...")
            return True
    else:
        print("✓ Dependencies already installed")
        return True

def init_database():
    """Initialize database if it doesn't exist"""
    if not os.path.exists("attendance_system.db"):
        print("🗄️  Initializing database...")
        venv_python = get_venv_python()
        try:
            subprocess.run([venv_python, "database.py"], check=True)
            print("✓ Database initialized")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize database: {e}")
            return False
    else:
        print("✓ Database already exists")
    return True

def start_application():
    """Start the Flask application"""
    print()
    print("=" * 60)
    print("🚀 Starting Flask Application...")
    print("=" * 60)
    print()
    print("Access the application at:")
    print("  🏠 Home: http://localhost:8181")
    print("  👤 Admin: http://localhost:8181/admin/login")
    print("  📸 Mark Attendance: http://localhost:8181/mark-attendance")
    print()
    print("Default Admin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    venv_python = get_venv_python()
    
    try:
        subprocess.run([venv_python, "app.py"])
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running application: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print_header()
    
    # Step 1: Check Python
    if not check_python():
        sys.exit(1)
    
    print()
    
    # Step 2: Create virtual environment
    if not create_venv():
        sys.exit(1)
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print("\n⚠️  Warning: Some dependencies may not be installed correctly.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print()
    
    # Step 4: Initialize database
    if not init_database():
        sys.exit(1)
    
    # Step 5: Start application
    start_application()

if __name__ == "__main__":
    main()
