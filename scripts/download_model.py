#!/usr/bin/env python3
"""
Download dlib shape predictor model for liveness detection
Run this script before starting the application if liveness detection is needed
"""

import os
import urllib.request
import bz2
import sys

def download_shape_predictor():
    """
    Download the dlib shape predictor model if not present
    """
    model_file = "shape_predictor_68_face_landmarks.dat"
    
    if os.path.exists(model_file):
        print(f"✓ {model_file} already exists")
        return True
    
    print("="*60)
    print("Downloading dlib shape predictor model...")
    print("This is required for liveness detection (blink detection)")
    print("="*60)
    
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    compressed_file = "shape_predictor_68_face_landmarks.dat.bz2"
    
    try:
        # Download compressed file
        print(f"\n📥 Downloading from {url}")
        print("Please wait, this may take a few minutes (~100 MB)...")
        
        def progress_callback(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, downloaded * 100 / total_size)
            bar_length = 40
            filled = int(bar_length * downloaded / total_size)
            bar = '█' * filled + '-' * (bar_length - filled)
            print(f'\r[{bar}] {percent:.1f}%', end='', flush=True)
        
        urllib.request.urlretrieve(url, compressed_file, progress_callback)
        print("\n✓ Download complete")
        
        # Decompress
        print("\n📦 Decompressing...")
        with bz2.open(compressed_file, 'rb') as source, open(model_file, 'wb') as dest:
            dest.write(source.read())
        
        # Remove compressed file
        os.remove(compressed_file)
        
        print(f"✓ {model_file} extracted successfully")
        print(f"✓ File size: {os.path.getsize(model_file) / (1024*1024):.1f} MB")
        print("\n" + "="*60)
        print("✅ Setup complete! Liveness detection is ready to use.")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to download model: {str(e)}")
        print("\nAlternative: Download manually from:")
        print(url)
        print(f"Then extract to: {os.path.abspath(model_file)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Liveness Detection Setup")
    print("="*60)
    print("\nThis will download the facial landmark detector model")
    print("required for blink detection (anti-spoofing).")
    print("\nPressing Ctrl+C will cancel the download.\n")
    
    try:
        success = download_shape_predictor()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user")
        sys.exit(1)
