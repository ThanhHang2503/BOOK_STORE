from datetime import datetime
from DSCTPhieuNhap import DSCTPhieuNhap

class PhieuNhap:
    def __init__(self, maPN="", maNV="", ngayTao=None, dsctpn=None):
        self.maPN = maPN
        self.maNV = maNV 
        
        if ngayTao is None:
            self.ngayTao = datetime.today().date()
        else:
            self.ngayTao = ngayTao 
        
        self.dsctpn = dsctpn if dsctpn is not None else DSCTPhieuNhap()
        self.tongTien = 0 

    def tinh_tong_tien(self):
        self.tongTien = sum(ctpn.thanhTien for ctpn in self.dsctpn.ds)
        return self.tongTien
