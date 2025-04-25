import pyodbc
from ChiTietPhieuNhapDTO import ChiTietPhieuNhapDTO

class CTPhieuNhapDAO:
    def __init__(self):
        self.ds = [] 

    def connect_db(self):
        return pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=DESKTOP-SG8M886\\SQLEXPRESS;'
            'DATABASE=DOANPYTHON;'
            'Trusted_Connection=yes;'
        )

    def lay_du_lieu_tu_sql(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = "SELECT maPN, maSP, soLuongSP, donGia, thanhTien FROM CHITIETPN"
            cursor.execute(query)
            rows = cursor.fetchall()

            self.ds = []  # Danh sách ChiTietPhieuNhapDTO
            for row in rows:
                ctpn = ChiTietPhieuNhapDTO(
                    maPN=row[0],
                    maSP=row[1],
                    soLuong=row[2],
                    donGia=row[3],
                    thanhTien=row[4]
                )
                self.ds.append(ctpn)

            return self.ds

        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")
            return []
        finally:
            cursor.close()
            conn.close()


    def them(self, maPN, maSP, soLuong, donGia, thanhTien):
        try:
            conn=self.connect_db()
            cursor= conn.cursor()
            cursor.execute(
                "INSERT INTO CHITIETPN (maPN, maSP, soLuongSP, donGia, thanhTien) VALUES (?, ?, ?, ?, ?)",
                (maPN, maSP, soLuong, donGia, thanhTien)
            )
            conn.commit()
        except Exception as e:
            print(f"Lỗi khi lưu chi tiết phiếu nhập: {str(e)}")

        finally:
            cursor.close()
            conn.close()
            
    def sua_chi_tiet_phieu_nhap(self, maPN, maSP, soLuong, donGia, thanhTien):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            sql = """
                UPDATE CHITIETPN
                SET soLuongSP = ?, donGia = ?, thanhTien = ?
                WHERE maPN = ? AND maSP = ?
            """
            cursor.execute(sql, (soLuong, donGia, thanhTien, maPN, maSP))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("[ERROR - DAO] Không thể cập nhật chi tiết phiếu nhập:", e)
            return False
