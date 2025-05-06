def capNhatTongTien(maPN, cursor):
    try:
        cursor.execute("SELECT thanhTien FROM CHITIETPN WHERE maPN = ?", (maPN,))
        rows = cursor.fetchall()
        
        # Tính tổng tiền, mặc định là 0 nếu không có chi tiết
        tong_tien = sum(row[0] for row in rows) if rows else 0
        
        cursor.execute(
            "UPDATE PHIEUNHAP SET tongTien = ? WHERE maPN = ?",
            (tong_tien, maPN)
        )
        return True
    except Exception as e:
        print(f"Lỗi khi cập nhật tổng tiền: {e}")
        # Nếu có lỗi, đặt tổng tiền về 0
        try:
            cursor.execute(
                "UPDATE PHIEUNHAP SET tongTien = 0 WHERE maPN = ?",
                (maPN,)
            )
        except:
            pass
        return False 