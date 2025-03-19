import tkinter as tk
from tkinter import ttk, messagebox

from DSNhanVien import DSNhanVien
from NhanVien import NhanVien


class NhanVienGUI:

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

        self.dsNhanVien = DSNhanVien()  # KẾT NỐI DATABASE
        self.taoGiaoDien()

        # Mặc định hiển thị danh sách nhân viên
        self.hienThiDS()

        # cờ trạng thái thao tác
        self.thanhCong = False

    def hienThiDS(self):
        """Hiển thị danh sách nhân viên trong TreeView"""
        try:
            dsNhanVien = self.dsNhanVien.danhSachNV()  # Lấy danh sách nhân viên

            # Xóa dữ liệu cũ trong TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Thêm dữ liệu mới vào TreeView
            for nv in dsNhanVien:
                self.tree.insert("", "end", values=(nv.maNV, nv.tenNV, nv.chucVu, nv.luong, nv.diaChi, nv.SĐT))

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

            self.lamMoiForm()  # Reset form khi chuyển giữa các chế độ

            if action == "Thêm nhân viên":
                self.label_thong_bao.config(text="Nhập thông tin nhân viên mới", fg="blue")
                self.entry_maNV.config(state="normal")
                self.btn_luu.config(state="normal")


            elif action == "Sửa thông tin nhân viên":
                self.label_thong_bao.config(text="Chọn nhân viên từ danh sách để sửa", fg="blue")
                self.entry_maNV.config(state="readonly")
                self.btn_luu.config(state="normal")

                if hasattr(self, "frame_form"):
                    self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

                    for widget in self.frame_form.winfo_children():
                        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
                            widget.grid_configure(sticky="ew")

                for widget in self.parent.grid_slaves():
                    grid_info = widget.grid_info()
                    if int(grid_info.get('row', -1)) > 0 and widget != self.frame_form:
                        widget.grid_forget()

                if hasattr(self, "btn_lam_moi") and self.btn_lam_moi.winfo_exists():
                    self.btn_lam_moi.pack_forget()

                if hasattr(self, "btn_luu") and self.btn_luu.winfo_exists():
                    self.btn_luu.pack_forget()

                self.frame_suaNV = tk.Frame(self.parent)
                self.btn_xac_nhan = tk.Button(self.frame_suaNV, text="Xác nhận sửa",
                                              command=self.suaNhanVien, bg="green", fg="white",
                                              font=("Arial", 10, "bold"))
                self.btn_xac_nhan.pack(side=tk.LEFT, padx=5, pady=5)

                self.btn_huy_sua = tk.Button(self.frame_suaNV, text="Hủy",
                                             command=self.lamMoiForm, bg="red", fg="white",
                                             font=("Arial", 10, "bold"))
                self.btn_huy_sua.pack(side=tk.LEFT, padx=5, pady=5)

                self.frame_suaNV.grid(row=2, column=0, padx=10, pady=5, sticky="w")

                self.separator = tk.Frame(self.parent, height=2, bg="gray")
                self.separator.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

                self.frame_danh_sach.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

                self.parent.grid_rowconfigure(0, weight=0)
                self.parent.grid_rowconfigure(2, weight=0)
                self.parent.grid_rowconfigure(3, weight=0)
                self.parent.grid_rowconfigure(4, weight=1)
                self.parent.grid_columnconfigure(0, weight=1)

                self.btn_luu.config(state="disabled")
                self.btn_huy_sua.config(state="disabled")
                self.btn_xac_nhan.config(state="disabled")

                self.hienThiDS()


            elif action == "Tìm kiếm nhân viên":
                self.label_thong_bao.config(text="Nhập thông tin nhân viên cần tìm", fg="blue")
                self.entry_maNV.config(state="normal")
                self.btn_luu.config(state="disabled")

            # TRANG THAI
            # elif action == "Trạng thái":
            #     self.label_thong_bao.config(text="Trạng thái nhân viên", fg="blue")
            #     self.entry_maNV.config(state="normal")
            #     self.btn_luu.config(state="disabled")

            else:
                self.label_thong_bao.config(text="", fg="black")

    def diChuyen(self, event):
        current_entry = event.widget  # Lấy ô nhập liệu hiện tại
        if current_entry.get().strip() == "":  # Nếu ô đang trống
            return "break"  # Không làm gì cả

        next_widget = current_entry.tk_focusNext()  # Tìm ô tiếp theo
        if isinstance(next_widget, tk.Entry):  # Nếu ô tiếp theo là Entry thì chuyển
            next_widget.focus()
        return "break"  # Ngăn hành động mặc định

    def hienThiFrameSuaNV(self):
        print("Hiển thị frame_suaNV...")
        self.frame_suaNV.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    def anGiaoDien(self):
        """Ẩn giao diện quản lý nhân viên"""
        self.frame.grid_forget()

    def taoGiaoDien(self):
        """Tạo giao diện chung cho quản lý nhân viên"""
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        # Frame nhập thông tin
        self.frame_nhap = ttk.LabelFrame(self.frame)

        self.label_thong_bao = tk.Label(self.frame_nhap, text="", fg="red")
        self.label_thong_bao.grid(row=0, column=0, columnspan=4, pady=5)

        ttk.Label(self.frame_nhap, text="Mã nhân viên:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_maNV = ttk.Entry(self.frame_nhap)
        self.entry_maNV.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Tên nhân viên:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_tenNV = ttk.Entry(self.frame_nhap)
        self.entry_tenNV.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Chức vụ:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_chucVu = ttk.Entry(self.frame_nhap)
        self.entry_chucVu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Lương:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_luong = ttk.Entry(self.frame_nhap)
        self.entry_luong.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Địa chỉ:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_diaChi = ttk.Entry(self.frame_nhap)
        self.entry_diaChi.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="SĐT:").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.entry_SĐT = ttk.Entry(self.frame_nhap)
        self.entry_SĐT.grid(row=4, column=3, padx=5, pady=5, sticky="ew")

        # Frame chứa các nút chức năng
        self.frame_button = tk.Frame(self.frame)

        self.btn_lam_moi = tk.Button(self.frame_button, text="Quay lại", command=self.lamMoiForm, bg="#9E9E9E",
                                     fg="white")
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)

        self.btn_luu = tk.Button(self.frame_button, text="OK", command=self.luuNhanVien, bg="#4CAF50", fg="white")
        self.btn_luu.pack(side=tk.LEFT, padx=5)
        # Tạo frame chứa các nút sửa nếu chưa có
        self.frame_suaNV = tk.Frame(self.parent)
        # Nút Hủy sửa
        self.btn_huy_sua = tk.Button(self.frame_suaNV, text="Hủy sửa",
                                     command=self.lamMoiForm, bg="red", fg="white")
        self.btn_huy_sua.pack(side="left", padx=5, pady=5)
        # Nút Xác nhận sửa
        self.btn_xac_nhan = tk.Button(self.frame_suaNV, text="Xác nhận sửa",
                                      command=self.suaNhanVien, bg="green", fg="white")
        self.btn_xac_nhan.pack(side="left", padx=5, pady=5)
        # Frame hiển thị danh sách
        self.frame_danh_sach = ttk.LabelFrame(self.frame, text="Danh sách nhân viên")

        # Tạo Treeview để hiển thị danh sách
        self.tree = ttk.Treeview(self.frame_danh_sach, columns=("maNV", "tenNV", "chucVu", "luong", "diaChi", "SĐT"),
                                 show="headings", height=15)
        self.tree.heading("maNV", text="Mã nhân viên")
        self.tree.heading("tenNV", text="Tên nhân viên")
        self.tree.heading("chucVu", text="Chức vụ")
        self.tree.heading("luong", text="Lương")
        self.tree.heading("diaChi", text="Địa chỉ")
        self.tree.heading("SĐT", text="SĐT")

        # Thiết lập độ rộng cột
        self.tree.column("maNV", width=100)
        self.tree.column("tenNV", width=200)
        self.tree.column("chucVu", width=150)
        self.tree.column("luong", width=100)
        self.tree.column("diaChi", width=200)
        self.tree.column("SĐT", width=120)

        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(self.frame_danh_sach, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_danh_sach, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sắp xếp các thành phần
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Bắt sự kiện khi chọn một nhân viên trong danh sách
        self.tree.bind("<<TreeviewSelect>>", self.chonNV)

        # Frame hiển thị trạng thái (sẽ được tạo khi cần)
        # self.frame_trang_thai = None

        # Gán sự kiện khi nhấn Enter để di chuyển đến ô tiếp theo
        entries = [self.entry_maNV, self.entry_tenNV, self.entry_chucVu, self.entry_luong, self.entry_diaChi,
                   self.entry_SĐT]
        for entry in entries:
            entry.bind("<Return>", self.diChuyen)

    def chonNV(self, event):
        """Xử lý sự kiện khi chọn một nhân viên trong danh sách"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")

            # Hiển thị thông tin nhân viên được chọn lên form
            self.entry_maNV.config(state="normal")  # mo khoa tam thoi
            self.entry_maNV.delete(0, tk.END)
            self.entry_maNV.insert(0, values[0])
            self.entry_maNV.config(state="readonly")  # khoa lai

            self.entry_tenNV.delete(0, tk.END)
            self.entry_tenNV.insert(0, values[1])

            self.entry_chucVu.delete(0, tk.END)
            self.entry_chucVu.insert(0, values[2])

            self.entry_luong.delete(0, tk.END)
            self.entry_luong.insert(0, values[3])

            self.entry_diaChi.delete(0, tk.END)
            self.entry_diaChi.insert(0, values[4])

            self.entry_SĐT.delete(0, tk.END)
            self.entry_SĐT.insert(0, values[5])

    def luuNhanVien(self):
        """Lưu thông tin nhân viên mới"""
        try:
            maNV = self.entry_maNV.get()
            tenNV = self.entry_tenNV.get()
            chucVu = self.entry_chucVu.get()
            luong = self.entry_luong.get()
            diaChi = self.entry_diaChi.get()
            SĐT = self.entry_SĐT.get()

            if not all([maNV, tenNV, chucVu, luong, diaChi, SĐT]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            nvien = NhanVien(maNV, tenNV, chucVu, luong, diaChi, SĐT)
            if self.dsNhanVien.themNV(nvien):
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Thêm nhân viên thành công!", fg="green")
            else:
                self.label_thong_bao.config(text='Lỗi! Không thể thêm nhân viên.', fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi: {str(e)}", fg="red")

    def suaNhanVien(self):
        """Sửa thông tin nhân viên"""
        try:
            maNV = self.entry_maNV.get()
            if not maNV:
                self.label_thong_bao.config(text="Vui lòng chọn nhân viên cần sửa!", fg="red")
                return

            tenNV = self.entry_tenNV.get()
            chucVu = self.entry_chucVu.get()
            luong = self.entry_luong.get()
            diaChi = self.entry_diaChi.get()
            SĐT = self.entry_SĐT.get()

            if not all([tenNV, chucVu, luong, diaChi, SĐT]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            # Xác nhận trước khi sửa
            confirm = messagebox.askyesno("Xác nhận sửa",
                                          f"Bạn có chắc chắn muốn sửa thông tin nhân viên có mã {maNV}?")
            if not confirm:
                return
            # Sử dụng phương thức suaNV với kwargs
            self.dsNhanVien.suaNV(maNV, tenNV=tenNV, chucVu=chucVu, luong=luong, diaChi=diaChi, SĐT=SĐT)
            self.hienThiDS()
            self.lamMoiForm()
            self.label_thong_bao.config(text="Sửa thông tin nhân viên thành công!", fg="green")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi sửa nhân viên: {str(e)}", fg="red")

    def xoaNhanVien(self):
        """Xóa nhân viên"""
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                self.label_thong_bao.config(text="Vui lòng chọn nhân viên cần xóa!", fg="red")
                return

            item = selected_items[0]
            maNV = self.tree.item(item, "values")[0]

            # Hiển thị hộp thoại xác nhận
            confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa nhân viên có mã {maNV}?")
            if confirm:
                self.dsNhanVien.xoaNV(maNV)
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Xóa nhân viên thành công!", fg="green")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi xóa nhân viên: {str(e)}", fg="red")

    def timKiemNhanVien(self):
        # Hiển thị giao diện tìm kiếm
        self.hienThi("Tìm kiếm nhân viên")

    def timTheoMa(self):
        """Tìm kiếm nhân viên theo mã"""
        try:
            maNV = self.entry_maNV.get()
            if not maNV:
                self.label_thong_bao.config(text="Vui lòng nhập mã nhân viên cần tìm!", fg="red")
                return

            dsNhanVien = self.dsNhanVien.timKiemNV(maNV=maNV)

            # Xóa dữ liệu cũ trong tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Hiển thị kết quả tìm kiếm
            if dsNhanVien:
                for nvien in dsNhanVien:
                    self.tree.insert("", "end", values=(
                        nvien.maNV, nvien.tenNV, nvien.chucVu, nvien.luong, nvien.diaChi, nvien.SĐT))
                self.label_thong_bao.config(text=f"Đã tìm thấy {len(dsNhanVien)} nhân viên", fg="green")
            else:
                self.label_thong_bao.config(text="Không tìm thấy nhân viên nào!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi tìm kiếm: {str(e)}", fg="red")

    def timTheoTen(self):
        """Tìm kiếm nhân viên theo tên"""
        try:
            tenNV = self.entry_tenNV.get()
            if not tenNV:
                self.label_thong_bao.config(text="Vui lòng nhập tên nhân viên cần tìm!", fg="red")
                return

            dsNhanVien = self.dsNhanVien.timKiemNV(tenNV=tenNV)

            # Xóa dữ liệu cũ trong tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Hiển thị kết quả tìm kiếm
            if dsNhanVien:
                for nvien in dsNhanVien:
                    self.tree.insert("", "end", values=(
                        nvien.maNV, nvien.tenNV, nvien.chucVu, nvien.luong, nvien.diaChi, nvien.SĐT))
                self.label_thong_bao.config(text=f"Đã tìm thấy {len(dsNhanVien)} nhân viên", fg="green")
            else:
                self.label_thong_bao.config(text="Không tìm thấy nhân viên nào!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi tìm kiếm: {str(e)}", fg="red")

    def lamMoiForm(self):
        """Làm mới form nhập liệu"""
        self.entry_maNV.delete(0, tk.END)
        self.entry_tenNV.delete(0, tk.END)
        self.entry_chucVu.delete(0, tk.END)
        self.entry_luong.delete(0, tk.END)
        self.entry_diaChi.delete(0, tk.END)
        self.entry_SĐT.delete(0, tk.END)
        self.label_thong_bao.grid()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý nhân viên")
    app = NhanVienGUI(root)
    root.mainloop()
