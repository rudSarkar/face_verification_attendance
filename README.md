# Face Recognition Attendance System 🎓

A comprehensive AI-powered attendance management system using face recognition technology with **check-in/check-out functionality** to prevent class bunking. Built with Flask, OpenCV, and SQLite.

## ✨ Cross-Platform Support

**Works on Windows, macOS, and Linux!**

- 🐳 **Docker support** for easiest setup (recommended)
- 🐍 **Python cross-platform script** (`start.py`)
- 💻 **Platform-specific scripts** (`.bat` for Windows, `.sh` for Unix)
- 📦 **All dependencies work across platforms**

> **🚀 New to this project? Check [QUICKSTART.md](QUICKSTART.md) for the fastest way to get started!**

## 🆕 NEW: Check-In/Check-Out System

**Prevents students from leaving early!**

- ✅ Students must **check in** at class start
- ✅ Students must **check out** before leaving
- ✅ System tracks actual **duration** in class
- ✅ Minimum duration required for "Present" status
- ✅ Early departure flagged as "Absent (Left Early)"

📚 **[Read the Full Guide](CHECKIN_CHECKOUT_GUIDE.md)** | 📖 **[Quick Start](QUICK_START.md)**

## Features ✨

- **Face Recognition**: Automatic student identification using advanced AI
- **Check-In/Check-Out**: Track entry and exit times with duration monitoring
- **Duration Enforcement**: Configurable minimum class duration per course
- **Web Interface**: User-friendly web application for marking attendance
- **Admin Panel**: Complete dashboard for managing students, courses, and attendance
- **Real-time Camera**: Live webcam feed for face detection
- **Excel Export**: Export attendance reports with timing details
- **Attendance Tracking**: Calculate and monitor attendance percentages
- **SQLite Database**: Lightweight and efficient data storage
- **Jupyter Notebook**: Interactive exploration and testing

## Tech Stack 🛠️

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Face Recognition**: OpenCV, face_recognition library
- **Data Processing**: Pandas, NumPy
- **Export**: openpyxl (Excel export)
- **Frontend**: HTML, CSS, JavaScript

## Project Structure 📁

```
face_with_attendence/
├── app.py                          # Main Flask application
├── database.py                     # Database initialization and connection
├── models.py                       # Database models (Student, Course, Attendance)
├── face_recognition_module.py     # Face recognition core functionality
├── export_utils.py                # Excel export utilities
├── migrate_database.py            # Database migration script
├── requirements.txt               # Python dependencies
├── face_recognition_attendance.ipynb  # Jupyter notebook for exploration
│
├── CHECKIN_CHECKOUT_GUIDE.md      # Check-in/check-out documentation
├── QUICK_START.md                 # Quick reference guide
├── IMPLEMENTATION_SUMMARY.md      # Technical implementation details
│
├── templates/                     # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── mark_attendance.html
│   ├── admin_dashboard.html
│   ├── manage_students.html
│   ├── add_student.html
│   ├── manage_courses.html
│   ├── add_course.html
│   ├── view_attendance.html
│   ├── student_attendance.html
│   ├── course_attendance.html
│   └── settings.html
│
├── static/                        # Static files (CSS, JS, images)
├── student_images/                # Student photos for training
├── exports/                       # Exported Excel files
└── attendance_system.db           # SQLite database (created on first run)
```

## Installation 🚀

### Option 1: Docker (Easiest - Recommended for All Platforms)

**No Python installation needed! Works on Windows, macOS, and Linux:**

```bash
# Using Docker Compose
docker-compose up -d
```

Access at http://localhost:8181

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

### Option 2: Quick Start with Python (All Platforms)

**If you prefer running without Docker:**

```bash
# Run the cross-platform startup script
python start.py
```

This automatically handles:
- Virtual environment creation
- Dependency installation
- Database initialization
- Application startup

### Prerequisites (for Python installation)

- Python 3.8 or higher
- Webcam (for face recognition)
- pip (Python package manager)

### Platform-Specific Installation

For detailed installation instructions including troubleshooting, see [INSTALL.md](INSTALL.md).

#### Windows

```cmd
# Option 1: Docker (easiest)
docker-compose up -d

# Option 2: Python script (recommended)
python start.py

# Option 3: Batch file
start.bat

# Option 4: Manual
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### macOS

```bash
# Option 1: Docker (easiest)
docker-compose up -d

# Option 2: Python script (recommended)
python3 start.py

# Option 3: Shell script
chmod +x start.sh
./start.sh

# Option 4: Manual with Homebrew
brew install cmake
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Linux

```bash
# Option 1: Docker (easiest)
docker-compose up -d

# Option 2: Python script (recommended)
python3 start.py

# Option 3: Manual
sudo apt-get install build-essential cmake  # Ubuntu/Debian
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Note**: Installing `dlib` might require additional system dependencies. See [INSTALL.md](INSTALL.md) for detailed instructions.

## Usage 📖

### 1. Start the Application

**Easiest method (all platforms):**
```bash
python start.py
```

**Alternative methods:**
- Windows: Double-click `start.bat` or run it from Command Prompt
- macOS/Linux: Run `./start.sh` (make it executable first with `chmod +x start.sh`)
- Manual: Activate virtual environment and run `python app.py`

The application will start at: `http://localhost:8181`

