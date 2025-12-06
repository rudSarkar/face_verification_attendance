# Face Recognition Attendance System 🎓

A comprehensive AI-powered attendance management system using face recognition technology with **check-in/check-out functionality** to prevent class bunking. Built with Flask, OpenCV, and SQLite.

## 🎉 Latest Updates

### 🚀 Automatic Setup & Improved Structure
- ✨ **One-command startup**: Just run `python run.py`
- ✨ **Auto-initialization**: Automatically sets up everything on first run
- ✨ **Better organization**: Clean, modular project structure
- ✨ **Interactive script manager**: Easy access to all utilities
- ✨ **Comprehensive logging**: Better error tracking and debugging

> **New users**: Simply run `python run.py` after installing dependencies!

## ✨ Cross-Platform Support

**Works on Windows, macOS, and Linux!**

- 🐳 **Docker support** for easiest setup (recommended)
- 🐍 **Python cross-platform script** (`start.py`)
- 💻 **Platform-specific scripts** (`.bat` for Windows, `.sh` for Unix)
- 📦 **All dependencies work across platforms**

## 🆕 Check-In/Check-Out System

**Prevents students from leaving early!**

- ✅ Students must **check in** at class start
- ✅ Students must **check out** before leaving
- ✅ System tracks actual **duration** in class
- ✅ Minimum duration required for "Present" status
- ✅ Early departure flagged as "Absent (Left Early)"

📚 **[Read the Full Guide](docs/CHECKIN_CHECKOUT_GUIDE.md)** | 📖 **[Quick Start](docs/QUICK_START.md)**

## Features ✨

- **Face Recognition**: Automatic student identification using advanced AI
- **🛡️ Anti-Spoofing**: Liveness detection prevents photo/picture attacks (NEW!)
- **Check-In/Check-Out**: Track entry and exit times with duration monitoring
- **Duration Enforcement**: Configurable minimum class duration per course
- **Web Interface**: User-friendly web application for marking attendance
- **Admin Panel**: Complete dashboard for managing students, courses, and attendance
- **Real-time Camera**: Live webcam feed for face detection with blink counter
- **Excel Export**: Export attendance reports with timing details
- **Attendance Tracking**: Calculate and monitor attendance percentages
- **SQLite Database**: Lightweight and efficient data storage
- **Jupyter Notebook**: Interactive exploration and testing

> **🔒 Security Note**: The system now includes blink detection to verify you're a real person, not a photo! See [LIVENESS_DETECTION.md](LIVENESS_DETECTION.md) for details.

## Tech Stack 🛠️

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Face Recognition**: OpenCV, face_recognition library
- **Data Processing**: Pandas, NumPy
- **Export**: openpyxl (Excel export)
- **Frontend**: HTML, CSS, JavaScript

## Project Structure 📁

The project follows an organized, modular structure for easy maintenance:

```
face_with_attendence/
├── 📁 src/                          # Source code modules
│   ├── core/                        # Core business logic
│   ├── utils/                       # Utilities
│   │   └── startup.py              # Auto-initialization on startup
│   └── routes/                      # Route handlers
│
├── 📁 config/                       # Configuration
│   └── settings.py                  # Centralized settings
│
├── 📁 scripts/                      # Utility scripts
│   ├── manager.py                   # Interactive script manager ⭐
│   ├── download_model.py           # Liveness model downloader
│   ├── verify_installation.py      # Installation checker
│   └── verify_anti_spoofing.py     # Anti-spoofing verifier
│
├── 📁 templates/                    # HTML templates
├── 📁 static/                       # CSS, JavaScript
├── 📁 student_images/              # Student photos
├── 📁 exports/                      # Excel exports
├── 📁 docs/                         # Documentation
│   ├── PROJECT_STRUCTURE.md        # Detailed structure guide
│   ├── CHECKIN_CHECKOUT_GUIDE.md
│   └── ... (more guides)
│
├── 🐍 run.py                        # Quick start script ⭐ NEW!
├── 🐍 app.py                        # Main Flask application
├── 🐍 database.py                   # Database operations
├── 🐍 models.py                     # Data models
├── 🐍 face_recognition_module.py   # Face recognition
├── 🐍 liveness_detection.py        # Anti-spoofing
│
├── 📝 requirements.txt              # Dependencies
└── 📝 README.md                     # This file
```

> 📖 See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed information about the new structure.

## 🚀 Quick Start (New & Improved!)

### Fastest Way to Get Started

```bash
# 1. Install dependencies (first time only)
pip install -r requirements.txt

# 2. Run the application (auto-setup included!)
python run.py
```

That's it! The application now automatically:
- ✅ Creates all required directories
- ✅ Checks dependencies
- ✅ Initializes the database
- ✅ Sets up default configuration
- ✅ Starts the Flask server

Access at **http://localhost:8181**

Default admin credentials:
- Username: `admin`
- Password: `admin123`

### Alternative Methods

#### Option 1: Interactive Script Manager
```bash
python scripts/manager.py
```
Provides a menu with options for setup, verification, testing, and more!

#### Option 2: Docker (Easiest - No Python Required)
```bash
docker-compose up -d
```
See [DOCKER.md](docs/DOCKER.md) for details.

#### Option 3: Traditional Method
```bash
# Setup (first time only)
python setup.py

# Start application
python app.py
```

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- Webcam (for face recognition)
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd face_with_attendence
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

The application handles everything else automatically!

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
