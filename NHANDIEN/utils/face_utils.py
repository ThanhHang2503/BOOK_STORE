# face_utils.py
import base64
import io

import cv2
import numpy as np
from PIL import Image


def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    return faces

def crop_face(image, face):
    x, y, w, h = face
    return image[y:y+h, x:x+w]

def load_image_from_base64(base64_string):
    """Load an image from a base64 string"""
    # Decode base64 string
    img_bytes = base64.b64decode(base64_string)
    # Convert bytes to numpy array
    nparr = np.frombuffer(img_bytes, np.uint8)
    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

# Tải dữ liệu từ Hugging Face (nếu cần)
if __name__ == "__main__":
    from NHANDIEN.dataset import tai_dataset

    df = tai_dataset()
    print(df.head())

    # Lấy ảnh đầu tiên trong DataFrame
    img_base64 = df.iloc[0]['image']['bytes']

    # Load ảnh từ base64
    image = load_image_from_base64(img_base64)

    # Phát hiện khuôn mặt
    faces = detect_face(image)
    for face in faces:
        x, y, w, h = face
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Hiển thị ảnh
    cv2.imshow("Detected Face", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
