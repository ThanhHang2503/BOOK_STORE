class KhachHang:
    def __init__(self, maKH="", tenKH="", diaChi="", dienThoai=""):
        """
        Khởi tạo đối tượng khách hàng.

        Parameters:
            maKH (str): Mã khách hàng.
            tenKH (str): Tên khách hàng.
            diaChi (str): Địa chỉ.
            dienThoai (str): Số điện thoại.
        """
        self.maKH = maKH
        self.tenKH = tenKH
        self.diaChi = diaChi
        self.dienThoai = dienThoai

    def nhap_thong_tin(self):
        """Nhập thông tin khách hàng từ bàn phím."""
        self.maKH = input("Nhập mã khách hàng: ")
        self.tenKH = input("Nhập tên khách hàng: ")
        self.diaChi = input("Nhập địa chỉ: ")
        self.dienThoai = input("Nhập số điện thoại: ")

    def xuat_thong_tin(self):
        """Xuất thông tin khách hàng ra màn hình."""
        print(f"Mã KH: {self.maKH}")
        print(f"Tên KH: {self.tenKH}")
        print(f"Địa chỉ: {self.diaChi}")
        print(f"Điện thoại: {self.dienThoai}")

    def __str__(self):
        """Trả về chuỗi thể hiện thông tin của khách hàng."""
        return (f"KhachHang(maKH={self.maKH}, tenKH={self.tenKH}, "
                f"diaChi={self.diaChi}, dienThoai={self.dienThoai})")