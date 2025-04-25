import pyodbc

from .ChiTietHD import ChiTietHD


class DSCTHoaDon:
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
            self.cursor.execute(
                "INSERT INTO CHITIETHD (maHD, maSP, soLuongSP, donGia, thanhTien) VALUES (?, ?, ?, ?, ?)",
                (chitiet.maHD, chitiet.maSP, chitiet.soLuongSP, chitiet.donGia, chitiet.thanhTien)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm chi tiết hóa đơn: {e}")
            return False

    def xoa(self, maHD, maSP):
        try:
            self.cursor.execute("DELETE FROM CHITIETHD WHERE maHD = ? AND maSP = ?", (maHD, maSP))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi xóa chi tiết hóa đơn: {e}")
            return False

    def timKiem(self, maHD=None, maSP=None):

        if maHD:
            self.cursor.execute("SELECT * FROM CHITIETHD WHERE maHD = ?", (maHD,))
            row = self.cursor.fetchone()
            return [ChiTietHD(row[0], row[1], row[2], row[3])] if row else []

        elif maSP:
            self.cursor.execute("SELECT * FROM CHITIETHD WHERE maKH = ?", (maSP,))
            row = self.cursor.fetchone()
            return [ChiTietHD(row[0], row[1], row[2], row[3])] if row else []
        return []

    def xuat(self):
        self.cursor.execute("SELECT * FROM CHITIETHD")
        rows = self.cursor.fetchall()
        for row in rows:
            ct = ChiTietHD(row[0], row[1], row[2], row[3])
            ct.xuat()
            print("-" * 80)

    def dong_ket_noi(self):
        self.conn.close()
