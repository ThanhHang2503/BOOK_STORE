# face_utils.py
import io

import cv2
from PIL import Image
import numpy as np

def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, 1.3, 5)
    return faces

def crop_face(image, face):
    x, y, w, h = face
    return image[y:y+h, x:x+w]

# Tải dữ liệu từ Hugging Face (nếu cần)
if __name__ == "__main__":
    from NHANDIEN.dataset import tai_dataset

    df = tai_dataset()
    print(df.head())

    # Lấy ảnh đầu tiên trong DataFrame
    img_bytes = df.iloc[0]['image']['bytes']

    # Chuyển bytes thành ảnh OpenCV
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Phát hiện khuôn mặt
    faces = detect_face(image)
    for face in faces:
        x, y, w, h = face
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Hiển thị ảnh
    cv2.imshow("Detected Face", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
