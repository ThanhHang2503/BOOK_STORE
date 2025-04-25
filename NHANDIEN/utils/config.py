import os

# Database configuration
DB_PATH = "members.db"

# Face detection settings
FACE_DETECTION_SCALE_FACTOR = 1.3
FACE_DETECTION_MIN_NEIGHBORS = 5

# Camera settings
CAMERA_INDEX = 0  # Default camera index

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
