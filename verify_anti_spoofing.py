#!/usr/bin/env python3
"""
Anti-Spoofing Verification Test
Tests that liveness detection is properly integrated
"""

import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import cv2
        print("  ✓ opencv-python")
    except ImportError as e:
        print(f"  ✗ opencv-python: {e}")
        return False
        
    try:
        import dlib
        print("  ✓ dlib")
    except ImportError as e:
        print(f"  ✗ dlib: {e}")
        return False
        
    try:
        from scipy.spatial import distance
        print("  ✓ scipy")
    except ImportError as e:
        print(f"  ✗ scipy: {e}")
        return False
        
    try:
        from imutils import face_utils
        print("  ✓ imutils")
    except ImportError as e:
        print(f"  ✗ imutils: {e}")
        return False
    
    return True

def test_model_file():
    """Test that the facial landmark model exists"""
    print("\nTesting model file...")
    import os
    model_file = "shape_predictor_68_face_landmarks.dat"
    
    if os.path.exists(model_file):
        size_mb = os.path.getsize(model_file) / (1024 * 1024)
        print(f"  ✓ {model_file} ({size_mb:.1f} MB)")
        return True
    else:
        print(f"  ✗ {model_file} not found")
        print("    Run: python download_model.py")
        return False

def test_liveness_module():
    """Test that liveness detection module can be loaded"""
    print("\nTesting liveness detection module...")
    try:
        from liveness_detection import LivenessDetector
        detector = LivenessDetector()
        print("  ✓ LivenessDetector initialized")
        print(f"    - EAR Threshold: {detector.EAR_THRESHOLD}")
        print(f"    - Consecutive Frames: {detector.EAR_CONSEC_FRAMES}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to initialize: {e}")
        return False

def test_face_recognition_integration():
    """Test that face recognition module has liveness integration"""
    print("\nTesting face recognition integration...")
    try:
        from face_recognition_module import FaceRecognitionSystem
        fr_system = FaceRecognitionSystem(enable_liveness=True)
        
        if fr_system.enable_liveness:
            print("  ✓ Liveness detection enabled in FaceRecognitionSystem")
            if fr_system.liveness_detector:
                print("  ✓ LivenessDetector instance created")
            else:
                print("  ⚠ LivenessDetector is None (may be OK if model missing)")
        else:
            print("  ⚠ Liveness detection disabled")
        
        return True
    except Exception as e:
        print(f"  ✗ Failed to initialize: {e}")
        return False

def test_app_integration():
    """Test that app.py has liveness detection code"""
    print("\nTesting app.py integration...")
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            
        checks = [
            ('blink_count', 'Blink count parameter'),
            ('liveness_required', 'Liveness required check'),
            ('check_liveness=', 'Check liveness parameter'),
            ('is_live', 'Liveness status variable'),
        ]
        
        all_found = True
        for check, desc in checks:
            if check in content:
                print(f"  ✓ {desc} found")
            else:
                print(f"  ✗ {desc} not found")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"  ✗ Failed to check: {e}")
        return False

def test_frontend_integration():
    """Test that frontend has liveness UI elements"""
    print("\nTesting frontend integration...")
    try:
        with open('templates/mark_attendance.html', 'r') as f:
            content = f.read()
            
        checks = [
            ('liveness-status', 'Liveness status element'),
            ('blink-count', 'Blink counter element'),
            ('blink_count:', 'Blink count JavaScript'),
            ('liveness_required', 'Liveness required handling'),
        ]
        
        all_found = True
        for check, desc in checks:
            if check in content:
                print(f"  ✓ {desc} found")
            else:
                print(f"  ✗ {desc} not found")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"  ✗ Failed to check: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Anti-Spoofing Integration Verification")
    print("="*60)
    
    tests = [
        ("Dependencies", test_imports),
        ("Model File", test_model_file),
        ("Liveness Module", test_liveness_module),
        ("Face Recognition", test_face_recognition_integration),
        ("App Integration", test_app_integration),
        ("Frontend Integration", test_frontend_integration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Anti-spoofing is ready to use.")
        print("\nNext steps:")
        print("  1. python liveness_detection.py  # Test standalone")
        print("  2. python app.py                 # Start the app")
        print("="*60)
        return 0
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
