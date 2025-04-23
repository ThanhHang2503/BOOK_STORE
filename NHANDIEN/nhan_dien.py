import cv2
import numpy as np

from NHANDIEN.config import (CAMERA_INDEX, FACE_DETECTION_MIN_NEIGHBORS,
                             FACE_DETECTION_SCALE_FACTOR)
from NHANDIEN.db_utils import find_matching_member
from NHANDIEN.face_utils import crop_face, detect_face


def capture_photo():
    """Capture a photo from the camera"""
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise Exception("Could not open camera")
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception("Could not capture photo")
    
    return frame

def process_face(image):
    """Process the captured image to detect and extract face"""
    faces = detect_face(image)
    if len(faces) == 0:
        return None, None
    
    # For simplicity, we'll use the first detected face
    face = faces[0]
    face_image = crop_face(image, face)
    
    # TODO: Add face embedding extraction here
    # For now, we'll return a dummy embedding
    face_embedding = np.random.rand(128)  # Replace with actual face embedding
    
    return face_image, face_embedding

def verify_member():
    """Main function to verify if a person is a registered member"""
    try:
        # Capture photo
        image = capture_photo()
        
        # Process face
        face_image, face_embedding = process_face(image)
        if face_image is None:
            return None, "No face detected"
        
        # Find matching member
        member_name = find_matching_member(face_embedding)
        if member_name:
            return member_name, "Member"
        else:
            return None, "Not a member"
            
    except Exception as e:
        return None, f"Error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    member_name, status = verify_member()
    if member_name:
        print(f"Welcome {member_name}! Status: {status}")
    else:
        print(f"Status: {status}")
