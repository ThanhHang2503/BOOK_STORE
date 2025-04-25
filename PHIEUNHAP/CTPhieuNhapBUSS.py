from datetime import datetime
from CTPhieuNhapDAO import CTPhieuNhapDAO 

class CTPhieuNhapBUSS:
    def __init__(self):
        self.dsctpn = []  

    def lay_du_lieu_tu_sql(self):
        self.dsctpn = CTPhieuNhapDAO().lay_du_lieu_tu_sql()
        
    def them(self, maPN, maSP, soLuong, donGia):
        try:
            soLuong = int(soLuong)
            donGia = float(donGia)
            thanhTien = soLuong * donGia

            if self.kiem_tra_trung(maPN, maSP):
                return False 

            self.dsctpn.append([maPN, maSP, soLuong, donGia, thanhTien])
            CTPhieuNhapDAO.them()
            return True
        except ValueError:
            return False

    def xoa(self, maPN, maSP):
        for item in self.dsctpn:
            if isinstance(item, list) and len(item) >= 2:
                if item[0] == maPN and item[1] == maSP:
                    self.dsctpn.remove(item)
                   
                    return True
        return False

    def kiem_tra_trung(self, maPN, maSP):
        for item in self.dsctpn:
            if item.maPN == maPN and item.maSP == maSP:
                return True
        return False

    def luu_ctpn_vao_sql(self):
        try:
            for item in self.dsctpn:
                maPN, maSP, soLuong, donGia, thanhTien = item 
                CTPhieuNhapDAO().luu_thong_tin_vao_sql(maPN, maSP, soLuong, donGia, thanhTien)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu chi tiết phiếu nhập: {e}")
            return False

    def cap_nhat_tong_tien(self, maPN):
        tong_tien = 0
        for item in self.dsctpn:
            if item[0] == maPN:
                tong_tien += item[4]  # thanhTien
        return tong_tien
    
    def tim_kiem(self, maPN):
        ket_qua = []
        for item in self.dsctpn:
            if str(item.maPN) == str(maPN):
                ket_qua.append(item)
        return ket_qua
    
    def sua(self, maPN, maSP, soLuong, donGia, thanhTien):
        for item in self.dsctpn:
            if str(item.maPN) == str(maPN) and str(item.maSP) == str(maSP):
                item.soLuong = soLuong
                item.donGia = donGia
                item.thanhTien = thanhTien

                CTPhieuNhapDAO().sua_chi_tiet_phieu_nhap(maPN, maSP, soLuong, donGia, thanhTien)
                return True
        return False
