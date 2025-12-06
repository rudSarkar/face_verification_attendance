"""
Configuration Settings for Face Recognition Attendance System
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 8181))

# Upload Configuration
UPLOAD_FOLDER = BASE_DIR / 'student_images'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Database Configuration
DATABASE_PATH = BASE_DIR / 'attendance.db'

# Export Configuration
EXPORT_FOLDER = BASE_DIR / 'exports'

# Face Recognition Configuration
FACE_RECOGNITION_TOLERANCE = 0.6
FACE_RECOGNITION_MODEL = 'hog'  # or 'cnn' for better accuracy (slower)

# Liveness Detection Configuration
ENABLE_LIVENESS_DETECTION = True
LIVENESS_MODEL_PATH = BASE_DIR / 'shape_predictor_68_face_landmarks.dat'
LIVENESS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'

# Default Settings
DEFAULT_MIN_ATTENDANCE_PERCENTAGE = 75
DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin123'

# Logging Configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'app.log'

# Ensure directories exist
REQUIRED_DIRS = [
    UPLOAD_FOLDER,
    EXPORT_FOLDER,
    BASE_DIR / 'logs',
    BASE_DIR / 'templates',
    BASE_DIR / 'static',
]

def ensure_directories():
    """Create required directories if they don't exist"""
    for directory in REQUIRED_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
