import os

import cv2
import numpy as np
from tensorflow.keras.models import load_model

from NHANDIEN.models.face_embedding import FaceEmbeddingExtractor
from NHANDIEN.nhan_dien import capture_photo, process_face, verify_member


def test_model():
    """Test the face recognition system"""
    # Check if model exists
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'facenet_keras.h5')
    if not os.path.exists(model_path):
        print("Error: FaceNet model not found. Please run download_model.py first.")
        return
    
    try:
        # Test model loading
        print("Loading FaceNet model...")
        model = load_model(model_path)
        print("Model loaded successfully!")
        
        # Test face detection
        print("\nTesting face detection...")
        image = capture_photo()
        faces = detect_face(image)
        
        if len(faces) > 0:
            print(f"Face detected successfully! Found {len(faces)} face(s)")
            
            # Test face embedding
            print("\nTesting face embedding extraction...")
            face_image, face_embedding = process_face(image)
            
            if face_embedding is not None:
                print(f"Face embedding extracted successfully! Shape: {face_embedding.shape}")
                print(f"Sample embedding values: {face_embedding[:5]}")
                
                # Test member verification
                print("\nTesting member verification...")
                member_name, status = verify_member()
                print(f"Verification result: {status}")
                if member_name:
                    print(f"Member identified: {member_name}")
            else:
                print("Error: Could not extract face embedding")
        else:
            print("Error: No face detected in the image")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_model() 