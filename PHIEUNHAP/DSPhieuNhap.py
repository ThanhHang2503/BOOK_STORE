import pyodbc

from .PhieuNhap import PhieuNhap
from .utils import capNhatTongTien


class DSPhieuNhap:

    def __init__(self):
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-NRE55H1;"
            "DATABASE=DOANPYTHON;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()

    def danhSachPN(self):
        self.cursor.execute("SELECT * FROM PHIEUNHAP")
        rows = self.cursor.fetchall()

        dsach = []
        for row in rows:
            nvien = PhieuNhap(
                maPN=row[0],
                maNV=row[2],
                ngayTaoPN=row[1],
                tongTien=row[3]
            )
            dsach.append(nvien)
        return dsach

    def themPN(self, PN):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO PHIEUNHAP (maPN, maNV, tongTien) VALUES (?, ?, ?)",
                (PN.maPN, PN.maNV, PN.tongTien))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi thêm phiếu nhập: {e}")
            return False

    def xoa(self, maPN):
        self.cursor.execute("DELETE FROM PHIEUNHAP WHERE maPN = ?", (maPN,))
        self.conn.commit()

    def timKiem(self, maPN=None, maNV=None):
        if maPN:
            self.cursor.execute("SELECT * FROM PHIEUNHAP WHERE maPN = ?", (maPN,))
            row = self.cursor.fetchone()
            return PhieuNhap(row[0], row[1], row[2], row[3]) if row else None

        elif maNV:
            self.cursor.execute("SELECT * FROM PHIEUNHAP WHERE maNV = ?", (maNV,))
            rows = self.cursor.fetchall()
            return [PhieuNhap(row[0], row[1], row[2], row[3]) for row in rows] if rows else None

        return None

    def sua(self, maPN, **kwargs):
        set_clause = ", ".join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values()) + [maPN]

        query = f"UPDATE PHIEUNHAP SET {set_clause} WHERE maPN = ?"
        self.cursor.execute(query, values)
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def xuat(self):
        self.cursor.execute("SELECT * FROM PHIEUNHAP")
        rows = self.cursor.fetchall()
        for row in rows:
            PN = PhieuNhap(row[0], row[1], row[2], row[3])
            PN.xuat()

    def dong_ket_noi(self):
        self.conn.close()

    def capNhatTongTien(self, maPN):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT thanhTien FROM CHITIETPN WHERE maPN = ?", (maPN,))
            rows = cursor.fetchall()
            tongTien = sum(row[0] for row in rows) if rows else 0

            cursor.execute("UPDATE PHIEUNHAP SET tongTien = ? WHERE maPN = ?", (tongTien, maPN))
            self.conn.commit()

            # Cập nhật tổng tiền trong danh sách
            self.cursor.execute("SELECT tongTien FROM PHIEUNHAP WHERE maPN = ?", (maPN,))
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute("UPDATE PHIEUNHAP SET tongTien = ? WHERE maPN = ?", (tongTien, maPN))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật tổng tiền: {e}")
            return False