### 2. Admin Login

- Navigate to: `http://localhost:8181/admin/login`
- **Default credentials:**
  - Username: `admin`
  - Password: `admin123`

### 3. Add Courses

1. Go to Admin Dashboard → Manage Courses
2. Click "Add New Course"
3. Fill in course details (code, name, instructor, schedule)

### 4. Add Students

1. Go to Admin Dashboard → Manage Students
2. Click "Add New Student"
3. Fill in student details
4. Upload a clear photo of the student's face
5. The system will automatically train the face recognition model

**Important**: 
- Use clear, well-lit photos
- Face should be clearly visible
- One person per photo
- Supported formats: JPG, PNG, JPEG

### 5. Mark Attendance

**For Students:**
1. Navigate to: `http://localhost:8181/mark-attendance`
2. Select the course from dropdown
3. Position your face in front of the camera
4. Click "Capture Attendance"
5. System will automatically recognize and mark attendance

### 6. View Reports

**Admin Panel:**
- View all attendance records
- Check individual student attendance
- View course-wise attendance
- Monitor attendance percentages
- Export to Excel

### 7. Export Data

**Export Options:**
- **All Attendance**: Export all records to Excel
- **Course Attendance**: Export specific course data
- **Attendance Summary**: Export summary with percentages

Files are saved in the `exports/` folder with current date.

## Using Jupyter Notebook 📓

For exploration and testing:

```bash
jupyter notebook face_recognition_attendance.ipynb
```

The notebook includes:
- Database initialization
- Adding sample data
- Testing face recognition
- Marking attendance
- Generating reports
- Data visualization

## Configuration ⚙️

### Attendance Threshold

Set minimum attendance percentage in Admin Panel → Settings

Default: 75%

Students below threshold are highlighted in reports.

### Database

SQLite database: `attendance_system.db`

To reset database:
```bash
rm attendance_system.db
python database.py
```

## API Endpoints 🔌

### Public Routes
- `GET /` - Home page
- `GET /mark-attendance` - Attendance marking page
- `POST /capture-attendance` - Capture and mark attendance
- `GET /video-feed` - Live camera feed

### Admin Routes (Require Login)
- `GET /admin/login` - Admin login
- `GET /admin/dashboard` - Dashboard
- `GET /admin/students` - Manage students
- `POST /admin/students/add` - Add new student
- `GET /admin/courses` - Manage courses
- `GET /admin/attendance` - View all attendance
- `GET /admin/export/summary` - Export summary

## Database Schema 💾

### Students Table
- student_id (Primary Key)
- name
- email
- phone
- image_path
- face_encoding (BLOB)
- created_at

### Courses Table
- course_code (Primary Key)
- course_name
- instructor
- schedule
- created_at

### Attendance Table
- id (Auto-increment)
- student_id (Foreign Key)
- course_code (Foreign Key)
- date
- time
- status
- marked_at

### Settings Table
- key
- value

## Troubleshooting 🔧

### Camera Not Working

**Issue**: Cannot access webcam
**Solution**: 
- Check camera permissions
- Close other applications using camera
- Try different camera index in code (change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`)

### Face Not Recognized

**Issue**: System can't recognize face
**Solution**:
- Ensure good lighting
- Face camera directly
- Remove glasses/masks if worn during photo
- Re-train with better quality photo

### Installation Errors

**Issue**: dlib installation fails
**Solution**:
- Install cmake first
- Use pre-built wheels (Windows)
- Check Python version (3.8+)

### Database Locked

**Issue**: Database is locked
**Solution**:
- Close other connections
- Restart application
- Check file permissions

## Security Considerations 🔒

**Important for Production:**

1. **Change default admin password**
2. **Use environment variables for secrets**
3. **Enable HTTPS**
4. **Implement proper authentication**
5. **Add CSRF protection**
6. **Validate all inputs**
7. **Secure file uploads**

Example: Update `app.secret_key` in `app.py`:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')
```

## Future Enhancements 🚀

- [ ] Multiple face detection in single frame
- [ ] Email notifications for low attendance
- [ ] Mobile app integration
- [ ] Biometric authentication
- [ ] Advanced analytics dashboard
- [ ] Class scheduling integration
- [ ] Student self-service portal
- [ ] Multi-camera support
- [ ] Cloud storage integration
- [ ] REST API for mobile apps

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open source and available for educational purposes.

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## Acknowledgments 🙏

- OpenCV team for computer vision library
- face_recognition library by Adam Geitgey
- Flask framework
- SQLite database

## Version History 📋

**v1.0.0** (Current)
- Initial release
- Face recognition attendance system
- Admin panel
- Excel export
- Jupyter notebook

---

**Made with ❤️ for educational institutions**

*Simplifying attendance management through AI*
