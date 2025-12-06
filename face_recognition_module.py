import face_recognition
import cv2
import os
import numpy as np
from models import Student
import pickle
from liveness_detection import LivenessDetector

class FaceRecognitionSystem:
    def __init__(self, enable_liveness=True):
        self.known_face_encodings = []
        self.known_face_ids = []
        self.enable_liveness = enable_liveness
        self.liveness_detector = None
        
        # Initialize liveness detector if enabled
        if self.enable_liveness:
            try:
                self.liveness_detector = LivenessDetector()
                print("✓ Liveness detection enabled")
            except Exception as e:
                print(f"⚠ Warning: Failed to initialize liveness detector: {str(e)}")
                print("  Continuing without liveness detection...")
                self.enable_liveness = False
        
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load all known face encodings from database"""
        student_ids, encodings = Student.get_all_face_encodings()
        self.known_face_ids = student_ids
        self.known_face_encodings = encodings
        print(f"Loaded {len(self.known_face_encodings)} face encodings")
    
    def train_from_image(self, image_path, student_id):
        """
        Train face recognition from a single image
        Returns the face encoding or None if no face found
        """
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face encodings
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                print(f"No face found in {image_path}")
                return None
            
            if len(face_encodings) > 1:
                print(f"Multiple faces found in {image_path}, using the first one")
            
            # Return the first face encoding
            return face_encodings[0]
        
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return None
    
    def train_from_folder(self, folder_path, student_id):
        """
        Train face recognition from multiple images in a folder
        Returns the average face encoding or None if no faces found
        """
        encodings = []
        
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                encoding = self.train_from_image(image_path, student_id)
                
                if encoding is not None:
                    encodings.append(encoding)
        
        if len(encodings) == 0:
            return None
        
        # Return average encoding for better accuracy
        return np.mean(encodings, axis=0)
    
    def recognize_face_from_frame(self, frame, tolerance=0.6, check_liveness=True):
        """
        Recognize face from a video frame with optional liveness detection
        Returns (student_id, confidence, face_location, is_live) or (None, None, None, False) if no match
        
        Args:
            frame: Input video frame
            tolerance: Face matching tolerance (lower = more strict)
            check_liveness: Whether to perform liveness detection
        
        Returns:
            tuple: (student_id, confidence, face_location, is_live)
        """
        # Perform liveness check if enabled
        is_live = True
        if check_liveness and self.enable_liveness and self.liveness_detector:
            _, blinks, _, frame = self.liveness_detector.detect_blink(frame)
            # Require at least 1 blink to be detected over the session
            # The frontend will handle accumulating blinks over multiple frames
            is_live = blinks >= 0  # We'll check blink count in the calling function
        
        # Convert BGR to RGB (OpenCV uses BGR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces in frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        if len(face_encodings) == 0:
            return None, None, None, False
        
        # Check each face found in frame
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=tolerance
            )
            
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, 
                face_encoding
            )
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    student_id = self.known_face_ids[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    return student_id, confidence, face_location, is_live
        
        return None, None, None, False
    
    def recognize_face_from_image(self, image_path, tolerance=0.6):
        """
        Recognize face from an image file
        Returns (student_id, confidence) or (None, None) if no match
        """
        try:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                return None, None
            
            face_encoding = face_encodings[0]
            
            # Compare with known faces
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=tolerance
            )
            
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, 
                face_encoding
            )
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    student_id = self.known_face_ids[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    return student_id, confidence
            
            return None, None
        
        except Exception as e:
            print(f"Error recognizing face: {str(e)}")
            return None, None
    
    def draw_face_box(self, frame, face_location, student_id, confidence, is_live=True):
        """Draw bounding box and label on frame with liveness indicator"""
        top, right, bottom, left = face_location
        
        # Choose color based on liveness
        color = (0, 255, 0) if is_live else (0, 165, 255)  # Green if live, Orange if not verified
        
        # Draw rectangle
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        
        # Draw label
        liveness_status = "✓ LIVE" if is_live else "⚠ VERIFY"
        label = f"{student_id} ({confidence:.2%}) {liveness_status}"
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, label, (left + 6, bottom - 6), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        
        return frame

def process_student_images(student_id, name, email, phone, image_path):
    """
    Process student images and add to database
    image_path can be a single image or folder
    """
    fr_system = FaceRecognitionSystem()
    
    if os.path.isfile(image_path):
        # Single image
        encoding = fr_system.train_from_image(image_path, student_id)
    elif os.path.isdir(image_path):
        # Folder of images
        encoding = fr_system.train_from_folder(image_path, student_id)
    else:
        print(f"Invalid path: {image_path}")
        return False
    
    if encoding is None:
        print("Failed to process images - no face detected")
        return False
    
    # Add student to database
    success = Student.add_student(student_id, name, email, phone, image_path, encoding)
    
    if success:
        print(f"Student {student_id} - {name} added successfully!")
        return True
    else:
        print(f"Failed to add student {student_id} - may already exist")
        return False
