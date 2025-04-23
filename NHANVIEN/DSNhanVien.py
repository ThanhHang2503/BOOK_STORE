import sys
from tkinter import messagebox

import pyodbc

from .NhanVien import NhanVien


class DSNhanVien:
    def __init__(self):
        try:
            # Try to connect to the database
            self.conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=DESKTOP-NRE55H1;"
                "DATABASE=DOANPYTHON;"
                "Trusted_Connection=yes;"
                "Connection Timeout=30;"  # Increase timeout to 30 seconds
            )
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            error_message = f"Không thể kết nối đến cơ sở dữ liệu:\n{str(e)}\n\n"
            error_message += "Vui lòng kiểm tra:\n"
            error_message += "1. SQL Server đã được cài đặt và đang chạy\n"
            error_message += "2. Tên máy chủ (SERVER) trong kết nối là chính xác\n"
            error_message += "3. Cơ sở dữ liệu DOANPYTHON đã tồn tại\n"
            error_message += "4. ODBC Driver 17 for SQL Server đã được cài đặt"
            
            # Show error message in a message box
            messagebox.showerror("Lỗi kết nối cơ sở dữ liệu", error_message)
            sys.exit(1)  # Exit the application with error code 1

    def danhSachNV(self):
        self.cursor.execute("SELECT * FROM NHANVIEN")
        rows = self.cursor.fetchall()

        dsach = []
        for row in rows:
            nvien = NhanVien(
                maNV=row[0],
                tenNV=row[1],
                diaChi=row[2], # sửa ở đây
                SĐT=row[3], # sửa ở đây
                luong=row[4], # sửa ở đây
                chucVu=row[5], # sửa ở đây
                trangThai=row[6] # sửa ở đây
            )
            dsach.append(nvien)
        return dsach

    def themNV(self, nvien):
        try:
            self.cursor.execute(
                "INSERT INTO NHANVIEN (maNV, tenNV, diaChi, SĐT, luong, chucVu, trangThai) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nvien.maNV, nvien.tenNV, nvien.diaChi, nvien.SĐT, nvien.luong, nvien.chucVu, nvien.trangThai) # sửa ở đây
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
            return [NhanVien(maNV=row[0], tenNV=row[1], diaChi=row[2], SĐT=row[3], luong=row[4], chucVu=row[5], trangThai=row[6])] if row else []

        elif tenNV:
            self.cursor.execute("SELECT * FROM NHANVIEN WHERE tenNV LIKE ?", ('%' + tenNV + '%',))
            rows = self.cursor.fetchall()
            return [NhanVien(maNV=row[0], tenNV=row[1], diaChi=row[2], SĐT=row[3], luong=row[4], chucVu=row[5], trangThai=row[6]) for row in rows]
        return []

    def xuatNV(self):
        """Xuất danh sách nhân viên"""
        self.cursor.execute("SELECT * FROM NHANVIEN")
        rows = self.cursor.fetchall()

        self.dsach = [
            NhanVien(maNV=row[0], tenNV=row[1], diaChi=row[2], SĐT=row[3], luong=row[4], chucVu=row[5], trangThai=row[6]) # sửa ở đây
            for row in rows
        ]

        return self.dsach

    def dongKetNoi(self):
        self.conn.close()

