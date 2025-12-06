#!/bin/bash

# Face Recognition Attendance System - Startup Script

echo "=========================================="
echo "Face Recognition Attendance System"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.requirements_installed
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

echo ""

# Check if database exists
if [ ! -f "attendance_system.db" ]; then
    echo "🗄️  Initializing database..."
    python3 database.py
    echo "✓ Database initialized"
else
    echo "✓ Database already exists"
fi

echo ""
echo "=========================================="
echo "🚀 Starting Flask Application..."
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  🏠 Home: http://localhost:8181"
echo "  👤 Admin: http://localhost:8181/admin/login"
echo "  📸 Mark Attendance: http://localhost:8181/mark-attendance"
echo ""
echo "Default Admin Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start Flask application
python3 app.py
