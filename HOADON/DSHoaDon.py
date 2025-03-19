import pyodbc

from HoaDon import HoaDon


class DSHoaDon:

    def __init__(self):
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-NRE55H1;"
            "DATABASE=DOANPYTHON;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()

    def danhSachHD(self):
        self.cursor.execute("SELECT * FROM HOADON")
        rows = self.cursor.fetchall()

        dsach = []
        for row in rows:
            nvien = HoaDon(
                maHD=row[0],
                maNV=row[1],
                maKH=row[2],
                tongTien=row[4],
                ngayTaoHD=row[3]
            )
            dsach.append(nvien)
        return dsach

    def them(self, hd):
        """Thêm hóa đơn vào cơ sở dữ liệu"""
        try:
            self.cursor.execute(
                "INSERT INTO HOADON (maHD, maNV, maKH, tongTien, ngayTaoHD) VALUES (?, ?, ?, ?, ?)",
                (hd.maHD, hd.maNV, hd.maKH, hd.tongTien, hd.ngayTaoHD)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm hóa đơn: {e}")
            return False

    def xoa(self, maHD):
        """Xóa hóa đơn theo mã"""
        self.cursor.execute("DELETE FROM HOADON WHERE maHD = ?", (maHD,))
        self.conn.commit()

    def timKiem(self, maHD=None, maKH=None):
        if maHD:
            self.cursor.execute("SELECT * FROM HOADON WHERE maHD = ?", (maHD,))
            row = self.cursor.fetchone()
            return HoaDon(row[0], row[1], row[2], row[4], row[3]) if row else None  # Trả về đối tượng trực tiếp

        elif maKH:
            self.cursor.execute("SELECT * FROM HOADON WHERE maKH = ?", (maKH,))
            row = self.cursor.fetchone()
            return HoaDon(row[0], row[1], row[2], row[4], row[3]) if row else None

        return None

    def sua(self, maHD, **kwargs):
        set_clause = ", ".join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values()) + [maHD]

        query = f"UPDATE HOADON SET {set_clause} WHERE maHD = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def xuat(self):
        """Xuất danh sách hóa đơn"""
        self.cursor.execute("SELECT * FROM HOADON")
        rows = self.cursor.fetchall()
        for row in rows:
            hd = HoaDon(row[0], row[1], row[2], [], row[3], row[4])
            hd.xuat()

    def dong_ket_noi(self):
        self.conn.close()
