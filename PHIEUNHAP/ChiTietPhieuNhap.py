class ChiTietPhieuNhap:
    def __init__(self, maPN="", maSP="", soLuong=0, donGia=0.0):
        self.maPN = maPN
        self.maSP = maSP
        self.soLuong = soLuong
        self.donGia = donGia
        self.thanhTien = soLuong * donGia
        
    