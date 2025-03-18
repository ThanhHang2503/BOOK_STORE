import pyodbc

class DSCTPhieuNhap:
    def __init__(self):
        self.ds = []

    def connect_db(self):
        conn = pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER=localhost\\SQLEXPRESS;'
                              'DATABASE=DOANPYTHON;')   
        return conn

    def lay_du_lieu_tu_sql(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        query = "SELECT maPN, maSP, soLuongSP, donGia, thanhTien FROM CHITIETPN"
        cursor.execute(query)
        danh_sach = cursor.fetchall()  
        cursor.close()
        conn.close()
        return danh_sach 

    def luu_thong_tin_vao_sql(self, maPN, maSP, soLuong, donGia, thanhTien):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CHITIETPN (maPN, maSP, soLuongSP, donGia, thanhTien) VALUES (?, ?, ?, ?, ?)", 
                           (maPN, maSP, soLuong, donGia, thanhTien))
            conn.commit()
            print("Thêm chi tiết phiếu nhập thành công!")

        except Exception as e:
            print(f"Lỗi khi lưu chi tiết phiếu nhập: {str(e)}")

        finally:
            cursor.close()
            conn.close()

    def kiem_tra_lay_du_lieu(self):
        danh_sach = self.lay_du_lieu_tu_sql()
        if danh_sach:
            print("Dữ liệu lấy thành công! Một số dòng đầu:")
            for row in danh_sach[:10]:
                print(row)
        else:
            print("Không có dữ liệu trong bảng CHITIETPN!")

if __name__ == "__main__":
    ds_ct_phieu_nhap = DSCTPhieuNhap()
    ds_ct_phieu_nhap.kiem_tra_lay_du_lieu()
