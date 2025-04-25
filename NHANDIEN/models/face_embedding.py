import cv2
import numpy as np


class FaceEmbeddingExtractor:
    def __init__(self):
        """
        Initialize the face embedding extractor using basic image features
        """
        self.input_size = (160, 160)  # Standard face size

    def preprocess_face(self, face_image):
        """
        Preprocess the face image
        Args:
            face_image: Cropped face image
        Returns:
            Preprocessed image
        """
        # Resize to standard size
        face_image = cv2.resize(face_image, self.input_size)
        # Convert to grayscale
        if len(face_image.shape)==3:
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        return face_image

    def get_embedding(self, face_image):
        """
        Extract face features using basic image processing
        Args:
            face_image: Cropped face image
        Returns:
            Face features as numpy array
        """
        # Preprocess the face
        processed_face = self.preprocess_face(face_image)
        
        # Extract features using multiple methods
        features = []
        
        # 1. Histogram of Oriented Gradients (HOG)
        hog = cv2.HOGDescriptor()
        hog_features = hog.compute(processed_face)
        features.extend(hog_features.flatten())
        
        # 2. Local Binary Patterns (LBP)
        lbp = cv2.calcHist([processed_face], [0], None, [256], [0, 256])
        features.extend(lbp.flatten())
        
        # 3. Basic image statistics
        mean = np.mean(processed_face)
        std = np.std(processed_face)
        features.extend([mean, std])
        
        # Convert to numpy array and normalize
        features = np.array(features, dtype=np.float32)
        features = cv2.normalize(features, None, 0, 1, cv2.NORM_MINMAX)
        
        return features