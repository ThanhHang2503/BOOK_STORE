from datetime import datetime


class PhieuNhap:
    def __init__(self, maPN="", ngayTaoPN=None, maNV="", tongTien=None):
        self.maPN = maPN
        self.ngayTaoPN = ngayTaoPN if ngayTaoPN else datetime.now().strftime("%Y-%m-%d")
        self.maNV = maNV
        self.tongTien = tongTien

    def thongTinPN(self, maPN, maNV, tongTien):
        """Thiết lập thông tin phiếu nhập"""
        self.maPN = maPN
        self.maNV = maNV
        self.tongTien = tongTien

    def tinhTongTien(self, cursor):
        """Tính tổng tiền phiếu nhập từ chi tiết"""
        try:
            cursor.execute("SELECT thanhTien FROM CHITIETPN WHERE maPN = ?", (self.maPN,))
            rows = cursor.fetchall()
            self.tongTien = sum(row[0] for row in rows) if rows else 0
            return self.tongTien
        except Exception as e:
            print(f"Lỗi khi tính tổng tiền: {e}")
            return 0

    def xuat(self):
        """Xuất thông tin phiếu nhập"""
        return f"""Mã phiếu nhập: {self.maPN}
Ngày tạo phiếu nhập: {self.ngayTaoPN}
Mã nhân viên: {self.maNV}
Tổng tiền: {self.tongTien} VND"""

    def __str__(self):
        """Trả về chuỗi mô tả phiếu nhập"""
        return f"Phiếu nhập {self.maPN} | Ngày: {self.ngayTaoPN} | NV: {self.maNV} | Tổng tiền: {self.tongTien}"

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
