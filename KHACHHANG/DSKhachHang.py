import pyodbc
from KHACHHANG.KhachHang import KhachHang

class DSKhachHang:
    def __init__(self):
        self.customers = []
        self.conn = self.ket_noi_sql()

    def ket_noi_sql(self):
        """ Kết nối với SQL Server """
        try:
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=DESKTOP-NRE55H1;"
                "DATABASE=DOANPYTHON;"
                "Trusted_Connection=yes;"
            )

            print("✅ Kết nối SQL thành công!")
            return conn
        except Exception as e:
            print(f"❌ Lỗi kết nối SQL: {e}")
            return None

    def lay_danh_sach_tu_sql(self):
        """ Lấy danh sách khách hàng từ SQL Server """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM KhachHang")
            rows = cursor.fetchall()

            self.customers.clear()  # Xóa danh sách cũ
            for row in rows:
                kh = KhachHang(*row)
                self.customers.append(kh)

            print(f"✅ Đã tải {len(self.customers)} khách hàng từ SQL!")
        except Exception as e:
            print(f"❌ Lỗi khi lấy danh sách khách hàng: {e}")

    def them_khach_hang(self, khach_hang):
        """ Thêm khách hàng vào database """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO KhachHang (maKH, tenKH, diaChi, dienThoai) VALUES (?, ?, ?, ?)",
                (khach_hang.maKH, khach_hang.tenKH, khach_hang.diaChi, khach_hang.dienThoai)
            )
            self.conn.commit()
            print("✅ Khách hàng đã được thêm vào SQL!")
        except Exception as e:
            print(f"Lỗi thêm khách hàng: {e}")

    def sua_thong_tin_khach_hang(self, ma_kh, ten_moi, dia_chi_moi, dien_thoai_moi):
        """ Sửa thông tin khách hàng trong SQL """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE KhachHang SET tenKH=?, diaChi=?, dienThoai=? WHERE maKH=?",
                (ten_moi, dia_chi_moi, dien_thoai_moi, ma_kh)
            )
            self.conn.commit()
            print("✅ Thông tin khách hàng đã được cập nhật!")
        except Exception as e:
            print(f"Lỗi cập nhật khách hàng: {e}")

    def hien_thi_danh_sach(self):
        """ Hiển thị danh sách khách hàng """
        if not self.customers:
            print("📌 Danh sách khách hàng trống.")
        else:
            print("\n===== DANH SÁCH KHÁCH HÀNG =====")
            for kh in self.customers:
                kh.xuat_thong_tin()  # Giả sử class KhachHang có phương thức này
                print("--------------------")

    def tim_khach_hang_theo_ma(self, ma_kh):
        """ Tìm kiếm khách hàng theo mã trong SQL """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return None

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM KhachHang WHERE maKH = ?", (ma_kh,))
            row = cursor.fetchone()

            if row:
                kh = KhachHang(*row)
                print("\n Thông tin khách hàng tìm thấy:")
                kh.xuat_thong_tin()
                return kh
            else:
                print("Không tìm thấy khách hàng với mã này!")
                return None
        except Exception as e:
            print(f"Lỗi khi tìm khách hàng: {e}")
            return None

# Ví dụ chương trình điều khiển cho DSKhachHang
def main():
    ds_kh = DSKhachHang()

    while True:
        print("\n===== QUẢN LÝ KHÁCH HÀNG =====")
        print("1. Lấy danh sách khách hàng từ SQL")
        print("2. Hiển thị danh sách khách hàng")
        print("3. Thêm khách hàng mới")
        print("4. Sửa thông tin khách hàng")
        print("5. Tìm kiếm khách hàng theo mã")
        print("0. Thoát")
        lua_chon = input("Nhập lựa chọn: ")

        if lua_chon == "1":
            ds_kh.lay_danh_sach_tu_sql()
        elif lua_chon == "2":
            ds_kh.hien_thi_danh_sach()
        elif lua_chon == "3":
            maKH = input("Nhập mã khách hàng: ")
            tenKH = input("Nhập tên khách hàng: ")
            diaChi = input("Nhập địa chỉ: ")
            dienThoai = input("Nhập số điện thoại: ")
            kh_moi = KhachHang(maKH, tenKH, diaChi, dienThoai)
            ds_kh.them_khach_hang(kh_moi)
        elif lua_chon == "4":
            maKH = input("Nhập mã khách hàng cần sửa: ")
            ten_moi = input("Nhập tên mới: ")
            dia_chi_moi = input("Nhập địa chỉ mới: ")
            dien_thoai_moi = input("Nhập số điện thoại mới: ")
            ds_kh.sua_thong_tin_khach_hang(maKH, ten_moi, dia_chi_moi, dien_thoai_moi)
        elif lua_chon == "5":
            maKH = input("Nhập mã khách hàng cần tìm: ")
            ds_kh.tim_khach_hang_theo_ma(maKH)
        elif lua_chon == "0":
            print("Thoát chương trình!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ. Vui lòng nhập lại!")