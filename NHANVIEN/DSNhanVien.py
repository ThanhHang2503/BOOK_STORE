import pyodbc

from NhanVien import NhanVien


class DSNhanVien:
    def __init__(self):
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-NRE55H1;"
            "DATABASE=DOANPYTHON;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()

    def danhSachNV(self):
        self.cursor.execute("SELECT * FROM NHANVIEN")
        rows = self.cursor.fetchall()

        dsach = []
        for row in rows:
            nvien = NhanVien(
                maNV=row[0],
                tenNV=row[1],
                chucVu=row[2],
                luong=row[3],
                diaChi=row[4],
                SĐT=row[5]
            )
            dsach.append(nvien)
        return dsach

    def themNV(self, nvien):
        try:
            self.cursor.execute(
                "INSERT INTO NHANVIEN (maNV, tenNV, chucVu, luong, diaChi, SĐT) VALUES (?, ?, ?, ?, ?, ?)",
                (nvien.maNV, nvien.tenNV, nvien.chucVu, nvien.luong, nvien.diaChi, nvien.SĐT)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False

    def xoaNV(self, maNV):
        """Xoa theo ma"""
        self.cursor.execute("DELETE FROM NHANVIEN WHERE maNV = ?", (maNV))
        self.conn.commit()

    def suaNV(self, maNV, **kwargs):  # **kwargs: truyen so luong tham so ko xac dinh
        set_clause = ", ".join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values()) + [maNV]

        query = f"UPDATE NHANVIEN SET {set_clause} WHERE maNV = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def timKiemNV(self, maNV=None, tenNV=None):
        if maNV:
            self.cursor.execute("SELECT * FROM NHANVIEN WHERE maNV = ?", (maNV,))
            row = self.cursor.fetchone()
            return [NhanVien(row[0], row[1], row[2], row[3], row[4], row[5])] if row else []

        elif tenNV:
            self.cursor.execute("SELECT * FROM NHANVIEN WHERE tenNV LIKE ?", ('%' + tenNV + '%',))
            rows = self.cursor.fetchall()
            return [NhanVien(row[0], row[1], row[2], row[3], row[4], row[5]) for row in rows]
        return []

    def xuatNV(self):
        """Xuất danh sách nhân viên"""
        self.cursor.execute("SELECT * FROM NHANVIEN")
        rows = self.cursor.fetchall()

        self.dsach = [
            NhanVien(maNV=row[0], tenNV=row[1], chucVu=row[2], luong=row[3], diaChi=row[4], SĐT=row[5])
            for row in rows
        ]

        return self.dsach

    def dongKetNoi(self):
        self.conn.close()
