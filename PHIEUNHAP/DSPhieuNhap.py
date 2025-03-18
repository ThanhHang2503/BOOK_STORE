import pyodbc

class DSPhieuNhap:
    def __init__(self):
        self.ds = []  
        self.conn = None  
        self.connect_db()  

    def connect_db(self):
        conn = pyodbc.connect('DRIVER={SQL Server};'
                              'SERVER=localhost\\SQLEXPRESS;'    
                              'DATABASE=DOANPYTHON;')   
        return conn
    
    def lay_du_lieu_tu_sql(self):
        conn = self.connect_db()  
        cursor = conn.cursor()
        query = "SELECT maPN, maNV, ngayTaoPN, tongTien FROM PhieuNhap"
        cursor.execute(query)
        danh_sach = cursor.fetchall() # Lấy toàn bộ dữ liệu từ truy vấn
        cursor.close()
        conn.close()

        return danh_sach 

    def luu_thong_tin_vao_sql(self, maPN, maNV, ngayTao):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO PhieuNhap (maPN, maNV, ngayTaoPN, tongTien) VALUES (?, ?, ?, ?)", 
                        (maPN, maNV, ngayTao, 0))
            conn.commit()
            print("Thêm phiếu nhập thành công!")

        except Exception as e:
            print(f"Lỗi khi lưu phiếu nhập: {str(e)}")

        finally:
            cursor.close()
            conn.close()
    def tim_kiem_phieu_nhap(self, ma_pn):
        """Tìm kiếm phiếu nhập trực tiếp trong database"""
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = "SELECT maPN, maNV, ngayTaoPN, tongTien FROM PhieuNhap WHERE maPN = ?"
            cursor.execute(query, (ma_pn,))
            row = cursor.fetchone()  # Lấy kết quả đầu tiên

            cursor.close()
            conn.close()

            if row:
                print("✅ Tìm thấy phiếu nhập:", row)
                return {
                    "ma_phieu_nhap": row[0],
                    "ma_nhan_vien": row[1],
                    "ngay_nhap": row[2],
                    "tong_tien": row[3],
                }
            else:
                print("⚠️ Không tìm thấy phiếu nhập!")
                return None

        except Exception as e:
            print(f"❌ Lỗi khi tìm kiếm phiếu nhập: {str(e)}")
            return None
