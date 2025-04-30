from datetime import datetime


class HoaDon:
    def __init__(self, maHD="", maNV="", maKH="", ngayTaoHD=None, tongTien=None):
        self.maHD = maHD
        self.maNV = maNV
        self.maKH = maKH
        self.ngayTaoHD = ngayTaoHD if ngayTaoHD else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tongTien = tongTien

    def thongTinHD(self, maHD, maNV, maKH, tongTien):
        """Thiết lập thông tin hóa đơn"""
        self.maHD = maHD
        self.maNV = maNV
        self.maKH = maKH
        self.tongTien = tongTien

    def tinhTongTien(self, cursor):
        """Tính tổng tiền hóa đơn từ chi tiết"""
        try:
            cursor.execute("SELECT thanhTien FROM CHITIETHD WHERE maHD = ?", (self.maHD,))
            rows = cursor.fetchall()
            self.tongTien = sum(row[0] for row in rows) if rows else 0
            return self.tongTien
        except Exception as e:
            print(f"Lỗi khi tính tổng tiền: {e}")
            return 0

    def xuat(self):
        """Xuất thông tin hóa đơn"""
        return f"""Mã hóa đơn: {self.maHD}
Mã nhân viên: {self.maNV}
Mã khách hàng: {self.maKH}
Ngày tạo hóa đơn: {self.ngayTaoHD}
Tổng tiền: {self.tongTien} VND"""

    def __str__(self):
        """Trả về chuỗi mô tả hóa đơn"""
        return f"Hóa đơn {self.maHD} | NV: {self.maNV} | KH: {self.maKH} | Ngày: {self.ngayTaoHD} | Tổng tiền: {self.tongTien}"

    @staticmethod
    def soNguyen(value):
        """Hỗ trợ kiểm tra số nguyên hợp lệ"""
        try:
            value = int(value)
            return value if value > 0 else None
        except ValueError:
            return None

    @staticmethod
    def soThuc(value):
        """Hỗ trợ kiểm tra số thực hợp lệ"""
        try:
            value = float(value)
            return value if value > 0 else None
        except ValueError:
            return None
