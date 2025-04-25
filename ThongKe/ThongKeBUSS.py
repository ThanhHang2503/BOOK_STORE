from datetime import datetime, date, time
from calendar import monthrange

class ThongKeBUSS:
    def __init__(self):
        self.dshoadon = []  

    def lay_du_lieu_tu_sql(self):
        self.dshoadon = self.dao.lay_du_lieu_tu_sql()
        # Chuyển đổi ngày từ str → datetime nếu cần
        for i in range(len(self.dshoadon)):
            maHD, ngayTaoHD, maNV, tongTien = self.dshoadon[i]

            if isinstance(ngayTaoHD, str):
                try:
                    ngayTaoHD = datetime.strptime(ngayTaoHD, "%Y-%m-%d")
                except ValueError:
                    try:
                        ngayTaoHD = datetime.strptime(ngayTaoHD, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        continue  # bỏ qua hóa đơn nếu lỗi định dạng
            elif isinstance(ngayTaoHD, date) and not isinstance(ngayTaoHD, datetime):
                ngayTaoHD = datetime.combine(ngayTaoHD, time.min)

            self.dshoadon[i] = (maHD, ngayTaoHD, maNV, tongTien)

    def ThongKeTuNgayDenNgay(self, ngayBD, ngayKT):
        ket_qua = []
        doanh_thu = 0
        for hd in self.dshoadon:
            maHD, ngayTaoHD, maNV, tongTien = hd
            if ngayBD <= ngayTaoHD <= ngayKT:
                ket_qua.append(hd)
                doanh_thu += tongTien
        return ket_qua, doanh_thu

    def ThongKeTheoNgay(self, ngay):  # 'ngay' là kiểu datetime.date
        ket_qua = []
        doanh_thu = 0
        for hd in self.dshoadon:
            maHD, ngayTaoHD, maNV, tongTien = hd
            if ngayTaoHD.date() == ngay:
                ket_qua.append(hd)
                doanh_thu += tongTien
        return ket_qua, doanh_thu

    def ThongKeTheoThang(self, thang, nam):
        ngay_bat_dau = datetime(nam, thang, 1, 0, 0, 0)
        ngay_ket_thuc = datetime(nam, thang, monthrange(nam, thang)[1], 23, 59, 59)
        return self.ThongKeTuNgayDenNgay(ngay_bat_dau, ngay_ket_thuc)

    def ThongKeTheoNam(self, nam):
        ngay_bat_dau = datetime(nam, 1, 1, 0, 0, 0)
        ngay_ket_thuc = datetime(nam, 12, 31, 23, 59, 59)
        return self.ThongKeTuNgayDenNgay(ngay_bat_dau, ngay_ket_thuc)
