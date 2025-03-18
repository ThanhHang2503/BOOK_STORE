import pyodbc
from KhachHang import KhachHang
class DSKhachHang:
    def __init__(self):
        # Danh sách chứa dữ liệu khách hàng (lấy từ SQL)
        self.ds = []
        # Kết nối đến cơ sở dữ liệu SQL Server
        self.conn = self.connect_db()

    def connect_db(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};'
                'SERVER=localhost\\SQLEXPRESS;'
                'DATABASE=DOANPYTHON;'
                'Trusted_Connection=yes;'
            )
            return conn
        except pyodbc.Error as e:
            print("Lỗi kết nối CSDL:", e)
            return None

    def close_connection(self):
        """Đóng kết nối đến CSDL khi không sử dụng."""
        if self.conn is not None:
            try:
                self.conn.close()
                print("Đã đóng kết nối CSDL.")
            except pyodbc.Error as e:
                print("Lỗi khi đóng kết nối CSDL:", e)

    def load_data(self):
        """Lấy dữ liệu khách hàng từ bảng KhachHang trong SQL Server."""
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        try:
            cursor = self.conn.cursor()
            query = "SELECT maKH, tenKH, diaChi, dienThoai FROM KhachHang"
            cursor.execute(query)
            self.ds = []
            for row in cursor.fetchall():
                kh = {
                    "maKH": row[0],
                    "tenKH": row[1],
                    "diaChi": row[2],
                    "dienThoai": row[3]
                }
                self.ds.append(kh)
            cursor.close()
        except pyodbc.Error as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def add_khachhang(self, maKH, tenKH, diaChi, dienThoai):
        """Thêm khách hàng mới vào cơ sở dữ liệu và danh sách nội bộ."""
        if any(kh["maKH"] == maKH for kh in self.ds):
            print("Mã khách hàng đã tồn tại!")
            return
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO KhachHang (maKH, tenKH, diaChi, dienThoai) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (maKH, tenKH, diaChi, dienThoai))
            self.conn.commit()
            cursor.close()
            # Cập nhật danh sách sau khi thêm
            self.ds.append({
                "maKH": maKH,
                "tenKH": tenKH,
                "diaChi": diaChi,
                "dienThoai": dienThoai
            })
            print("Thêm khách hàng thành công!")
        except pyodbc.Error as e:
            print("Lỗi khi thêm khách hàng:", e)
            self.conn.rollback()

    def update_khachhang(self, maKH):
        """Cập nhật thông tin khách hàng theo mã khách hàng."""
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        for kh in self.ds:
            if kh["maKH"] == maKH:
                print("\nChọn thông tin cần sửa:")
                print("1. Họ tên")
                print("2. Địa chỉ")
                print("3. Điện thoại")
                option = input("Mời nhập lựa chọn: ")
                new_value = None
                col_name = None
                if option == "1":
                    new_value = input("Nhập họ tên mới: ")
                    col_name = "tenKH"
                elif option == "2":
                    new_value = input("Nhập địa chỉ mới: ")
                    col_name = "diaChi"
                elif option == "3":
                    new_value = input("Nhập số điện thoại mới: ")
                    col_name = "dienThoai"
                else:
                    print("Lựa chọn không hợp lệ. Không có thay đổi.")
                    return
                try:
                    cursor = self.conn.cursor()
                    query = f"UPDATE KhachHang SET {col_name} = ? WHERE maKH = ?"
                    cursor.execute(query, (new_value, maKH))
                    self.conn.commit()
                    cursor.close()
                    # Cập nhật lại trong danh sách nội bộ
                    kh[col_name] = new_value
                    print("Sửa thông tin khách hàng thành công!")
                except pyodbc.Error as e:
                    print("Lỗi khi cập nhật khách hàng:", e)
                    self.conn.rollback()
                return
        print("Không tìm thấy khách hàng!")

    def delete_khachhang(self, maKH):
        """Xóa khách hàng khỏi cơ sở dữ liệu và danh sách nội bộ."""
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        if any(kh["maKH"] == maKH for kh in self.ds):
            try:
                cursor = self.conn.cursor()
                query = "DELETE FROM KhachHang WHERE maKH = ?"
                cursor.execute(query, (maKH,))
                self.conn.commit()
                cursor.close()
                # Cập nhật lại danh sách nội bộ
                self.ds = [kh for kh in self.ds if kh["maKH"] != maKH]
                print("Xóa khách hàng thành công!")
            except pyodbc.Error as e:
                print("Lỗi khi xóa khách hàng:", e)
                self.conn.rollback()
        else:
            print("Không tìm thấy khách hàng!")

    def search_khachhang(self, key):
        """Tìm kiếm khách hàng dựa trên key trong các trường maKH, tenKH, diaChi, dienThoai."""
        key = key.lower()
        results = [kh for kh in self.ds if
                   key in kh.get("tenKH", "").lower() or 
                   key in kh.get("maKH", "").lower() or 
                   key in kh.get("diaChi", "").lower() or 
                   key in kh.get("dienThoai", "").lower()]
        return results

    def display_khachhang(self):
        """Hiển thị danh sách khách hàng."""
        if not self.ds:
            print("Danh sách rỗng!")
        else:
            print("\nDanh sách khách hàng: ")
            print("=" * 70)
            for kh in self.ds:
                print(f"Mã KH: {kh['maKH']}, Tên: {kh['tenKH']}, "
                      f"Địa chỉ: {kh.get('diaChi', 'Không có')}, "
                      f"Điện thoại: {kh.get('dienThoai', 'Không có')}")
                print("-" * 70)

# Ví dụ sử dụng:
if __name__ == '__main__':
    ds_kh = DSKhachHang()
    # Lấy dữ liệu khách hàng từ SQL Server
    ds_kh.load_data()
    ds_kh.display_khachhang()
    ds_kh.close_connection()