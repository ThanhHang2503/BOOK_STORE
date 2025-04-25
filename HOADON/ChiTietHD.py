class ChiTietHD:
    def __init__(self, maHD="", maSP="", soLuongSP=0, donGia=0.0):
        self.maHD = maHD
        self.maSP = maSP
        self.soLuongSP = soLuongSP
        self.donGia = donGia
        self.thanhTien = self.thanhTien()

    def thongTinHD(self, maHD, maSP, soLuongSP, donGia):
        """Thiết lập thông tin chi tiết hóa đơn"""
        self.maHD = maHD
        self.maSP = maSP
        self.soLuongSP = soLuongSP
        self.donGia = donGia
        self.thanhTien = self.thanhTien()

    def thanhTien(self):
        """Tính thành tiền"""
        return self.soLuongSP * self.donGia

    def xuat(self):
        """Xuất thông tin chi tiết hóa đơn"""
        return f"Mã HD: {self.maHD}, Mã SP: {self.maSP}, Số lượng: {self.soLuongSP}, Đơn giá: {self.donGia}, Thành tiền: {self.thanhTien}"
