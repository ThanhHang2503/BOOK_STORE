import tkinter as tk
from tkinter import ttk, messagebox

from .ChiTietHD import ChiTietHD
from .DSCTHoaDon import DSCTHoaDon


class ChiTietHDGUI:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Khởi tạo các frame con cho từng chức năng
        self.them_frame = ttk.Frame(self.frame)
        self.sua_frame = ttk.Frame(self.frame)
        self.timKiem_frame = ttk.Frame(self.frame)
        self.hienThiDS_frame = ttk.Frame(self.frame)
        self.trangThai_frame = ttk.Frame(self.frame)

        self.ds_chitiet = DSCTHoaDon()  # KẾT NỐI DATABASE
        self.current_maHD = None  # Mã hóa đơn hiện tại đang xem chi tiết
        self.taoGiaoDien()

        # Mặc định hiển thị danh sách chi tiết hóa đơn
        self.hienThiDS()

        # cờ trạng thái thao tác
        self.thanhCong = False

    def hienThiDS(self, maHD=None):
        try:
            # Xóa dữ liệu cũ trong TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Thêm dữ liệu mới vào TreeView
            if maHD:
                # Chỉ hiển thị chi tiết của hóa đơn có mã maHD
                self.current_maHD = maHD
                ket_qua = self.ds_chitiet.tim_theo_ma_hd(maHD)
                for ct in ket_qua:
                    self.tree.insert("", "end", values=(ct.maHD, ct.maSP, ct.soLuongSP, ct.donGia, ct.thanhTien))

                # Cập nhật tiêu đề frame danh sách
                self.frame_danh_sach.configure(text=f"Chi tiết của hóa đơn {maHD}")

                # Hiển thị nút quay lại danh sách đầy đủ
                self.btn_xem_tat_ca.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            else:
                # Hiển thị tất cả chi tiết hóa đơn
                self.current_maHD = None
                for ct in self.ds_chitiet.ds:
                    self.tree.insert("", "end", values=(ct.maHD, ct.maSP, ct.soLuongSP, ct.donGia, ct.thanhTien))

                # Cập nhật tiêu đề frame danh sách
                self.frame_danh_sach.configure(text="Danh sách chi tiết hóa đơn")

                # Ẩn nút quay lại
                self.btn_xem_tat_ca.grid_forget()

            # Đảm bảo frame hiển thị đúng
            self.frame_danh_sach.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
            self.frame_danh_sach.tkraise()  # Đưa frame danh sách lên trên cùng

        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi hiển thị danh sách: {str(e)}", fg="red")

    def hienThi(self, action):
        """Ẩn widget trong frame trước khi hiển thị"""
        for widget in self.frame.winfo_children():
            widget.grid_forget()

        self.frame.grid(row=0, column=0, sticky="nsew")

        if action == "Hiển thị danh sách":
            # Chỉ hiển thị danh sách, ẩn form nhập liệu và nút
            self.frame_danh_sach.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.hienThiDS()  # Gọi lại để load dữ liệu

        else:
            # Hiển thị form nhập liệu và nút cho các chức năng khác
            self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")

            self.lam_moi_form()  # Reset form khi chuyển giữa các chế độ

            if action == "Thêm chi tiết hóa đơn":
                self.label_thong_bao.config(text="Nhập thông tin chi tiết hóa đơn mới", fg="blue")
                self.entry_maHD.config(state="normal")
                self.entry_maSP.config(state="normal")
                self.btn_luu.config(state="normal")

                # Nếu đang xem chi tiết của một hóa đơn cụ thể, tự động điền mã hóa đơn
                if self.current_maHD:
                    self.entry_maHD.delete(0, tk.END)
                    self.entry_maHD.insert(0, self.current_maHD)

            elif action == "Sửa thông tin chi tiết hóa đơn":
                self.label_thong_bao.config(text="Chọn chi tiết hóa đơn từ danh sách để sửa", fg="blue")
                self.entry_maHD.config(state="readonly")
                self.entry_maSP.config(state="readonly")
                self.btn_luu.config(state="disabled")

            elif action == "Tìm kiếm chi tiết hóa đơn":
                self.label_thong_bao.config(text="Nhập thông tin chi tiết hóa đơn cần tìm", fg="blue")
                self.entry_maHD.config(state="normal")
                self.entry_maSP.config(state="normal")
                self.btn_luu.config(state="disabled")

            else:
                self.label_thong_bao.config(text="", fg="black")

    def anGiaoDien(self):
        """Ẩn giao diện quản lý chi tiết hóa đơn"""
        self.frame.grid_forget()

    def taoGiaoDien(self):
        """Tạo giao diện chung cho quản lý chi tiết hóa đơn"""
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)

        # Frame nhập thông tin
        self.frame_nhap = ttk.LabelFrame(self.frame, text="Thông tin chi tiết hóa đơn")

        self.label_thong_bao = tk.Label(self.frame_nhap, text="", fg="red")
        self.label_thong_bao.grid(row=0, column=0, columnspan=4, pady=5)

        ttk.Label(self.frame_nhap, text="Mã hóa đơn:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_maHD = ttk.Entry(self.frame_nhap)
        self.entry_maHD.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Mã sản phẩm:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_maSP = ttk.Entry(self.frame_nhap)
        self.entry_maSP.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Số lượng:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_soLuongSP = ttk.Entry(self.frame_nhap)
        self.entry_soLuongSP.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Đơn giá:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_donGia = ttk.Entry(self.frame_nhap)
        self.entry_donGia.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Thành tiền:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_thanhTien = ttk.Entry(self.frame_nhap, state="readonly")
        self.entry_thanhTien.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Thêm nút tính toán thành tiền
        self.btn_tinh_tien = ttk.Button(self.frame_nhap, text="Tính thành tiền", command=self.tinhThanhTien)
        self.btn_tinh_tien.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="e")

        # Frame chứa các nút chức năng
        self.frame_button = tk.Frame(self.frame)

        self.btn_lam_moi = tk.Button(self.frame_button, text="Quay lại", command=self.lam_moi_form, bg="#9E9E9E",
                                     fg="white")
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)

        self.btn_luu = tk.Button(self.frame_button, text="OK", command=self.luuChiTietHD, bg="#4CAF50", fg="white")
        self.btn_luu.pack(side=tk.LEFT, padx=5)

        # Frame hiển thị danh sách
        self.frame_danh_sach = ttk.LabelFrame(self.frame, text="Danh sách chi tiết hóa đơn")

        # Nút xem tất cả chi tiết hóa đơn (chỉ hiển thị khi đang xem chi tiết của một hóa đơn cụ thể)
        self.btn_xem_tat_ca = ttk.Button(self.frame_danh_sach, text="Xem tất cả chi tiết",
                                         command=lambda: self.hienThiDS(None))

        # Frame tìm kiếm
        self.frame_timkiem = ttk.Frame(self.frame_danh_sach)
        self.frame_timkiem.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.frame_timkiem, text="Tìm theo mã hóa đơn:").pack(side=tk.LEFT, padx=5)
        self.entry_tim_hd = ttk.Entry(self.frame_timkiem, width=15)
        self.entry_tim_hd.pack(side=tk.LEFT, padx=5)

        ttk.Button(self.frame_timkiem, text="Tìm",
                   command=lambda: self.hienThiDS(self.entry_tim_hd.get().strip())).pack(side=tk.LEFT, padx=5)

        ttk.Button(self.frame_timkiem, text="Xem tất cả",
                   command=lambda: self.hienThiDS(None)).pack(side=tk.LEFT, padx=5)

        # Tạo Treeview để hiển thị danh sách
        self.tree = ttk.Treeview(self.frame_danh_sach, columns=("maHD", "maSP", "soLuongSP", "donGia", "thanhTien"),
                                 show="headings", height=15)
        self.tree.heading("maHD", text="Mã hóa đơn")
        self.tree.heading("maSP", text="Mã sản phẩm")
        self.tree.heading("soLuongSP", text="Số lượng")
        self.tree.heading("donGia", text="Đơn giá")
        self.tree.heading("thanhTien", text="Thành tiền")

        # Thiết lập độ rộng cột
        self.tree.column("maHD", width=100)
        self.tree.column("maSP", width=100)
        self.tree.column("soLuongSP", width=100)
        self.tree.column("donGia", width=150)
        self.tree.column("thanhTien", width=150)

        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(self.frame_danh_sach, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_danh_sach, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sắp xếp các thành phần
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Bắt sự kiện khi chọn một chi tiết hóa đơn trong danh sách
        self.tree.bind("<<TreeviewSelect>>", self.chonHD)

        # Thêm nhóm nút thao tác trên bảng
        self.frame_action_buttons = ttk.Frame(self.frame_danh_sach)
        self.frame_action_buttons.pack(fill="x", padx=5, pady=5)

        self.btn_them = ttk.Button(self.frame_action_buttons, text="Thêm chi tiết",
                                   command=lambda: self.hienThi("Thêm chi tiết hóa đơn"))
        self.btn_them.pack(side=tk.LEFT, padx=5)

        self.btn_sua = ttk.Button(self.frame_action_buttons, text="Sửa chi tiết",
                                  command=self.sua_chitiet_tu_bang)
        self.btn_sua.pack(side=tk.LEFT, padx=5)

        self.btn_xoa = ttk.Button(self.frame_action_buttons, text="Xóa chi tiết",
                                  command=self.xoaChiTietHD)
        self.btn_xoa.pack(side=tk.LEFT, padx=5)

    def tinhThanhTien(self):
        """Tính thành tiền từ số lượng và đơn giá"""
        try:
            soLuongSP = self.entry_soLuongSP.get().strip()
            donGia = self.entry_donGia.get().strip()

            if not soLuongSP or not donGia:
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ số lượng và đơn giá!", fg="red")
                return

            try:
                soLuongSP = int(soLuongSP)
                donGia = float(donGia)
                if soLuongSP <= 0 or donGia <= 0:
                    self.label_thong_bao.config(text="Số lượng và đơn giá phải lớn hơn 0!", fg="red")
                    return
            except ValueError:
                self.label_thong_bao.config(text="Số lượng và đơn giá phải là số!", fg="red")
                return

            thanhTien = soLuongSP * donGia

            self.entry_thanhTien.config(state="normal")
            self.entry_thanhTien.delete(0, tk.END)
            self.entry_thanhTien.insert(0, thanhTien)
            self.entry_thanhTien.config(state="readonly")

            self.label_thong_bao.config(text="Đã tính thành tiền!", fg="green")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi tính thành tiền: {str(e)}", fg="red")

    def sua_chitiet_tu_bang(self):
        """Chọn chi tiết từ bảng để sửa"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn chi tiết hóa đơn cần sửa từ bảng!")
            return

        # Hiển thị form sửa và thiết lập dữ liệu
        self.hienThi("Sửa thông tin chi tiết hóa đơn")
        self.chonHD(None)  # Gọi hàm này để điền dữ liệu vào form

    def chonHD(self, event):
        """Xử lý sự kiện khi chọn một chi tiết hóa đơn trong danh sách"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")

            # Hiển thị thông tin lên form
            self.entry_maHD.config(state="normal")
            self.entry_maHD.delete(0, tk.END)
            self.entry_maHD.insert(0, values[0])
            if self.entry_maHD.cget("state") == "readonly":
                self.entry_maHD.config(state="readonly")

            self.entry_maSP.config(state="normal")
            self.entry_maSP.delete(0, tk.END)
            self.entry_maSP.insert(0, values[1])
            if self.entry_maSP.cget("state") == "readonly":
                self.entry_maSP.config(state="readonly")

            self.entry_soLuongSP.delete(0, tk.END)
            self.entry_soLuongSP.insert(0, values[2])

            self.entry_donGia.delete(0, tk.END)
            self.entry_donGia.insert(0, values[3])

            self.entry_thanhTien.config(state="normal")
            self.entry_thanhTien.delete(0, tk.END)
            self.entry_thanhTien.insert(0, values[4])
            self.entry_thanhTien.config(state="readonly")

            # Nếu đang ở chế độ sửa, kích hoạt nút lưu
            if self.entry_maHD.cget("state") == "readonly" and self.entry_maSP.cget("state") == "readonly":
                self.btn_luu.config(state="normal")

    def luuChiTietHD(self):
        """Lưu thông tin chi tiết hóa đơn mới hoặc cập nhật chi tiết hóa đơn đã có"""
        try:
            maHD = self.entry_maHD.get().strip()
            maSP = self.entry_maSP.get().strip()
            soLuongSP = self.entry_soLuongSP.get().strip()
            donGia = self.entry_donGia.get().strip()

            if not all([maHD, maSP, soLuongSP, donGia]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            try:
                soLuongSP = int(soLuongSP)
                donGia = float(donGia)
                if soLuongSP <= 0 or donGia <= 0:
                    self.label_thong_bao.config(text="Số lượng và đơn giá phải lớn hơn 0!", fg="red")
                    return
            except ValueError:
                self.label_thong_bao.config(text="Số lượng và đơn giá phải là số!", fg="red")
                return

            # Tạo chi tiết hóa đơn mới
            ct = ChiTietHD(
                maHD=maHD,
                maSP=maSP,
                soLuongSP=soLuongSP,
                donGia=donGia
            )

            # Kiểm tra trạng thái của entry_maHD để xác định là thêm mới hay cập nhật
            if self.entry_maHD.cget("state") == "readonly" and self.entry_maSP.cget("state") == "readonly":
                # Đang ở chế độ sửa
                if self.ds_chitiet.xoa(maHD, maSP) and self.ds_chitiet.them(ct):
                    self.hienThiDS(self.current_maHD)  # Cập nhật hiển thị với cùng mã hóa đơn hiện tại
                    self.lam_moi_form()
                    self.label_thong_bao.config(text="Cập nhật chi tiết hóa đơn thành công!", fg="green")
                else:
                    self.label_thong_bao.config(text="Lỗi khi cập nhật chi tiết hóa đơn!", fg="red")
            else:
                # Đang ở chế độ thêm mới
                if self.ds_chitiet.them(ct):
                    # Nếu đang xem chi tiết của một hóa đơn cụ thể, giữ nguyên hiển thị đó
                    self.hienThiDS(maHD if maHD == self.current_maHD else self.current_maHD)
                    self.lam_moi_form()
                    self.label_thong_bao.config(text="Thêm chi tiết hóa đơn thành công!", fg="green")

                    # Nếu thêm chi tiết cho hóa đơn mới, cập nhật mã hóa đơn hiện tại
                    if not self.current_maHD:
                        self.current_maHD = maHD
                else:
                    self.label_thong_bao.config(text=f'Lỗi! Chi tiết hóa đơn đã tồn tại.', fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi: {str(e)}", fg="red")

    def xoaChiTietHD(self):
        """Xóa chi tiết hóa đơn"""
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                messagebox.showerror("Lỗi", "Vui lòng chọn chi tiết hóa đơn cần xóa từ bảng!")
                return

            item = selected_items[0]
            values = self.tree.item(item, "values")
            maHD = values[0]
            maSP = values[1]

            # Hiển thị hộp thoại xác nhận
            confirm = messagebox.askyesno("Xác nhận xóa",
                                          f"Bạn có chắc muốn xóa chi tiết sản phẩm {maSP} của hóa đơn {maHD}?")
            if confirm:
                if self.ds_chitiet.xoa(maHD, maSP):
                    self.hienThiDS(self.current_maHD)  # Cập nhật hiển thị với cùng mã hóa đơn hiện tại
                    self.label_thong_bao.config(text="Xóa chi tiết hóa đơn thành công!", fg="green")
                else:
                    self.label_thong_bao.config(text=f"Không tìm thấy chi tiết hóa đơn để xóa!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi xóa chi tiết hóa đơn: {str(e)}", fg="red")

    def lam_moi_form(self):
        """Làm mới form nhập liệu"""
        self.entry_maHD.config(state="normal")
        self.entry_maHD.delete(0, tk.END)

        # Nếu đang xem chi tiết của một hóa đơn cụ thể, tự động điền mã hóa đơn
        if self.current_maHD:
            self.entry_maHD.insert(0, self.current_maHD)

        self.entry_maSP.config(state="normal")
        self.entry_maSP.delete(0, tk.END)

        self.entry_soLuongSP.delete(0, tk.END)
        self.entry_soLuongSP.insert(0, "0")

        self.entry_donGia.delete(0, tk.END)
        self.entry_donGia.insert(0, "0")

        self.entry_thanhTien.config(state="normal")
        self.entry_thanhTien.delete(0, tk.END)
        self.entry_thanhTien.insert(0, "0")
        self.entry_thanhTien.config(state="readonly")

        self.label_thong_bao.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý chi tiết hóa đơn")
    app = ChiTietHDGUI(root)
    root.mainloop()
