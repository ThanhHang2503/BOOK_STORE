import cv2

cap = cv2.VideoCapture(0)  # 0 là camera mặc định

while True:
    ret, frame = cap.read()  # Đọc hình ảnh từ camera
    if not ret:
        break

    cv2.imshow('Camera', frame)  # Hiển thị khung hình

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Nhấn 'q' để thoát
        break

cap.release()
cv2.destroyAllWindows()
