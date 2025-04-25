import os

import cv2
import numpy as np

from NHANDIEN.utils.config import (CAMERA_INDEX, FACE_DETECTION_MIN_NEIGHBORS,
                             FACE_DETECTION_SCALE_FACTOR)
from NHANDIEN.utils.db_utils import find_matching_member
from NHANDIEN.utils.face_utils import crop_face, detect_face
from NHANDIEN.models.face_embedding import FaceEmbeddingExtractor

# Initialize face embedding extractor
face_embedding_extractor = FaceEmbeddingExtractor()

def capture_photo():
    """Capture a photo from the camera"""
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise Exception("Could not open camera")
    
    # Allow camera to warm up
    for _ in range(5):
        cap.read()
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception("Could not capture photo")
    
    return frame

def process_face(image):
    """Process the captured image to detect and extract face"""
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = detect_face(gray)
    if len(faces) == 0:
        return None, None
    
    # For simplicity, we'll use the first detected face
    face = faces[0]
    face_image = crop_face(image, face)
    
    try:
        # Extract face embedding using OpenCV
        face_embedding = face_embedding_extractor.get_embedding(face_image)
        return face_image, face_embedding
    except Exception as e:
        print(f"Error extracting face embedding: {str(e)}")
        return None, None

def verify_member():
    """Main function to verify if a person is a registered member"""
    try:
        # Capture photo
        print("Capturing photo...")
        image = capture_photo()
        
        # Process face
        print("Processing face...")
        face_image, face_embedding = process_face(image)
        if face_image is None:
            return None, "No face detected"
        
        # Find matching member
        print("Verifying member...")
        member_name = find_matching_member(face_embedding)
        if member_name:
            return member_name, "Member verified"
        else:
            return None, "Not a registered member"
            
    except Exception as e:
        return None, f"Error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    member_name, status = verify_member()
    if member_name:
        print(f"Welcome {member_name}! Status: {status}")
    else:
        print(f"Status: {status}")
