#!/usr/bin/env python3
"""
Startup Initialization Module
Automatically handles all setup tasks when the application starts
"""
import os
import sys
import urllib.request
import bz2
import sqlite3
from pathlib import Path
from typing import Tuple, List
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StartupInitializer:
    """Handles all initialization tasks on application startup"""
    
    def __init__(self, base_dir: Path = None):
        # Resolve base_dir correctly - should be project root, not src folder
        if base_dir is None:
            # If called from src/utils/startup.py, go up 2 levels to project root
            current_file = Path(__file__).resolve()
            if 'src' in current_file.parts:
                self.base_dir = current_file.parent.parent.parent
            else:
                self.base_dir = current_file.parent
        else:
            self.base_dir = base_dir
        
        self.errors = []
        self.warnings = []
        
    def initialize(self, silent: bool = False) -> Tuple[bool, List[str], List[str]]:
        """
        Run all initialization tasks
        
        Args:
            silent: If True, suppress console output
            
        Returns:
            Tuple of (success, errors, warnings)
        """
        if not silent:
            self._print_header("Application Startup Initialization")
        
        tasks = [
            ("Creating directories", self._create_directories),
            ("Checking Python dependencies", self._check_dependencies),
            ("Initializing database", self._initialize_database),
            ("Setting up liveness detection", self._setup_liveness_detection),
            ("Verifying file structure", self._verify_file_structure),
            ("Setting up default configuration", self._setup_default_config),
        ]
        
        for task_name, task_func in tasks:
            if not silent:
                logger.info(f"⏳ {task_name}...")
            
            try:
                success, message = task_func()
                if success:
                    if not silent:
                        logger.info(f"✅ {task_name}: {message}")
                else:
                    self.warnings.append(f"{task_name}: {message}")
                    if not silent:
                        logger.warning(f"⚠️  {task_name}: {message}")
            except Exception as e:
                error_msg = f"{task_name}: {str(e)}"
                self.errors.append(error_msg)
                if not silent:
                    logger.error(f"❌ {task_name}: {str(e)}")
        
        if not silent:
            self._print_summary()
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _create_directories(self) -> Tuple[bool, str]:
        """Create all required directories"""
        required_dirs = [
            'student_images',
            'exports',
            'logs',
            'templates',
            'static',
            'docs',
            '__pycache__',
        ]
        
        created = []
        for dir_name in required_dirs:
            dir_path = self.base_dir / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                created.append(dir_name)
        
        if created:
            return True, f"Created {len(created)} directories"
        return True, "All directories exist"
    
    def _check_dependencies(self) -> Tuple[bool, str]:
        """Check if critical dependencies are installed"""
        critical_packages = {
            'flask': 'Flask',
            'cv2': 'opencv-python',
            'face_recognition': 'face_recognition',
            'numpy': 'numpy',
        }
        
        missing = []
        for package, name in critical_packages.items():
            try:
                if package == 'cv2':
                    import cv2
                else:
                    __import__(package)
            except ImportError:
                missing.append(name)
        
        if missing:
            return False, f"Missing packages: {', '.join(missing)}. Run: pip install -r requirements.txt"
        
        return True, "All critical dependencies installed"
    
    def _initialize_database(self) -> Tuple[bool, str]:
        """Initialize database with required tables"""
        db_path = self.base_dir / 'attendance.db'
        
        try:
            # Add base_dir to path if not already there
            base_dir_str = str(self.base_dir)
            if base_dir_str not in sys.path:
                sys.path.insert(0, base_dir_str)
            
            # Import database module
            from database import init_db
            
            # Check if database already exists
            db_exists = db_path.exists()
            
            # Initialize database
            init_db()
            
            # Verify tables exist
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            if db_exists:
                return True, f"Database verified ({len(tables)} tables)"
            else:
                return True, f"Database created with {len(tables)} tables"
                
        except Exception as e:
            return False, f"Database initialization failed: {str(e)}"
    
    def _setup_liveness_detection(self) -> Tuple[bool, str]:
        """Download and setup liveness detection model if needed"""
        model_file = self.base_dir / 'shape_predictor_68_face_landmarks.dat'
        
        # Check if liveness detection dependencies are available
        try:
            import dlib
            import scipy
            import imutils
        except ImportError:
            return True, "Liveness detection dependencies not installed (optional)"
        
        # Check if model already exists
        if model_file.exists():
            size_mb = model_file.stat().st_size / (1024 * 1024)
            return True, f"Model exists ({size_mb:.1f} MB)"
        
        # Ask if user wants to download (auto-download in silent mode)
        return True, "Model not found. Run 'python scripts/download_model.py' to enable liveness detection"
    
    def _verify_file_structure(self) -> Tuple[bool, str]:
        """Verify critical files exist"""
        critical_files = [
            'app.py',
            'database.py',
            'models.py',
            'face_recognition_module.py',
            'requirements.txt',
        ]
        
        missing = []
        for file_name in critical_files:
            if not (self.base_dir / file_name).exists():
                missing.append(file_name)
        
        if missing:
            return False, f"Missing critical files: {', '.join(missing)}"
        
        return True, "All critical files present"
    
    def _setup_default_config(self) -> Tuple[bool, str]:
        """Setup default configuration in database"""
        try:
            # Add base_dir to path if not already there
            base_dir_str = str(self.base_dir)
            if base_dir_str not in sys.path:
                sys.path.insert(0, base_dir_str)
            
            from models import Settings, Admin
            
            # Check if settings exist
            threshold = Settings.get_min_attendance_percentage()
            
            # Check if default admin exists
            admin_exists = Admin.verify_admin('admin', 'admin123')
            
            messages = []
            if threshold:
                messages.append(f"attendance threshold: {threshold}%")
            if admin_exists:
                messages.append("default admin account exists")
            
            if messages:
                return True, ", ".join(messages).capitalize()
            else:
                return True, "Configuration ready"
                
        except Exception as e:
            return True, f"Configuration check skipped: {str(e)}"
    
    def _print_header(self, text: str):
        """Print a formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70 + "\n")
    
    def _print_summary(self):
        """Print initialization summary"""
        print("\n" + "=" * 70)
        print("  Initialization Summary")
        print("=" * 70)
        
        if not self.errors and not self.warnings:
            print("\n✅ All initialization tasks completed successfully!")
        else:
            if self.errors:
                print(f"\n❌ Errors: {len(self.errors)}")
                for error in self.errors:
                    print(f"   - {error}")
            
            if self.warnings:
                print(f"\n⚠️  Warnings: {len(self.warnings)}")
                for warning in self.warnings:
                    print(f"   - {warning}")
        
        print("\n" + "=" * 70 + "\n")


def initialize_app(silent: bool = False) -> bool:
    """
    Initialize the application on startup
    
    Args:
        silent: If True, suppress console output
        
    Returns:
        True if initialization successful, False otherwise
    """
    initializer = StartupInitializer()
    success, errors, warnings = initializer.initialize(silent=silent)
    
    if not success:
        logger.error("Application initialization failed!")
        logger.error("Please fix the errors above before starting the application.")
        return False
    
    if not silent and not errors and not warnings:
        logger.info("🚀 Application is ready to start!")
    
    return True


if __name__ == "__main__":
    """Run initialization manually"""
    success = initialize_app(silent=False)
    sys.exit(0 if success else 1)
