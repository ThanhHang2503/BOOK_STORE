def capNhatTongTien(maHD, cursor):
    """Cập nhật tổng tiền của hóa đơn dựa trên chi tiết hóa đơn"""
    try:
        # Lấy danh sách chi tiết hóa đơn
        cursor.execute("SELECT thanhTien FROM CHITIETHD WHERE maHD = ?", (maHD,))
        rows = cursor.fetchall()
        
        # Tính tổng tiền, mặc định là 0 nếu không có chi tiết
        tong_tien = sum(row[0] for row in rows) if rows else 0
        
        # Cập nhật tổng tiền vào hóa đơn
        cursor.execute(
            "UPDATE HOADON SET tongTien = ? WHERE maHD = ?",
            (tong_tien, maHD)
        )
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật tổng tiền: {e}")
        # Nếu có lỗi, đặt tổng tiền về 0
        try:
            cursor.execute(
                "UPDATE HOADON SET tongTien = 0 WHERE maHD = ?",
                (maHD,)
            )
        except:
            pass
        return False 