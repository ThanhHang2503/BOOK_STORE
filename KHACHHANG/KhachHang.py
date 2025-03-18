import pyodbc

class KhachHang:
    def __init__(self, connection_string):
        self.conn_str = connection_string
    
    def get_connection(self):
        return pyodbc.connect(self.conn_str)
    
    def load_data(self):
        query = "SELECT MaKH, TenKH, DiaChi, DienThoai FROM KhachHang"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [
                {"maKH": row.MaKH, "tenKH": row.TenKH, "diaChi": row.DiaChi, "dienThoai": row.DienThoai}
                for row in cursor.fetchall()
            ]
    
    def add_khachhang(self, maKH, tenKH, diaChi, dienThoai):
        query = """
        INSERT INTO KhachHang (MaKH, TenKH, DiaChi, DienThoai) 
        VALUES (?, ?, ?, ?)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (maKH, tenKH, diaChi, dienThoai))
            conn.commit()
        print("Thêm khách hàng thành công!")
    
    def update_khachhang(self, maKH, tenKH=None, diaChi=None, dienThoai=None):
        updates = []
        params = []
        if tenKH:
            updates.append("TenKH = ?")
            params.append(tenKH)
        if diaChi:
            updates.append("DiaChi = ?")
            params.append(diaChi)
        if dienThoai:
            updates.append("DienThoai = ?")
            params.append(dienThoai)
        
        if not updates:
            print("Không có thông tin nào để cập nhật.")
            return
        
        query = f"UPDATE KhachHang SET {', '.join(updates)} WHERE MaKH = ?"
        params.append(maKH)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        print("Cập nhật khách hàng thành công!")
    
    def delete_khachhang(self, maKH):
        query = "DELETE FROM KhachHang WHERE MaKH = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (maKH,))
            conn.commit()
        print("Xóa khách hàng thành công!")
    
    def search_khachhang(self, key):
        query = """
        SELECT MaKH, TenKH, DiaChi, DienThoai FROM KhachHang
        WHERE LOWER(TenKH) LIKE ? OR LOWER(MaKH) LIKE ? OR LOWER(DiaChi) LIKE ? OR LOWER(DienThoai) LIKE ?
        """
        key = f"%{key.lower()}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (key, key, key, key))
            return [
                {"maKH": row.MaKH, "tenKH": row.TenKH, "diaChi": row.DiaChi, "dienThoai": row.DienThoai}
                for row in cursor.fetchall()
            ]
    
    def display_khachhang(self):
        khachhang = self.load_data()
        if not khachhang:
            print("Danh sách rỗng!")
        else:
            print("\nDanh sách khách hàng:")
            print("=" * 70)
            for kh in khachhang:
                print(f"Mã KH: {kh['maKH']}, Tên: {kh['tenKH']}, Địa chỉ: {kh['diaChi']}, Điện thoại: {kh['dienThoai']}")
                print("-" * 70)

# Sử dụng
connection_string = "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=DOANPYTHON;Trusted_Connection=yes;"
kh = KhachHang(connection_string)
kh.display_khachhang()