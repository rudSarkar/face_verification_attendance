#!/usr/bin/env python3
"""
Quick Start Script - One command to rule them all!
This script handles everything needed to get the application running
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    """Quick start the application"""
    print("\n" + "=" * 70)
    print("  Face Recognition Attendance System - Quick Start")
    print("=" * 70)
    print("\n🚀 Starting automatic setup and launch...\n")
    
    # Step 1: Run startup initialization
    print("Step 1: Running initialization checks...")
    try:
        from src.utils.startup import initialize_app
        if not initialize_app(silent=False):
            print("\n❌ Initialization failed!")
            print("\nTroubleshooting:")
            print("  1. Install dependencies: pip install -r requirements.txt")
            print("  2. Check Python version: python --version (3.8+ required)")
            print("  3. Run: python scripts/manager.py (for detailed options)")
            return 1
    except Exception as e:
        print(f"\n⚠️  Warning: Initialization module not available: {e}")
        print("Continuing with basic setup...\n")
        
        # Fallback: Basic initialization
        try:
            from database import init_db
            init_db()
            print("✅ Database initialized")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return 1
    
    print("\n" + "=" * 70)
    print("  Setup Complete! Starting Application...")
    print("=" * 70)
    print("\nThe application will start momentarily...")
    print("\n📱 Access the application at:")
    print("   🏠 Home:          http://localhost:8181")
    print("   👨‍💼 Admin Panel:   http://localhost:8181/admin/login")
    print("   ✅ Mark Attendance: http://localhost:8181/mark-attendance")
    print("\n👤 Default Admin Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n⌨️  Press Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    # Step 2: Start the application
    try:
        import app
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user\n")
        return 0
    except Exception as e:
        print(f"\n❌ Failed to start application: {e}")
        print("\nPlease check the error above and try again.")
        print("For help, run: python scripts/manager.py")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
