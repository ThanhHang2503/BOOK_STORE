from datetime import date 

class PhieuNhapDTO:
    def __init__(self, maPN="", maNV="", ngayTao=None, tongTien=0.0, dsCTPN=None):
        self.maPN = maPN      
        self.maNV = maNV      
        self.ngayTao = ngayTao if ngayTao is not None else date.today() 
        self.dsCTPN = dsCTPN if dsCTPN is not None else []
        self.tongTien = self.tinh_tong_tien() 
        
    def tinh_tong_tien(self):
        return sum(ctpn.thanhTien for ctpn in self.dsCTPN)
