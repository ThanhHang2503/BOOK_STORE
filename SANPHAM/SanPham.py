import pyodbc

class SanPham:
    def __init__(self, maSP="", tenSP="", soLuongTon=0, donGia=0.0, tacGia="", nhaXuatBan=""):
        """
        Khởi tạo đối tượng Sản phẩm.
        
        Parameters:
            maSP (str): Mã sản phẩm.
            tenSP (str): Tên sản phẩm.
            soLuongTon (int): Số lượng tồn.
            donGia (float): Đơn giá.
            tacGia (str): Tác giả.
            nhaXuatBan (str): Nhà xuất bản.
        """
        self.maSP = maSP
        self.tenSP = tenSP
        self.soLuongTon = soLuongTon
        self.donGia = donGia
        self.tacGia = tacGia
        self.nhaXuatBan = nhaXuatBan

    def nhap_thong_tin(self):
        """Nhập thông tin sản phẩm từ bàn phím."""
        self.maSP = input("Nhập mã sản phẩm: ")
        self.tenSP = input("Nhập tên sản phẩm: ")
        self.soLuongTon = int(input("Nhập số lượng tồn: "))
        self.donGia = float(input("Nhập đơn giá: "))
        self.tacGia = input("Nhập tác giả: ")
        self.nhaXuatBan = input("Nhập nhà xuất bản: ")

    def xuat_thong_tin(self):
        """Xuất thông tin sản phẩm ra màn hình."""
        print(f"Mã SP: {self.maSP}")
        print(f"Tên SP: {self.tenSP}")
        print(f"Số lượng tồn: {self.soLuongTon}")
        print(f"Đơn giá: {self.donGia}")
        print(f"Tác giả: {self.tacGia}")
        print(f"Nhà xuất bản: {self.nhaXuatBan}")
    
    def __str__(self):
        """Trả về chuỗi thể hiện thông tin sản phẩm."""
        return (f"SanPham(maSP={self.maSP}, tenSP={self.tenSP}, "
                f"soLuongTon={self.soLuongTon}, donGia={self.donGia}, "
                f"tacGia={self.tacGia}, nhaXuatBan={self.nhaXuatBan})")

