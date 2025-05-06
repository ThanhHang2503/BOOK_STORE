class ChiTietPN:
    def __init__(self, maPN="", maSP="", soLuongSP=0, donGia=0.0):
        self.maPN = maPN
        self.maSP = maSP
        self.soLuongSP = soLuongSP
        self.donGia = donGia
        self.thanhTien = self.thanhTien()

    def thongTinPN(self, maPN, maSP, soLuongSP, donGia):
        self.maPN = maPN
        self.maSP = maSP
        self.soLuongSP = soLuongSP
        self.donGia = donGia
        self.thanhTien = self.thanhTien()

    def thanhTien(self):
        """Tính thành tiền"""
        return self.soLuongSP * self.donGia

    def xuat(self):
        return f"Mã HD: {self.maPN}, Mã SP: {self.maSP}, Số lượng: {self.soLuongSP}, Đơn giá: {self.donGia}, Thành tiền: {self.thanhTien}"
