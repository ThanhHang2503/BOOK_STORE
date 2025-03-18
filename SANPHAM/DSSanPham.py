import pyodbc
from SanPham import SanPham

class DSSanPham:
    def __init__(self):
        # Danh sách chứa dữ liệu sản phẩm (lấy từ SQL)
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
        """Lấy dữ liệu sản phẩm từ bảng SanPham trong SQL Server."""
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        try:
            cursor = self.conn.cursor()
            query = "SELECT maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan FROM SanPham"
            cursor.execute(query)
            self.ds = []
            for row in cursor.fetchall():
                sp = {
                    "maSP": row[0],
                    "tenSP": row[1],
                    "soLuongTon": row[2],
                    "donGia": row[3],
                    "tacGia": row[4],
                    "nhaXuatBan": row[5]
                }
                self.ds.append(sp)
            cursor.close()
        except pyodbc.Error as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def add_sanpham(self, maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan):
        """Thêm sản phẩm mới vào cơ sở dữ liệu và danh sách nội bộ."""
        if any(sp["maSP"] == maSP for sp in self.ds):
            print("Mã sản phẩm đã tồn tại!")
            return
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO SanPham (maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan))
            self.conn.commit()
            cursor.close()
            # Cập nhật danh sách sau khi thêm
            self.ds.append({
                "maSP": maSP,
                "tenSP": tenSP,
                "soLuongTon": soLuongTon,
                "donGia": donGia,
                "tacGia": tacGia,
                "nhaXuatBan": nhaXuatBan
            })
            print("Thêm sản phẩm thành công!")
        except pyodbc.Error as e:
            print("Lỗi khi thêm sản phẩm:", e)
            self.conn.rollback()

    def update_sanpham(self, maSP):
        """Cập nhật thông tin sản phẩm theo mã sản phẩm."""
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        for sp in self.ds:
            if sp["maSP"] == maSP:
                print("\nChọn thông tin cần sửa:")
                print("1. Tên sản phẩm")
                print("2. Số lượng tồn")
                print("3. Đơn giá")
                print("4. Tác giả")
                print("5. Nhà xuất bản")
                option = input("Mời nhập lựa chọn: ")
                new_value = None
                col_name = None
                if option == "1":
                    new_value = input("Nhập tên sản phẩm mới: ")
                    col_name = "tenSP"
                elif option == "2":
                    new_value = input("Nhập số lượng tồn mới: ")
                    col_name = "soLuongTon"
                elif option == "3":
                    new_value = input("Nhập đơn giá mới: ")
                    col_name = "donGia"
                elif option == "4":
                    new_value = input("Nhập tên tác giả mới: ")
                    col_name = "tacGia"
                elif option == "5":
                    new_value = input("Nhập nhà xuất bản mới: ")
                    col_name = "nhaXuatBan"
                else:
                    print("Lựa chọn không hợp lệ. Không có thay đổi.")
                    return
                try:
                    cursor = self.conn.cursor()
                    query = f"UPDATE SanPham SET {col_name} = ? WHERE maSP = ?"
                    cursor.execute(query, (new_value, maSP))
                    self.conn.commit()
                    cursor.close()
                    # Cập nhật lại trong danh sách nội bộ
                    sp[col_name] = new_value
                    print("Sửa thông tin sản phẩm thành công!")
                except pyodbc.Error as e:
                    print("Lỗi khi cập nhật sản phẩm:", e)
                    self.conn.rollback()
                return
        print("Không tìm thấy sản phẩm!")

    def delete_sanpham(self, maSP):
        """Xóa sản phẩm khỏi cơ sở dữ liệu và danh sách nội bộ."""
        if self.conn is None:
            print("Không có kết nối đến CSDL.")
            return
        if any(sp["maSP"] == maSP for sp in self.ds):
            try:
                cursor = self.conn.cursor()
                query = "DELETE FROM SanPham WHERE maSP = ?"
                cursor.execute(query, (maSP,))
                self.conn.commit()
                cursor.close()
                # Cập nhật lại danh sách nội bộ
                self.ds = [sp for sp in self.ds if sp["maSP"] != maSP]
                print("Xóa sản phẩm thành công!")
            except pyodbc.Error as e:
                print("Lỗi khi xóa sản phẩm:", e)
                self.conn.rollback()
        else:
            print("Không tìm thấy sản phẩm!")

    def search_sanpham(self, key):
        """Tìm kiếm sản phẩm dựa trên key trong các trường maSP, tenSP, tacGia, nhaXuatBan."""
        key = key.lower()
        results = [sp for sp in self.ds if
                   key in sp.get("tenSP", "").lower() or 
                   key in sp.get("maSP", "").lower() or 
                   key in sp.get("tacGia", "").lower() or 
                   key in sp.get("nhaXuatBan", "").lower()]
        return results

    def display_sanpham(self):
        """Hiển thị danh sách sản phẩm."""
        if not self.ds:
            print("Danh sách rỗng!")
        else:
            print("\nDanh sách sản phẩm: ")
            print("=" * 90)
            for sp in self.ds:
                print(f"Mã SP: {sp['maSP']}, Tên: {sp['tenSP']}, "
                      f"Số lượng: {sp['soLuongTon']}, Giá: {sp['donGia']}, "
                      f"Tác giả: {sp['tacGia']}, Nhà xuất bản: {sp['nhaXuatBan']}")
                print("-" * 90)

# Ví dụ sử dụng:
if __name__ == '__main__':
    ds_sp = DSSanPham()
    # Lấy dữ liệu sản phẩm từ SQL Server
    ds_sp.load_data()
    ds_sp.display_sanpham()
    ds_sp.close_connection()