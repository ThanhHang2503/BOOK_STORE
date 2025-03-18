import pyodbc

class SanPham:
    def __init__(self, connection_string):
        self.conn_str = connection_string
    
    def get_connection(self):
        return pyodbc.connect(self.conn_str)
    
    def load_data(self):
        query = "SELECT MaSP, TenSP, SoLuongTon, DonGia, TacGia, NhaXuatBan FROM SanPham"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [
                {
                    "maSP": row.MaSP,
                    "tenSP": row.TenSP,
                    "soLuongTon": row.SoLuongTon,
                    "donGia": row.DonGia,
                    "tacGia": row.TacGia,
                    "nhaXuatBan": row.NhaXuatBan
                }
                for row in cursor.fetchall()
            ]
    
    def add_sanpham(self, maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan):
        query = """
        INSERT INTO SanPham (MaSP, TenSP, SoLuongTon, DonGia, TacGia, NhaXuatBan)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan))
            conn.commit()
        print("Thêm sản phẩm thành công!")
    
    def update_sanpham(self, maSP, tenSP=None, soLuongTon=None, donGia=None, tacGia=None, nhaXuatBan=None):
        updates = []
        params = []
        if tenSP:
            updates.append("TenSP = ?")
            params.append(tenSP)
        if soLuongTon is not None:
            updates.append("SoLuongTon = ?")
            params.append(soLuongTon)
        if donGia is not None:
            updates.append("DonGia = ?")
            params.append(donGia)
        if tacGia:
            updates.append("TacGia = ?")
            params.append(tacGia)
        if nhaXuatBan:
            updates.append("NhaXuatBan = ?")
            params.append(nhaXuatBan)
        
        if not updates:
            print("Không có thông tin nào để cập nhật.")
            return
        
        query = f"UPDATE SanPham SET {', '.join(updates)} WHERE MaSP = ?"
        params.append(maSP)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        print("Cập nhật sản phẩm thành công!")
    
    def delete_sanpham(self, maSP):
        query = "DELETE FROM SanPham WHERE MaSP = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (maSP,))
            conn.commit()
        print("Xóa sản phẩm thành công!")
    
    def search_sanpham(self, key):
        query = """
        SELECT MaSP, TenSP, SoLuongTon, DonGia, TacGia, NhaXuatBan FROM SanPham
        WHERE LOWER(TenSP) LIKE ? OR LOWER(MaSP) LIKE ? OR LOWER(TacGia) LIKE ? OR LOWER(NhaXuatBan) LIKE ?
        """
        key = f"%{key.lower()}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (key, key, key, key))
            return [
                {
                    "maSP": row.MaSP,
                    "tenSP": row.TenSP,
                    "soLuongTon": row.SoLuongTon,
                    "donGia": row.DonGia,
                    "tacGia": row.TacGia,
                    "nhaXuatBan": row.NhaXuatBan
                }
                for row in cursor.fetchall()
            ]
    
    def display_sanpham(self):
        sanpham_list = self.load_data()
        if not sanpham_list:
            print("Danh sách rỗng!")
        else:
            print("\nDanh sách sản phẩm:")
            print("=" * 80)
            for sp in sanpham_list:
                print(f"Mã SP: {sp['maSP']}, Tên: {sp['tenSP']}, Số lượng tồn: {sp['soLuongTon']}, Giá: {sp['donGia']}, Tác giả: {sp['tacGia']}, Nhà xuất bản: {sp['nhaXuatBan']}")
                print("-" * 80)
    
    # tính tổng giá trị tồn kho
    def tinh_tong_gia_tri_ton_kho(self):
        tong = sum(sp.get("soLuongTon", 0) * sp.get("donGia", 0) for sp in self.sanpham)
        return tong

connection_string = "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=DOANPYTHON;Trusted_Connection=yes;"
sp = SanPham(connection_string)
sp.display_sanpham()

