#!/usr/bin/env python3
"""
Centralized Script Manager
Provides easy access to all utility scripts
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def print_menu():
    """Display main menu"""
    print("\n" + "=" * 70)
    print("  Face Recognition Attendance System - Script Manager")
    print("=" * 70)
    print("\nAvailable Commands:")
    print("\n  Setup & Initialization:")
    print("    1. Initialize Application     - Run full system setup")
    print("    2. Verify Installation        - Check all components")
    print("    3. Download Liveness Model    - Setup anti-spoofing")
    print("\n  Database:")
    print("    4. Initialize Database        - Create/reset database")
    print("    5. Migrate Database          - Run database migrations")
    print("\n  Verification:")
    print("    6. Verify Anti-Spoofing      - Test liveness detection")
    print("    7. Test System               - Run all tests")
    print("\n  Application:")
    print("    8. Start Application         - Launch Flask app")
    print("    9. Quick Setup & Start       - Setup + Start app")
    print("\n  Other:")
    print("    0. Exit")
    print("\n" + "=" * 70)


def run_startup_init():
    """Run startup initialization"""
    print("\n🚀 Running Application Initialization...\n")
    from src.utils.startup import initialize_app
    success = initialize_app(silent=False)
    if success:
        print("\n✅ Initialization completed successfully!")
    else:
        print("\n❌ Initialization failed. Please check errors above.")
    return success


def run_verify_installation():
    """Run installation verification"""
    print("\n🔍 Verifying Installation...\n")
    import verify_installation
    verify_installation.run_verification()


def run_download_model():
    """Download liveness detection model"""
    print("\n📥 Downloading Liveness Detection Model...\n")
    import download_model
    download_model.download_shape_predictor()


def run_init_database():
    """Initialize database"""
    print("\n📦 Initializing Database...\n")
    from database import init_db
    init_db()
    print("\n✅ Database initialized successfully!")


def run_migrate_database():
    """Run database migrations"""
    print("\n🔄 Running Database Migrations...\n")
    import migrate_database
    # The migrate script will run automatically


def run_verify_anti_spoofing():
    """Verify anti-spoofing setup"""
    print("\n🔒 Verifying Anti-Spoofing Setup...\n")
    import verify_anti_spoofing
    result = verify_anti_spoofing.main()
    return result == 0


def run_test_system():
    """Run all system tests"""
    print("\n🧪 Running System Tests...\n")
    tests_passed = 0
    tests_total = 3
    
    # Test 1: Installation
    print("\n[1/3] Testing Installation...")
    import verify_installation
    verify_installation.run_verification()
    tests_passed += 1
    
    # Test 2: Anti-spoofing
    print("\n[2/3] Testing Anti-Spoofing...")
    if run_verify_anti_spoofing():
        tests_passed += 1
    
    # Test 3: Startup
    print("\n[3/3] Testing Startup...")
    from src.utils.startup import initialize_app
    if initialize_app(silent=True):
        tests_passed += 1
        print("✅ Startup test passed")
    else:
        print("❌ Startup test failed")
    
    print(f"\n{'=' * 70}")
    print(f"Test Results: {tests_passed}/{tests_total} tests passed")
    print("=" * 70)


def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Flask Application...\n")
    import app
    # The app will start when imported


def quick_setup_and_start():
    """Quick setup and start"""
    print("\n⚡ Quick Setup & Start...\n")
    
    # Run initialization
    if not run_startup_init():
        print("\n❌ Setup failed. Cannot start application.")
        return
    
    # Start application
    print("\n" + "=" * 70)
    input("Press Enter to start the application...")
    start_application()


def main():
    """Main script manager loop"""
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == '0':
                print("\n👋 Goodbye!\n")
                sys.exit(0)
            elif choice == '1':
                run_startup_init()
            elif choice == '2':
                run_verify_installation()
            elif choice == '3':
                run_download_model()
            elif choice == '4':
                run_init_database()
            elif choice == '5':
                run_migrate_database()
            elif choice == '6':
                run_verify_anti_spoofing()
            elif choice == '7':
                run_test_system()
            elif choice == '8':
                start_application()
                break  # Exit after starting app
            elif choice == '9':
                quick_setup_and_start()
                break  # Exit after starting app
            else:
                print("\n❌ Invalid choice. Please enter a number between 0-9.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
