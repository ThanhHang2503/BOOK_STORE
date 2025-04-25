import pyodbc
from datetime import date

class PhieuNhapDAO:
    def __init__(self):
        self.dspn = []  
        self.conn = self.connect_db()  

    def connect_db(self):
        conn = pyodbc.connect('DRIVER={SQL Server};'
                              r'SERVER=DESKTOP-SG8M886\SQLEXPRESS;'  
                              'DATABASE=DOANPYTHON;')  
        return conn

    def lay_du_lieu_tu_sql(self):
        cursor = self.conn.cursor()  
        query = "SELECT maPN, ngayTaoPN, maNV , tongTien FROM PhieuNhap"
        cursor.execute(query) 
        dspn = cursor.fetchall() 
        cursor.close()  
        return dspn  

    def luu_thong_tin_vao_sql(self, maPN, maNV, ngayTaoPN, tongTien):
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO PhieuNhap (maPN, maNV, ngayTaoPN, tongTien) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (maPN, maNV, ngayTaoPN, tongTien))  
            self.conn.commit()  
        except Exception as e:
            print("Lỗi khi lưu Phiếu Nhập:", str(e))

    def tim_kiem_phieu_nhap(self, ma_pn):
        try:
            cursor = self.conn.cursor() 
            query = "SELECT maPN, maNV, ngayTaoPN, tongTien FROM PhieuNhap WHERE maPN = ?"
            cursor.execute(query, (ma_pn,))  
            row = cursor.fetchone()
            cursor.close() 

            if row:
                return {
                    "ma_phieu_nhap": row[0],
                    "ma_nhan_vien": row[1],
                    "ngay_nhap": row[2],
                    "tong_tien": row[3],
                }
            else:
                return None

        except Exception as e:
            print(f"Lỗi khi tìm kiếm phiếu nhập: {str(e)}")
            return None
        
    def sua_phieu_nhap(self, maPN, ngayTaoPN, maNV, tongTien):
        try:
            query = """
            UPDATE PhieuNhap
            SET ngayTaoPN = ?, maNV = ?, tongTien = ?
            WHERE maPN = ?
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (ngayTaoPN, maNV, tongTien, maPN))
            self.conn.commit()
            result = cursor.rowcount > 0
            cursor.close()
            return result
        except Exception as e:
            print(f"Lỗi DAO khi cập nhật phiếu nhập: {e}")
            return False



    def xoa_phieu_nhap(self, maPN):
        try:
            cursor = self.conn.cursor() 
            query = "DELETE FROM PhieuNhap WHERE maPN = ?"
            cursor.execute(query, (maPN,))  
            self.conn.commit()  
            cursor.close()  
            print(f"Phiếu nhập {maPN} đã được xóa.")
        except Exception as e:
            print(f"Lỗi khi xóa phiếu nhập: {str(e)}")

    def cap_nhat_tong_tien(self, maPN, tongTien):
        try:
            cursor = self.conn.cursor()
            query = """UPDATE PhieuNhap
                    SET tongTien = ?
                    WHERE maPN = ?"""
            cursor.execute(query, (tongTien, maPN))
            self.conn.commit()  
            cursor.close()  
            print("Cập nhật tổng tiền thành công.")
        except Exception as e:
            print(f"Lỗi khi cập nhật tổng tiền: {str(e)}")

    def close(self):
        self.conn.close()
