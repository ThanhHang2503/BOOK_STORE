import sqlite3

import numpy as np

from NHANDIEN.utils.config import DB_PATH


def init_db():
    """Initialize the database with necessary tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create members table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS THANHVIEN (
        ma INTEGER PRIMARY KEY AUTOINCREMENT,
        hoten TEXT NOT NULL,
        face_embedding BLOB NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_member(hoten, face_embedding):
    """Add a new member to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert numpy array to bytes
    face_bytes = face_embedding.tobytes()
    
    cursor.execute(
        "INSERT INTO members (hoten, face_embedding) VALUES (?, ?)",
        (hoten, face_bytes)
    )
    
    conn.commit()
    conn.close()

def get_all_members():
    """Retrieve all members from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT ma, hoten, face_embedding FROM members")
    members = []
    
    for row in cursor.fetchall():
        ma, hoten, face_bytes = row
        face_embedding = np.frombuffer(face_bytes, dtype=np.float32)
        members.append((ma, hoten, face_embedding))
    
    conn.close()
    return members

def find_matching_member(face_embedding, threshold=0.6):
    """Find the best matching member for a given face embedding"""
    members = get_all_members()
    if not members:
        return None
    
    best_match = None
    best_score = float('inf')
    
    for ma, hoten, member_embedding in members:
        # Calculate Euclidean distance between embeddings
        distance = np.linalg.norm(face_embedding - member_embedding)
        if distance < best_score:
            best_score = distance
            best_match = (ma, hoten, distance)
    
    # Return match if it's below threshold
    if best_match and best_match[2] < threshold:
        return best_match[1]  # Return member name
    return None
