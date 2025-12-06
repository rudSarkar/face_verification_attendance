"""
Liveness Detection Module
Implements blink detection to prevent photo/picture spoofing attacks
"""

import cv2
import dlib
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils

class LivenessDetector:
    """Detects if a face is from a live person by detecting blinks"""
    
    # Eye Aspect Ratio (EAR) threshold for detecting blink
    EAR_THRESHOLD = 0.25
    
    # Number of consecutive frames the eye must be below threshold to count as a blink
    EAR_CONSEC_FRAMES = 2
    
    def __init__(self):
        """Initialize the liveness detector with dlib's face detector and predictor"""
        try:
            # Initialize dlib's face detector and facial landmark predictor
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
            
            # Grab the indexes of the facial landmarks for the left and right eye
            (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
            (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
            
            # Initialize blink counter and frame counter
            self.blink_counter = 0
            self.frame_counter = 0
            self.total_blinks = 0
            
        except Exception as e:
            raise Exception(f"Failed to initialize liveness detector: {str(e)}\n"
                          f"Make sure 'shape_predictor_68_face_landmarks.dat' is in the project directory.")
    
    def calculate_ear(self, eye):
        """
        Calculate the Eye Aspect Ratio (EAR)
        
        The EAR is used to detect blinks:
        - When eyes are open: EAR is relatively constant
        - When eyes close: EAR rapidly decreases
        
        Args:
            eye: Array of (x, y) coordinates for the eye landmarks
            
        Returns:
            float: The Eye Aspect Ratio
        """
        # Compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        
        # Compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        
        # Compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        
        return ear
    
    def reset_blink_counter(self):
        """Reset the blink counters"""
        self.blink_counter = 0
        self.frame_counter = 0
        self.total_blinks = 0
    
    def detect_blink(self, frame):
        """
        Detect if a blink occurred in the given frame
        
        Args:
            frame: Input video frame (BGR format from OpenCV)
            
        Returns:
            tuple: (blink_detected, total_blinks, ear_value, frame_with_overlay)
                - blink_detected: True if a blink was detected in this frame
                - total_blinks: Total number of blinks detected so far
                - ear_value: Current Eye Aspect Ratio value
                - frame_with_overlay: Frame with eye contours and EAR value drawn
        """
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the grayscale frame
        faces = self.detector(gray, 0)
        
        blink_detected = False
        ear = 0.0
        
        # Process each detected face
        for face in faces:
            # Determine the facial landmarks for the face region
            shape = self.predictor(gray, face)
            shape = face_utils.shape_to_np(shape)
            
            # Extract the left and right eye coordinates
            leftEye = shape[self.lStart:self.lEnd]
            rightEye = shape[self.rStart:self.rEnd]
            
            # Compute the eye aspect ratio for both eyes
            leftEAR = self.calculate_ear(leftEye)
            rightEAR = self.calculate_ear(rightEye)
            
            # Average the eye aspect ratio for both eyes
            ear = (leftEAR + rightEAR) / 2.0
            
            # Visualize the eye regions
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            
            # Check if the eye aspect ratio is below the blink threshold
            if ear < self.EAR_THRESHOLD:
                self.frame_counter += 1
            else:
                # If the eyes were closed for a sufficient number of frames
                # then increment the total number of blinks
                if self.frame_counter >= self.EAR_CONSEC_FRAMES:
                    self.total_blinks += 1
                    blink_detected = True
                
                # Reset the eye frame counter
                self.frame_counter = 0
            
            # Draw the total number of blinks and EAR on the frame
            cv2.putText(frame, f"Blinks: {self.total_blinks}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"EAR: {ear:.2f}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return blink_detected, self.total_blinks, ear, frame
    
    def verify_liveness(self, frame, min_blinks=1):
        """
        Verify if the person in the frame is live by checking for blinks
        
        Args:
            frame: Input video frame
            min_blinks: Minimum number of blinks required to pass liveness check
            
        Returns:
            tuple: (is_live, total_blinks, message)
                - is_live: True if liveness check passed
                - total_blinks: Total number of blinks detected
                - message: Status message
        """
        blink_detected, total_blinks, ear, processed_frame = self.detect_blink(frame)
        
        is_live = total_blinks >= min_blinks
        
        if is_live:
            message = f"✓ Liveness verified ({total_blinks} blink(s) detected)"
        else:
            message = f"Please blink naturally ({total_blinks}/{min_blinks} blinks detected)"
        
        return is_live, total_blinks, message
    
    def run_liveness_check(self, camera_index=0, duration_seconds=5, min_blinks=2):
        """
        Run a complete liveness check session
        
        Args:
            camera_index: Camera device index (default: 0)
            duration_seconds: How long to run the check
            min_blinks: Minimum number of blinks required
            
        Returns:
            tuple: (passed, total_blinks, message)
        """
        self.reset_blink_counter()
        
        camera = cv2.VideoCapture(camera_index)
        
        if not camera.isOpened():
            return False, 0, "Failed to open camera"
        
        start_time = cv2.getTickCount()
        fps = cv2.getTickFrequency()
        
        while True:
            success, frame = camera.read()
            
            if not success:
                break
            
            # Detect blinks
            blink_detected, total_blinks, ear, processed_frame = self.detect_blink(frame)
            
            # Calculate elapsed time
            elapsed = (cv2.getTickCount() - start_time) / fps
            remaining = max(0, duration_seconds - elapsed)
            
            # Draw instructions
            cv2.putText(processed_frame, "Please blink naturally", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(processed_frame, f"Time: {remaining:.1f}s", (10, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # Show the frame
            cv2.imshow("Liveness Detection", processed_frame)
            
            # Check if duration has elapsed
            if elapsed >= duration_seconds:
                break
            
            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        camera.release()
        cv2.destroyAllWindows()
        
        # Determine if liveness check passed
        passed = total_blinks >= min_blinks
        
        if passed:
            message = f"✓ Liveness check PASSED ({total_blinks} blinks detected)"
        else:
            message = f"✗ Liveness check FAILED ({total_blinks}/{min_blinks} blinks detected)"
        
        return passed, total_blinks, message


def download_shape_predictor():
    """
    Download the dlib shape predictor model if not present
    """
    import os
    import urllib.request
    import bz2
    
    model_file = "shape_predictor_68_face_landmarks.dat"
    
    if os.path.exists(model_file):
        print(f"✓ {model_file} already exists")
        return True
    
    print("Downloading shape predictor model...")
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    compressed_file = "shape_predictor_68_face_landmarks.dat.bz2"
    
    try:
        # Download compressed file
        print(f"Downloading from {url}...")
        urllib.request.urlretrieve(url, compressed_file)
        
        # Decompress
        print("Decompressing...")
        with bz2.open(compressed_file, 'rb') as source, open(model_file, 'wb') as dest:
            dest.write(source.read())
        
        # Remove compressed file
        os.remove(compressed_file)
        
        print(f"✓ {model_file} downloaded successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to download model: {str(e)}")
        return False


if __name__ == "__main__":
    """Test the liveness detector"""
    print("="*60)
    print("Liveness Detection Test")
    print("="*60)
    
    # Download model if needed
    if not download_shape_predictor():
        print("Failed to download required model. Exiting.")
        exit(1)
    
    # Initialize detector
    print("\nInitializing liveness detector...")
    detector = LivenessDetector()
    
    # Run liveness check
    print("\nStarting liveness check...")
    print("Instructions:")
    print("- Look at the camera")
    print("- Blink naturally at least 2 times")
    print("- The check will run for 5 seconds")
    print("\nPress any key to start...")
    input()
    
    passed, blinks, message = detector.run_liveness_check(
        camera_index=0,
        duration_seconds=5,
        min_blinks=2
    )
    
    print("\n" + "="*60)
    print(message)
    print("="*60)
