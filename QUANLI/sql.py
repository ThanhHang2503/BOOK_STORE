import pyodbc

server = 'localhost\SQLEXPRESS'  # server
database = 'DOANPYTHON'  # tên database
trusted_connection = True  # Dùng Windows Authentication

# Chuỗi kết nối
conn_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};"
if trusted_connection:
    conn_string += "Trusted_Connection=yes;"
else:
    conn_string += "UID=your_username;PWD=your_password;"

# Kết nối đến SQL Server
try:
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()
    
    # Kiểm tra kết nối
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("Connected to:", row[0])

    cursor.execute("SELECT * FROM chitiethd")
    rows = cursor.fetchall()  # Lấy toàn bộ dữ liệu

    # Hiển thị dữ liệu
    if rows:
        for row in rows:
            print(row)  # In cả dòng
            # print(row[0], row[1], row[2])  # Hoặc lấy từng cột cụ thể nếu cần
    else:
        print("Không có dữ liệu trong bảng HOADON.")
    conn.close()
except Exception as e:
    print("Lỗi khi kết nối SQL Server:", e)
