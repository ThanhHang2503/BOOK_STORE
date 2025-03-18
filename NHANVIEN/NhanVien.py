class NhanVien:
    def __init__(self, maNV, hoten, dchi, sdt, luong, chucvu, trangthai):
        self.maNV = maNV
        self.hoten = hoten
        self.dchi = dchi
        self.sdt = sdt
        self.luong = luong
        self.chucvu = chucvu
        self.trangthai = trangthai  # 0: Nghỉ việc, 1: Đang làm việc

    def nhap_thong_tin(self):
        self.maNV = input("Nhập mã nhân viên: ")
        self.hoten = input("Nhập họ tên: ")
        self.dchi = input("Nhập địa chỉ: ")
        self.sdt = input("Nhập số điện thoại: ")
        self.luong = float(input("Nhập lương: "))
        self.chucvu = input("Nhập chức vụ: ")
        self.trangthai = int(input("Nhập trạng thái (0: Nghỉ việc, 1: Đang làm việc): "))

    def xuat_thong_tin(self):
        print(f"Mã NV: {self.maNV}")
        print(f"Họ tên: {self.hoten}")
        print(f"Địa chỉ: {self.dchi}")
        print(f"SĐT: {self.sdt}")
        print(f"Lương: {self.luong}")
        print(f"Chức vụ: {self.chucvu}")
        print(f"Trạng thái: {'Đang làm việc' if self.trangthai == 1 else 'Nghỉ việc'}")