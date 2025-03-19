class ChiTietHD:
    def __init__(self, maHD="", maSP="", soLuong=0, donGia=0.0):
        self.maHD = maHD
        self.maSP = maSP
        self.soLuong = soLuong
        self.donGia = donGia
        self.thanhTien = self.thanhTien()

    def thongTinHD(self, maHD, maSP, soLuong, donGia):
        """Thiết lập thông tin chi tiết hóa đơn"""
        self.maHD = maHD
        self.maSP = maSP
        self.soLuong = soLuong
        self.donGia = donGia
        self.thanhTien = self.thanhTien()

    def thanhTien(self):
        """Tính thành tiền"""
        return self.soLuong * self.donGia

    def xuat(self):
        """Xuất thông tin chi tiết hóa đơn"""
        return f"Mã HD: {self.maHD}, Mã SP: {self.maSP}, Số lượng: {self.soLuong}, Đơn giá: {self.donGia}, Thành tiền: {self.thanhTien}"
