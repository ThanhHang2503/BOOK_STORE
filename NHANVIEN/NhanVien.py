class NhanVien:
    def __init__(self, maNV="", tenNV="", diaChi="", SĐT="", luong=0.0, chucVu="", trangThai=""):
        self.maNV = maNV
        self.tenNV = tenNV
        self.diaChi = diaChi
        self.SĐT = SĐT
        self.luong = luong
        self.chucVu = chucVu
        self.trangThai = trangThai

    def nhap(self):
        """Nhập thông tin nhân viên từ bàn phím"""
        self.maNV = input("Nhập mã nhân viên: ")
        self.tenNV = input("Nhập họ tên của nhân viên: ")
        self.diaChi = input("Nhập địa chỉ: ")
        self.SĐT = input("Nhập số điện thoại: ")

        while True:
            try:
                self.luong = float(input("Nhập lương: "))
                break
            except ValueError:
                print("Lương phải là số! Vui lòng nhập lại.")

        self.chucVu = input("Nhập chức vụ: ")

        while True:
            self.trangThai = input("Nhập trạng thái (1: còn làm, 0: nghỉ làm): ")
            if self.trangThai in ("0", "1"):
                break
            else:
                print("Trạng thái không hợp lệ! Vui lòng nhập lại.")

    def xuat(self):
        """Xuất thông tin nhân viên ra màn hình"""
        print(f"Mã NV: {self.maNV}")
        print(f"Họ tên: {self.tenNV}")
        print(f"Địa chỉ: {self.diaChi}")
        print(f"Số điện thoại: {self.SĐT}")
        print(f"Lương: {self.luong}")
        print(f"Chức vụ: {self.chucVu}")
        print(f"Trạng thái: {self.trangThai}")

    def __str__(self):
        """Trả về chuỗi thông tin nhân viên"""
        return f"{self.maNV} | {self.tenNV} | {self.diaChi} | {self.SĐT} | {self.luong} | {self.chucVu} | {self.trangThai}"