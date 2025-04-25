from CTPhieuNhapDAO import CTPhieuNhapDAO

class CTPhieuNhapBUSS:
    def __init__(self):
        self.ct_phieu_nhap_dao = CTPhieuNhapDAO()
    
    def lay_theo_ma_phieu_nhap(self, maPN):
        """Get all details for an import receipt"""
        return self.ct_phieu_nhap_dao.lay_theo_ma_phieu_nhap(maPN)