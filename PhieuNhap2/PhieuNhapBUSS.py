from PhieuNhapDAO import PhieuNhapDAO
from datetime import datetime

class PhieuNhapBUSS:
    def __init__(self):
        self.phieu_nhap_dao = PhieuNhapDAO()
    
    def lay_danh_sach(self):
       
        return self.phieu_nhap_dao.lay_danh_sach()
    
    def tim_theo_ma(self, maPN):
        """Find an import receipt by ID"""
        return self.phieu_nhap_dao.tim_theo_ma(maPN)
    
    def tim_theo_nhan_vien(self, maNV):
        """Find import receipts by employee ID"""
        return self.phieu_nhap_dao.tim_theo_nhan_vien(maNV)
    
    def tim_theo_ngay(self, from_date, to_date):
        """Find import receipts by date range"""
        return self.phieu_nhap_dao.tim_theo_ngay(from_date, to_date)
    
    def them(self, phieu_nhap):
        """Add a new import receipt"""
        # Validate the input
        if not phieu_nhap.maPN or not phieu_nhap.maNV:
            return False
        
        if not phieu_nhap.dsCTPN or len(phieu_nhap.dsCTPN) == 0:
            return False
        
        # Add the import receipt
        return self.phieu_nhap_dao.them(phieu_nhap)
    
    def sua(self, phieu_nhap):
        """Update an import receipt"""
        # Validate the input
        if not phieu_nhap.maPN or not phieu_nhap.maNV:
            return False
        
        if not phieu_nhap.dsCTPN or len(phieu_nhap.dsCTPN) == 0:
            return False
        
        # Update the import receipt
        return self.phieu_nhap_dao.sua(phieu_nhap)
    
    def xoa(self, maPN):
        """Delete an import receipt"""
        return self.phieu_nhap_dao.xoa(maPN)
    
    def tao_ma_phieu_nhap_moi(self):
        return self.phieu_nhap_dao.tao_ma_phieu_nhap_moi()
    
    def in_danh_sach(self, phieu_nhap_list):
        """Generate a text representation of a list of import receipts"""
        output = "DANH SÁCH PHIẾU NHẬP\n"
        output += "===========================================\n"
        output += "Mã PN\tMã NV\tNgày tạo\t\tTổng tiền\n"
        output += "-------------------------------------------\n"
        
        for pn in phieu_nhap_list:
            output += f"{pn.maPN}\t{pn.maNV}\t{pn.ngayTaoPN.strftime('%d/%m/%Y')}\t{pn.tongTien:,.0f}\n"
        
        output += "===========================================\n"
        
        return output
    
    def in_chi_tiet(self, maPN):
        """Generate a text representation of an import receipt"""
        phieu_nhap = self.tim_theo_ma(maPN)
        
        if not phieu_nhap:
            return f"Không tìm thấy phiếu nhập với mã {maPN}."
        
        output = "CHI TIẾT PHIẾU NHẬP\n"
        output += "===========================================\n"
        output += f"Mã phiếu nhập: {phieu_nhap.maPN}\n"
        output += f"Mã nhân viên: {phieu_nhap.maNV}\n"
        output += f"Ngày tạo: {phieu_nhap.ngayTaoPN.strftime('%d/%m/%Y')}\n"
        output += f"Tổng tiền: {phieu_nhap.tongTien:,.0f} VND\n"
        output += "-------------------------------------------\n"
        output += "Mã SP\tSố lượng\tĐơn giá\t\tThành tiền\n"
        output += "-------------------------------------------\n"
        
        for ctpn in phieu_nhap.dsCTPN:
            output += f"{ctpn.maSP}\t{ctpn.soLuong}\t\t{ctpn.donGia:,.0f}\t\t{ctpn.thanhTien:,.0f}\n"
        
        output += "===========================================\n"
        
        return output