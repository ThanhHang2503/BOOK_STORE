import pyodbc
from SANPHAM.SanPham import SanPham

class DSSanPham:
    def __init__(self):
        self.products = []
        self.conn = self.ket_noi_sql()

    def ket_noi_sql(self):
        """ Kết nối với SQL Server """
        try:
            conn = pyodbc.connect(
                "DRIVER={SQL Server};"
                "SERVER=LAPTOP-H2KMKBBS\\MSSQLSERVER01;"  # Thay bằng tên server của bạn
                "DATABASE=DOANPYTHON;"           # Thay bằng tên database của bạn
            )
            print("✅ Kết nối SQL thành công!")
            return conn
        except Exception as e:
            print(f"❌ Lỗi kết nối SQL: {e}")
            return None

    def lay_danh_sach_tu_sql(self):
        """ Lấy danh sách sản phẩm từ SQL Server """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM SanPham")
            rows = cursor.fetchall()

            self.products.clear()  # Xóa danh sách cũ
            for row in rows:
                sp = SanPham(*row)
                self.products.append(sp)

            print(f"✅ Đã tải {len(self.products)} sản phẩm từ SQL!")
        except Exception as e:
            print(f"❌ Lỗi khi lấy danh sách sản phẩm: {e}")

    def them_san_pham(self, san_pham):
        """ Thêm sản phẩm vào database """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO SanPham (maSP, tenSP, gia, soLuong) VALUES (?, ?, ?, ?)",
                (san_pham.maSP, san_pham.tenSP, san_pham.gia, san_pham.soLuong)
            )
            self.conn.commit()
            print("✅ Sản phẩm đã được thêm vào SQL!")
        except Exception as e:
            print(f"Lỗi thêm sản phẩm: {e}")

    def sua_thong_tin_san_pham(self, ma_sp, ten_moi, gia_moi, so_luong_moi):
        """ Sửa thông tin sản phẩm trong SQL """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE SanPham SET tenSP=?, gia=?, soLuong=? WHERE maSP=?",
                (ten_moi, gia_moi, so_luong_moi, ma_sp)
            )
            self.conn.commit()
            print("✅ Thông tin sản phẩm đã được cập nhật!")
        except Exception as e:
            print(f"Lỗi cập nhật sản phẩm: {e}")

    def hien_thi_danh_sach(self):
        """ Hiển thị danh sách sản phẩm """
        if not self.products:
            print("📌 Danh sách sản phẩm trống.")
        else:
            print("\n===== DANH SÁCH SẢN PHẨM =====")
            for sp in self.products:
                sp.xuat_thong_tin()  # Giả sử class SanPham có phương thức này
                print("--------------------")

    def tim_san_pham_theo_ma(self, ma_sp):
        """ Tìm kiếm sản phẩm theo mã trong SQL """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return None

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM SanPham WHERE maSP = ?", (ma_sp,))
            row = cursor.fetchone()

            if row:
                sp = SanPham(*row)
                print("\n Thông tin sản phẩm tìm thấy:")
                sp.xuat_thong_tin()
                return sp
            else:
                print("Không tìm thấy sản phẩm với mã này!")
                return None
        except Exception as e:
            print(f"Lỗi khi tìm sản phẩm: {e}")
            return None
