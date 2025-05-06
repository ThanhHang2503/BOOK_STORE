import pyodbc

from .HoaDon import HoaDon
from .utils import capNhatTongTien


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
                ngayTaoHD=row[3],
                tongTien=row[4]
            )
            dsach.append(nvien)
        return dsach

    def themHD(self, hd):
        """Thêm hóa đơn vào danh sách"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO HOADON (maHD, maNV, maKH, tongTien) VALUES (?, ?, ?, ?)",
                (hd.maHD, hd.maNV, hd.maKH, hd.tongTien))
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
            return HoaDon(row[0], row[1], row[2], row[3], row[4]) if row else None

        elif maKH:
            self.cursor.execute("SELECT * FROM HOADON WHERE maKH = ?", (maKH,))
            rows = self.cursor.fetchall()
            return [HoaDon(row[0], row[1], row[2], row[3], row[4]) for row in rows] if rows else None

        return None

    def sua(self, maHD, **kwargs):
        set_clause = ", ".join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values()) + [maHD]

        query = f"UPDATE HOADON SET {set_clause} WHERE maHD = ?"
        self.cursor.execute(query, values)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def xuat(self):
        """Xuất danh sách hóa đơn"""
        self.cursor.execute("SELECT * FROM HOADON")
        rows = self.cursor.fetchall()
        for row in rows:
            hd = HoaDon(row[0], row[1], row[2], row[3], row[4])
            hd.xuat()

    def dong_ket_noi(self):
        self.conn.close()

    def capNhatTongTien(self, maHD):
        """Cập nhật tổng tiền cho hóa đơn"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT thanhTien FROM CHITIETHD WHERE maHD = ?", (maHD,))
            rows = cursor.fetchall()
            tongTien = sum(row[0] for row in rows) if rows else 0

            cursor.execute("UPDATE HOADON SET tongTien = ? WHERE maHD = ?", (tongTien, maHD))
            self.conn.commit()

            # Cập nhật tổng tiền trong danh sách
            self.cursor.execute("SELECT tongTien FROM HOADON WHERE maHD = ?", (maHD,))
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute("UPDATE HOADON SET tongTien = ? WHERE maHD = ?", (tongTien, maHD))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật tổng tiền: {e}")
            return False
