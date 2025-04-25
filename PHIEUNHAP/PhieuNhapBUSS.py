from datetime import datetime
from PhieuNhapDAO import PhieuNhapDAO
from CTPhieuNhapBUSS import CTPhieuNhapBUSS

class PhieuNhapBUSS:
    def __init__(self):
        self.dsphieunhap = []  
        self.dao = PhieuNhapDAO()

    def lay_du_lieu_tu_sql(self):
        self.dsphieunhap = self.dao.lay_du_lieu_tu_sql()

    def them(self, maPN, ngayNhap, nhaCungCap, tongTien):
        try:
            ngayNhap = datetime.strptime(ngayNhap, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Ngày nhập không hợp lệ! Định dạng phải là YYYY-MM-DD")

        phieu_nhap = [maPN, ngayNhap, nhaCungCap, tongTien]
        self.dsphieunhap.append(phieu_nhap)
        self.dao.them_phieu_nhap(maPN, ngayNhap, nhaCungCap, tongTien)

    def sua_phieu_nhap(self, maPN, ngayTao, maNV, tongTien):
        try:
            print(f"Đang cập nhật phiếu nhập với mã phiếu: {maPN}, ngày tạo: {ngayTao}, mã nhân viên: {maNV}, tổng tiền: {tongTien}")
            result = self.dao.sua_phieu_nhap(maPN, ngayTao, maNV, tongTien)
            if result:
                print("Cập nhật phiếu nhập thành công.")
            else:
                print("Không tìm thấy phiếu nhập để cập nhật.")
            return result
        except Exception as e:
            print(f"Đã xảy ra lỗi khi cập nhật phiếu nhập: {e}")
            return False


    def tim_kiem(self, maPN):
        for item in self.dsphieunhap:
            if str(item[0]) == maPN:
                maPN = item[0]
                ngayTao = item[1]
                maNV = item[2]
                tongTien = item[3]
                return (maPN, ngayTao, maNV, tongTien) 
        return None

    def luu_phi_nhap_vao_sql(self):
        try:
            for item in self.dsphieunhap:
                maPN = item[0]
                ngayNhap = item[1]
                nhaCungCap = item[2]
                tongTien = item[3]
                self.dao.them_phieu_nhap(maPN, ngayNhap, nhaCungCap, tongTien)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu phiếu nhập: {e}")
            return False

    def cap_nhat_tong_tien(self, maPN):
        chi_tiet_phieu_nhap = CTPhieuNhapBUSS()
        chi_tiet_phieu_nhap.lay_du_lieu_tu_sql()
        tong_tien = 0
        for item in chi_tiet_phieu_nhap.dsctpn:
            if item[0] == maPN:
                tong_tien += item[4]
        self.dao.cap_nhat_tong_tien(maPN, tong_tien)
