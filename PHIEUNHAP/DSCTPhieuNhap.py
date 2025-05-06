import pyodbc

from .ChiTietPN import ChiTietPN
from .utils import capNhatTongTien


class DSCTPhieuNhap:
    def __init__(self):
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-NRE55H1;"
            "DATABASE=DOANPYTHON;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()

    def them(self, chitiet):
        try:
            # Tính thành tiền
            thanh_tien = chitiet.soLuongSP * chitiet.donGia

            self.cursor.execute(
                "INSERT INTO CHITIETPN (maPN, maSP, soLuongSP, donGia, thanhTien) VALUES (?, ?, ?, ?, ?)",
                (chitiet.maPN, chitiet.maSP, chitiet.soLuongSP, chitiet.donGia, thanh_tien)
            )
            self.conn.commit()

            # Cập nhật tổng tiền của hóa đơn
            self.cursor.execute("SELECT SUM(thanhTien) FROM CHITIETPN WHERE maPN = ?", (chitiet.maPN,))
            tong_tien = self.cursor.fetchone()[0] or 0
            self.cursor.execute("UPDATE PHIEUNHAP SET tongTien = ? WHERE maPN = ?", (tong_tien, chitiet.maPN))
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Lỗi khi thêm chi tiết hóa đơn: {e}")
            return False

    def xoa(self, maPN, maSP):
        try:
            self.cursor.execute("DELETE FROM CHITIETPN WHERE maPN = ? AND maSP = ?", (maPN, maSP))
            self.conn.commit()

            # Cập nhật tổng tiền của hóa đơn
            capNhatTongTien(maPN, self.cursor)

            return True
        except Exception as e:
            print(f"Lỗi khi xóa chi tiết hóa đơn: {e}")
            return False

    def timKiem(self, maPN=None, maSP=None):
        try:
            if maPN:
                self.cursor.execute("SELECT * FROM CHITIETPN WHERE maPN = ?", (maPN,))
                rows = self.cursor.fetchall()
                return [ChiTietPN(row[0], row[1], row[2], row[3]) for row in rows]

            elif maSP:
                self.cursor.execute("SELECT * FROM CHITIETPN WHERE maSP = ?", (maSP,))
                rows = self.cursor.fetchall()
                return [ChiTietPN(row[0], row[1], row[2], row[3]) for row in rows]
            return []
        except Exception as e:
            print(f"Lỗi khi tìm kiếm chi tiết hóa đơn: {e}")
            return []


    def sua(self, maPN, maSP, soLuongSP=None, donGia=None):
        """Cập nhật thông tin chi tiết hóa đơn"""
        try:
            # Lấy thông tin chi tiết hiện tại
            self.cursor.execute(
                "SELECT * FROM CHITIETPN WHERE maPN = ? AND maSP = ?",
                (maPN, maSP)
            )
            row = self.cursor.fetchone()
            if not row:
                return False

            # Sử dụng giá trị hiện tại nếu không được cập nhật
            current_soLuongSP = row[2] if soLuongSP is None else soLuongSP
            current_donGia = row[3] if donGia is None else donGia
            current_thanhTien = current_soLuongSP * current_donGia

            # Cập nhật thông tin
            self.cursor.execute(
                "UPDATE CHITIETPN SET soLuongSP = ?, donGia = ?, thanhTien = ? WHERE maPN = ? AND maSP = ?",
                (current_soLuongSP, current_donGia, current_thanhTien, maPN, maSP)
            )
            self.conn.commit()

            # Cập nhật tổng tiền của hóa đơn
            self.cursor.execute("SELECT SUM(thanhTien) FROM CHITIETPN WHERE maPN = ?", (maPN,))
            tong_tien = self.cursor.fetchone()[0] or 0
            self.cursor.execute("UPDATE PHIEUNHAP SET tongTien = ? WHERE maPN = ?", (tong_tien, maPN))
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật chi tiết hóa đơn: {e}")
            return False

    def xuat(self):
        self.cursor.execute("SELECT * FROM CHITIETPN")
        rows = self.cursor.fetchall()
        for row in rows:
            ct = ChiTietPN(row[0], row[1], row[2], row[3])
            ct.xuat()
            print("-" * 80)

    def dong_ket_noi(self):
        self.conn.close()
