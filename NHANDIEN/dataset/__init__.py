import base64
import os
from io import BytesIO

import cv2
import numpy as np
import pandas as pd
import requests


def tai_dataset():
    """
    Load sample face dataset for testing
    Returns:
        pandas.DataFrame: DataFrame containing sample face images
    """
    # Create sample images using OpenCV
    def create_sample_image():
        # Create a blank image
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        # Add some random noise to make it look like a face
        img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        # Convert to bytes
        _, img_encoded = cv2.imencode('.jpg', img)
        return base64.b64encode(img_encoded).decode('utf-8')
    
    # Sample data with locally generated images
    sample_data = {
        'name': ['Sample Person 1', 'Sample Person 2'],
        'image': [
            {'bytes': create_sample_image()},
            {'bytes': create_sample_image()}
        ]
    }
    
    return pd.DataFrame(sample_data) 