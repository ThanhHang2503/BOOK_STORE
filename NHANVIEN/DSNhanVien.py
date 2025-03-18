import pyodbc
from NHANVIEN.NhanVien import NhanVien

class DSNhanVien:
    def __init__(self):
        self.danh_sach = []
        self.conn = self.ket_noi_sql()

    def ket_noi_sql(self):
        """ Kết nối với SQL Server """
        try:
            conn = pyodbc.connect(
                "DRIVER={SQL Server};"
                "SERVER=localhost\SQLEXPRESS;"  # Thay bằng tên server của bạn
                "DATABASE=DOANPYTHON;"  # Thay bằng tên database của bạn
                "Trusted_Connection=yes;"
            )
            print("✅ Kết nối SQL thành công!")
            return conn
        except Exception as e:
            print(f"❌ Lỗi kết nối SQL: {e}")
            return None

    def lay_danh_sach_tu_sql(self):
        """ Lấy danh sách nhân viên từ SQL Server """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM NHANVIEN")
        rows = cursor.fetchall()

        self.danh_sach.clear()  # Xóa danh sách cũ
        for row in rows:
            nv = NhanVien(*row)
            self.danh_sach.append(nv)

        print(f"✅ Đã tải {len(self.danh_sach)} nhân viên từ SQL!")

    def them_nhan_vien(self, nhan_vien):
        """ Thêm nhân viên vào database """
        if not self.conn:
            print("❌ Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO NhanVien (maNV, tenNV, SĐT, luong , chucVu) VALUES (maNV, tenNV, sdt, luong, chucVu)",
                (nhan_vien.maNV, nhan_vien.tenNV, nhan_vien.ngaySinh, nhan_vien.chucVu, nhan_vien.luong, nhan_vien.diaChi, nhan_vien.soDT)
            )
            self.conn.commit()
            print("✅ Nhân viên đã được thêm vào SQL!")
        except Exception as e:
            print(f" Lỗi thêm nhân viên: {e}")

    def sua_thong_tin_nhan_vien(self, ma_nv, ten_moi, chuc_vu_moi, luong_moi, dia_chi_moi, so_dt_moi):
        """ Sửa thông tin nhân viên trong SQL """
        if not self.conn:
            print(" Không thể kết nối SQL.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE NhanVien SET tenNV=?, chucVu=?, luong=?, diaChi=?, soDT=? WHERE maNV=?",
                (ten_moi, chuc_vu_moi, luong_moi, dia_chi_moi, so_dt_moi, ma_nv)
            )
            self.conn.commit()
            print(" Thông tin nhân viên đã được cập nhật!")
        except Exception as e:
            print(f"Lỗi cập nhật nhân viên: {e}")

    def hien_thi_danh_sach(self):
     
        if not self.danh_sach:
            print("📌 Danh sách nhân viên trống.")
        else:
            print("\n===== DANH SÁCH NHÂN VIÊN =====")
        for nv in self.danh_sach:
            nv.xuat_thong_tin()
            print("--------------------")

    def tim_nhan_vien_theo_ma(self, ma_nv):
        """ Tìm kiếm nhân viên trong SQL """
        if not self.conn:
            print(" Không thể kết nối SQL.")
            return None

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM NhanVien WHERE maNV = ?", (ma_nv,))
        row = cursor.fetchone()

        if row:
            nv = NhanVien(*row)
            print("\n Thông tin nhân viên tìm thấy:")
            nv.xuat_thong_tin()
            return nv
        else:
            print("Không tìm thấy nhân viên với mã này!")
            return None






def main():
    ds = DSNhanVien()

    while True:
        print("\n===== QUẢN LÝ NHÂN VIÊN =====")
        print("1. Lấy danh sách nhân viên từ SQL")
        print("2. Hiển thị danh sách nhân viên")
        print("3. Thêm nhân viên mới")
        print("4. Sửa thông tin nhân viên")
        print("5. Tìm kiếm nhân viên theo mã")
        print("0. Thoát")
        lua_chon = input("Nhập lựa chọn: ")

        if lua_chon == "1":
            ds.lay_danh_sach_tu_sql()
            print("✅ Danh sách nhân viên đã được cập nhật từ SQL!")

        elif lua_chon == "2":
            ds.hien_thi_danh_sach()

        elif lua_chon == "3":
            maNV = input("Nhập mã nhân viên: ")
            tenNV = input("Nhập tên nhân viên: ")
            ngaySinh = input("Nhập ngày sinh (YYYY-MM-DD): ")
            chucVu = input("Nhập chức vụ: ")
            luong = float(input("Nhập lương: "))
            diaChi = input("Nhập địa chỉ: ")
            soDT = input("Nhập số điện thoại: ")

            nv_moi = NhanVien(maNV, tenNV, ngaySinh, chucVu, luong, diaChi, soDT)
            ds.them_nhan_vien(nv_moi)

        elif lua_chon == "4":
            maNV = input("Nhập mã nhân viên cần sửa: ")
            ten_moi = input("Nhập tên mới: ")
            chuc_vu_moi = input("Nhập chức vụ mới: ")
            luong_moi = float(input("Nhập lương mới: "))
            dia_chi_moi = input("Nhập địa chỉ mới: ")
            so_dt_moi = input("Nhập số điện thoại mới: ")

            ds.sua_thong_tin_nhan_vien(maNV, ten_moi, chuc_vu_moi, luong_moi, dia_chi_moi, so_dt_moi)

        elif lua_chon == "5":
            maNV = input("Nhập mã nhân viên cần tìm: ")
            ds.tim_nhan_vien_theo_ma(maNV)

        elif lua_chon == "0":
            print("Thoát chương trình!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ. Vui lòng nhập lại!")

if __name__ == "__main__":
    main()