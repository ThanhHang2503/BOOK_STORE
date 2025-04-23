import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


from .DSCTHoaDon import DSCTHoaDon
from .DSHoaDon import DSHoaDon
from HOADON.ChiTietHD import ChiTietHD
from .HoaDon import HoaDon


class HoaDonGUI:
    def __init__(self, parent):
        self.master = None
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Khởi tạo các frame con cho từng chức năng
        self.them_frame = ttk.Frame(self.frame)
        self.sua_frame = ttk.Frame(self.frame)
        self.timKiem_frame = ttk.Frame(self.frame)
        self.hienThiDS_frame = ttk.Frame(self.frame)
        self.trangThai_frame = ttk.Frame(self.frame)

        self.dsHoaDon = DSHoaDon()  # KẾT NỐI DATABASE
        self.taoGiaoDien()

        # Mặc định hiển thị danh sách hóa đơn
        self.hienThiDS()

        # cờ trạng thái thao tác
        self.thanhCong = False

        # Biến lưu trạng thái tìm kiếm - không chọn mặc định
        self.search_type = tk.StringVar(value="")

        # Biến lưu trạng thái radio button đã chọn
        self.selected_radio = None

    def hienThiDS(self):
        """Hiển thị danh sách hóa đơn trong TreeView"""
        try:
            dsHoaDon = self.dsHoaDon.danhSachHD()  # Lấy danh sách hóa đơn

            # Xóa dữ liệu cũ trong TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Thêm dữ liệu mới vào TreeView
            for hd in dsHoaDon:
                self.tree.insert("", "end", values=(
                    hd.maHD, hd.maNV, hd.maKH, hd.tongTien, hd.ngayTaoHD))

            # Đảm bảo frame hiển thị đúng
            self.frame_danh_sach.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
            self.frame_danh_sach.tkraise()  # Đưa frame danh sách lên trên cùng

        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi hiển thị danh sách: {str(e)}", fg="red")


    def hienThi(self, action):
        # Ẩn mọi widget trong frame chính
        for widget in self.frame.winfo_children():
            widget.grid_forget()

        # Hiển thị khung chính
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Mặc định hiển thị nút làm mới và lưu
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)
        self.btn_luu.pack(side=tk.LEFT, padx=5)
        self.btn_luu.config(state="normal")

        if action=="Hiển thị hóa đơn":
            # Chỉ hiện danh sách hóa đơn
            self.frame_danh_sach.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.hienThiDS()

        elif action=="Tìm kiếm hóa đơn":
            # Ẩn form nhập hiện tại
            for widget in self.frame_nhap.winfo_children():
                widget.grid_forget()

            # Hiển thị lại frame nhập, tạo giao diện tìm kiếm
            self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")
            self.taoGiaoDienTimKiem()

            # Ẩn các nút không liên quan
            self.btn_luu.pack_forget()
            self.btn_lam_moi.pack_forget()

        else:
            # Các chức năng tạo, sửa hóa đơn

            # Ẩn khung tìm kiếm nếu đang tồn tại
            if hasattr(self, "search_frame"):
                self.search_frame.grid_forget()

            # Tạo lại form đầy đủ
            self.taoGiaoDien()
            self.lamMoiForm()

            self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")

            if action=="Tạo hóa đơn":
                self.label_thong_bao.config(text="Nhập thông tin hóa đơn mới", fg="blue")
                self.entry_maHD.config(state="normal")
                self.btn_luu.config(state="normal")

            elif action=="Sửa hóa đơn":
                self.label_thong_bao.config(text="Chọn hóa đơn từ danh sách để sửa", fg="blue")
                self.entry_maHD.config(state="readonly")

                # Hiện form sửa nếu có
                if hasattr(self, "frame_form"):
                    self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                    for widget in self.frame_form.winfo_children():
                        if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
                            widget.grid_configure(sticky="ew")

                # Ẩn tất cả widget sau dòng thứ 1 (form button là dòng 1)
                for widget in self.frame.winfo_children():
                    grid_info = widget.grid_info()
                    if int(grid_info.get('row', -1)) > 1:
                        widget.grid_forget()

                # Ẩn các nút mặc định
                self.btn_lam_moi.pack_forget()
                self.btn_luu.pack_forget()

                # Frame chứa nút xác nhận/hủy sửa
                self.frame_suaHD = tk.Frame(self.frame)
                self.btn_huy_sua = tk.Button(self.frame_suaHD, text="Hủy",
                    command=self.lamMoiForm, bg="red", fg="white",
                    font=("Arial", 10, "bold"))
                self.btn_huy_sua.pack(side=tk.LEFT, padx=5, pady=5)

                self.btn_xac_nhan = tk.Button(self.frame_suaHD, text="Xác nhận sửa",
                    command=self.suaHoaDon, bg="green", fg="white",
                    font=("Arial", 10, "bold"))
                self.btn_xac_nhan.pack(side=tk.LEFT, padx=5, pady=5)

                self.frame_suaHD.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

                # Separator
                self.separator = tk.Frame(self.frame, height=2, bg="gray")
                self.separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

                # Danh sách hóa đơn
                self.frame_danh_sach.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
                self.hienThiDS()  # Load danh sách hóa đơn

                # Cấu hình lại layout
                self.frame.grid_rowconfigure(0, weight=0)
                self.frame.grid_rowconfigure(2, weight=0)
                self.frame.grid_rowconfigure(3, weight=0)
                self.frame.grid_rowconfigure(4, weight=1)
                self.frame.grid_columnconfigure(0, weight=1)

                # Vô hiệu hóa nút lưu (vì đã có xác nhận sửa riêng)
                self.btn_luu.config(state="disabled")

            else:
                # Trạng thái mặc định
                self.label_thong_bao.config(text="", fg="black")

    def taoGiaoDienTimKiem(self):
        """Tạo giao diện tìm kiếm theo mẫu mới"""
        # Xóa các widget cũ trong frame nhập
        for widget in self.frame_nhap.winfo_children():
            widget.grid_forget()

        # Reset biến tìm kiếm
        self.search_type.set("")
        self.selected_radio = None

        # Tạo frame chính với padding nhưng không có viền
        main_frame = tk.Frame(self.frame_nhap, bg="#f5f5f5")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_nhap.columnconfigure(0, weight=1)
        self.frame_nhap.rowconfigure(0, weight=1)

        # Tạo frame chứa giao diện tìm kiếm không có viền
        self.search_frame = tk.Frame(main_frame, bg="white")
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=0)

        # Tiêu đề
        title_label = tk.Label(
            self.search_frame,
            text="Tìm kiếm hóa đơn",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#87CEEB"
        )
        title_label.grid(row=0, column=0, pady=(20, 15), sticky="ew")
        self.search_frame.columnconfigure(0, weight=1)

        # Frame chứa radio buttons
        radio_frame = tk.Frame(self.search_frame, bg="white")
        radio_frame.grid(row=1, column=0, pady=10, sticky="ew")

        # Tạo custom radio buttons
        self.radio_id_hd_var = tk.IntVar(value=0)
        self.radio_id_kh_var = tk.IntVar(value=0)

        style = ttk.Style()
        style.configure("Custom.TRadiobutton",
            background="white",
            foreground="black",
            font=("Arial", 15),
            indicatorcolor="black",
            indicatordiameter=12,
            indicatormargin=4,
            relief="flat")

        # Frame cho radio ID
        id_radio_frame = tk.Frame(radio_frame, bg="white")
        id_radio_frame.grid(row=0, column=0, padx=20)

        self.radio_id = ttk.Radiobutton(
            id_radio_frame,
            text="Tìm theo mã hóa đơn",
            variable=self.search_type,
            value="id_hd",
            style="Custom.TRadiobutton",
            command=lambda: self.toggleSearchOption("id_hd")
        )
        self.radio_id.grid(row=0, column=0)

        # Frame cho radio Name
        name_radio_frame = tk.Frame(radio_frame, bg="white")
        name_radio_frame.grid(row=0, column=1, padx=20)

        self.radio_name = ttk.Radiobutton(
            name_radio_frame,
            text="Tìm theo mã khách hàng",
            variable=self.search_type,
            value="id_kh",
            style="Custom.TRadiobutton",
            command=lambda: self.toggleSearchOption("id_kh")
        )
        self.radio_name.grid(row=0, column=0)

        # Căn giữa các radio buttons trong radio_frame
        radio_frame.grid_columnconfigure(0, weight=1)
        radio_frame.grid_columnconfigure(1, weight=1)

        # Frame chứa input và nút tìm kiếm (ẩn ban đầu)
        self.input_frame = tk.Frame(self.search_frame, bg="white")

        # Input field - không có placeholder
        self.search_entry = tk.Entry(
            self.input_frame,
            font=("Arial", 12),
            bd=1,
            relief=tk.SOLID,
            width=40
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), ipady=5, sticky="ew")

        # Nút tìm kiếm
        self.search_button = tk.Button(
            self.input_frame,
            text="Tìm kiếm",
            bg="#212121",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            padx=15,
            pady=5,
            command=self.thucHienTimKiem
        )
        self.search_button.grid(row=0, column=1, padx=5)
        self.input_frame.columnconfigure(0, weight=1)

        # Frame hiển thị kết quả tìm kiếm
        self.result_frame = tk.Frame(main_frame, bg="white")

        # Label thông báo kết quả
        self.result_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 12),
            fg="green",
            bg="#f5f5f5"
        )
        self.result_label.grid(row=1, column=0, pady=10, sticky="ew")

        # Ẩn danh sách hóa đơn
        if hasattr(self, "frame_danh_sach"):
            self.frame_danh_sach.grid_forget()

    def toggleSearchOption(self, option):
        """Xử lý khi chọn hoặc bỏ chọn radio button"""
        if option == "id_hd":
            # Nếu đã chọn radio ID trước đó, bỏ chọn nó
            if self.selected_radio == "id_hd":
                self.radio_id_hd_var.set(0)
                self.selected_radio = None
                self.search_type.set("")
                self.input_frame.grid_forget()
                return

            # Nếu chưa chọn hoặc đã chọn radio khác, chọn radio ID
            self.radio_id_hd_var.set(1)
            self.radio_id_kh_var.set(0)
            self.selected_radio = "id_hd"
            self.search_type.set("id_hd")

        elif option == "id_kh":
            # Nếu đã chọn radio Name trước đó, bỏ chọn nó
            if self.selected_radio == "id_kh":
                self.radio_id_kh_var.set(0)
                self.selected_radio = None
                self.search_type.set("")
                self.input_frame.grid_forget()
                return

            # Nếu chưa chọn hoặc đã chọn radio khác, chọn radio Name
            self.radio_id_kh_var.set(1)
            self.radio_id_hd_var.set(0)
            self.selected_radio = "id_kh"
            self.search_type.set("id_kh")

        # Hiển thị input field nếu đã chọn một option
        if self.selected_radio:
            # Xóa nội dung cũ trong ô nhập liệu
            self.search_entry.delete(0, tk.END)
            # Hiển thị ô nhập liệu
            self.input_frame.grid(row=2, column=0, pady=15, padx=20, sticky="ew")
            # Đặt focus vào ô nhập liệu
            self.search_entry.focus_set()
        else:
            self.input_frame.grid_forget()

        # Xóa kết quả tìm kiếm cũ
        if hasattr(self, "result_frame") and self.result_frame.winfo_exists():
            self.result_frame.grid_forget()

        # Xóa thông báo
        if hasattr(self, "result_label") and self.result_label.winfo_exists():
            self.result_label.config(text="")

    def thucHienTimKiem(self):
        """Thực hiện tìm kiếm theo loại đã chọn"""
        search_text = self.search_entry.get()

        # Kiểm tra nếu ô nhập liệu trống
        if not search_text.strip():
            self.result_label.config(text="Vui lòng nhập thông tin tìm kiếm!", fg="red")
            return

        # Xóa kết quả tìm kiếm cũ
        if hasattr(self, "result_frame") and self.result_frame.winfo_exists():
            self.result_frame.grid_forget()

        # Thực hiện tìm kiếm
        try:
            if self.search_type.get() == "id_hd":
                # Tìm kiếm chính xác theo mã
                hd = self.dsHoaDon.timKiem(search_text)
                dsHoaDon = [hd] if hd else []
            else:
                # Tìm kiếm theo mã khách hàng
                dsHoaDon = self.dsHoaDon.timKiem(maKH=search_text)
                if dsHoaDon is None:
                    
                    dsHoaDon = []

            # Kiểm tra kết quả
            if not dsHoaDon:
                self.result_label.config(text="Không tìm thấy hóa đơn", fg="red")
                return

            # Hiển thị danh sách hóa đơn tìm được
            self.hienThiDSKetQua(dsHoaDon)
            self.result_label.config(text=f"Đã tìm thấy {len(dsHoaDon)} hóa đơn", fg="green")

        except Exception as e:
            self.result_label.config(text="Không tìm thấy hóa đơn", fg="red")

    def hienThiDSKetQua(self, dsHoaDon):
        """Hiển thị danh sách kết quả tìm kiếm"""
        # Tạo frame kết quả
        self.result_frame = tk.Frame(self.frame_nhap, bg="white")
        self.result_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Tạo Treeview để hiển thị kết quả
        columns = ("maHD", "maNV", "maKH", "tongTien", "ngayTaoHD")
        tree = ttk.Treeview(self.result_frame, columns=columns, show="headings")
        
        # Đặt tiêu đề cột
        tree.heading("maHD", text="Mã hóa đơn")
        tree.heading("maNV", text="Mã nhân viên")
        tree.heading("maKH", text="Mã khách hàng")
        tree.heading("tongTien", text="Tổng tiền")
        tree.heading("ngayTaoHD", text="Ngày tạo")

        # Thêm dữ liệu vào Treeview
        for hd in dsHoaDon:
            tree.insert("", "end", values=(
                hd.maHD,
                hd.maNV,
                hd.maKH,
                hd.tongTien,
                hd.ngayTaoHD
            ))

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Đặt layout
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cấu hình frame
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)

    def diChuyen(self, event):
        current_entry = event.widget  # Lấy ô nhập liệu hiện tại
        if current_entry.get().strip() == "":  # Nếu ô đang trống
            return "break"  # Không làm gì cả

        next_widget = current_entry.tk_focusNext()  # Tìm ô tiếp theo
        if isinstance(next_widget, tk.Entry):  # Nếu ô tiếp theo là Entry thì chuyển
            next_widget.focus()
        return "break"  # Ngăn hành động mặc định

    def hienThiFrameSuaHD(self):
        print("Hiển thị frame_suaHD...")
        self.frame_suaHD.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")  # di chuyển xuống row 2, thêm columnspan

    def anGiaoDien(self):
        """Ẩn giao diện quản lý hóa đơn"""
        self.frame.grid_forget()

    def taoGiaoDien(self):
        """Tạo giao diện chung cho quản lý hóa đơn"""
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        # Frame nhập thông tin
        self.frame_nhap = ttk.LabelFrame(self.frame)

        self.label_thong_bao = tk.Label(self.frame_nhap, text="", fg="red")
        self.label_thong_bao.grid(row=0, column=0, columnspan=4, pady=5)

        ttk.Label(self.frame_nhap, text="Mã hóa đơn:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_maHD = ttk.Entry(self.frame_nhap)
        self.entry_maHD.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Mã nhân viên:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_maNV = ttk.Entry(self.frame_nhap)
        self.entry_maNV.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Mã khách hàng:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_maKH = ttk.Entry(self.frame_nhap)
        self.entry_maKH.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Tổng tiền:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_tongTien = ttk.Entry(self.frame_nhap)
        self.entry_tongTien.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Ngày tạo:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_ngayTao = ttk.Entry(self.frame_nhap, state="readonly")
        self.entry_ngayTao.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Frame chứa các nút chức năng
        self.frame_button = tk.Frame(self.frame)

        self.btn_lam_moi = tk.Button(self.frame_button, text="Quay lại", command=self.lamMoiForm, bg="#9E9E9E",
            fg="white")
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)
        self.btn_luu = tk.Button(self.frame_button, text="OK", command=self.luuHoaDon, bg="#4CAF50", fg="white")
        self.btn_luu.pack(side=tk.LEFT, padx=5)

        # Tạo frame chứa các nút sửa nếu chưa có
        self.frame_suaHD = tk.Frame(self.parent)

        # Frame hiển thị danh sách
        self.frame_danh_sach = ttk.LabelFrame(self.frame, text="Danh sách hóa đơn")

        # Tạo Treeview để hiển thị danh sách
        self.tree = ttk.Treeview(self.frame_danh_sach, columns=(
        "maHD", "maNV", "maKH", "tongTien", "ngayTaoHD", "chiTiet"),
            show="headings", height=15)
        self.tree.heading("maHD", text="Mã hóa đơn")
        self.tree.heading("maNV", text="Mã nhân viên")
        self.tree.heading("maKH", text="Mã khách hàng")
        self.tree.heading("tongTien", text="Tổng tiền")
        self.tree.heading("ngayTaoHD", text="Ngày tạo")
        self.tree.heading("chiTiet", text="Chi tiết")

        # Thiết lập độ rộng cột
        self.tree.column("maHD", width=100)
        self.tree.column("maNV", width=100)
        self.tree.column("maKH", width=100)
        self.tree.column("tongTien", width=150)
        self.tree.column("ngayTaoHD", width=150)
        self.tree.column("chiTiet", width=100)

        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(self.frame_danh_sach, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_danh_sach, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sắp xếp các thành phần
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Bắt sự kiện khi chọn một hóa đơn trong danh sách
        self.tree.bind("<<TreeviewSelect>>", self.chonHD)
        self.tree.bind("<Double-1>", self.xemChiTietHD)

        # Frame hiển thị trạng thái (sẽ được tạo khi cần)
        self.frame_trang_thai = None

        # Gán sự kiện khi nhấn Enter để di chuyển đến ô tiếp theo
        entries = [self.entry_maHD, self.entry_maNV, self.entry_maKH, self.entry_tongTien, self.entry_ngayTao]
        for entry in entries:
            entry.bind("<Return>", self.diChuyen)

    def chonHD(self, event):
        """Xử lý sự kiện khi chọn một hóa đơn trong danh sách"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")

            # Hiển thị thông tin hóa đơn được chọn lên form
            if self.entry_maHD and self.entry_maHD.winfo_exists():
                self.entry_maHD.config(state="normal")

            self.entry_maHD.delete(0, tk.END)
            self.entry_maHD.insert(0, values[0])
            self.entry_maHD.config(state="readonly")  # khoa lai

            self.entry_maNV.delete(0, tk.END)
            self.entry_maNV.insert(0, values[1])

            self.entry_maKH.delete(0, tk.END)
            self.entry_maKH.insert(0, values[2])

            self.entry_tongTien.delete(0, tk.END)
            self.entry_tongTien.insert(0, values[3])

            self.entry_ngayTao.config(state="normal")
            self.entry_ngayTao.delete(0, tk.END)
            self.entry_ngayTao.insert(0, values[4])
            self.entry_ngayTao.config(state="readonly")

    def luuHoaDon(self):
        """Lưu thông tin hóa đơn mới"""
        try:
            maHD = self.entry_maHD.get().strip()
            maNV = self.entry_maNV.get().strip()
            maKH = self.entry_maKH.get().strip()
            tongTien = self.entry_tongTien.get().strip()

            if not all([maHD, maNV, maKH, tongTien]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            try:
                tongTien = float(tongTien)
            except ValueError:
                self.label_thong_bao.config(text="Tổng tiền phải là số!", fg="red")
                return

            # Tạo hóa đơn mới
            hd = HoaDon(
                maHD=maHD,
                maNV=maNV,
                maKH=maKH,
                tongTien=tongTien,
                ngayTaoHD=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            if self.dsHoaDon.them(hd):
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Thêm hóa đơn thành công!", fg="green")
            else:
                self.label_thong_bao.config(text=f'Lỗi! Mã hóa đơn {maHD} đã tồn tại.', fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi: {str(e)}", fg="red")

    def suaHoaDon(self):
        """Sửa thông tin hóa đơn"""
        try:
            maHD = self.entry_maHD.get().strip()
            if not maHD:
                self.label_thong_bao.config(text="Vui lòng chọn hóa đơn cần sửa!", fg="red")
                return

            maNV = self.entry_maNV.get().strip()
            maKH = self.entry_maKH.get().strip()
            tongTien = self.entry_tongTien.get().strip()

            if not all([maNV, maKH, tongTien]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            try:
                tongTien = float(tongTien)
            except ValueError:
                self.label_thong_bao.config(text="Tổng tiền phải là số!", fg="red")
                return

            # Xác nhận trước khi sửa
            confirm = messagebox.askyesno("Xác nhận sửa", f"Bạn có chắc muốn sửa thông tin hóa đơn có mã {maHD}?")
            if not confirm:
                return

            # Cập nhật hóa đơn
            if self.dsHoaDon.sua(maHD, maNV, maKH, tongTien):
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Sửa thông tin hóa đơn thành công!", fg="green")
            else:
                self.label_thong_bao.config(text=f"Không tìm thấy hóa đơn có mã {maHD}!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi sửa hóa đơn: {str(e)}", fg="red")

    def xoaHoaDon(self):
        """Xóa hóa đơn"""
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                self.label_thong_bao.config(text="Vui lòng chọn hóa đơn cần xóa!", fg="red")
                return

            item = selected_items[0]
            maHD = self.tree.item(item, "values")[0]

            # Hiển thị hộp thoại xác nhận
            confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa hóa đơn có mã {maHD}?")
            if confirm:
                if self.dsHoaDon.xoa(maHD):
                    self.hienThiDS()
                    self.lamMoiForm()
                    self.label_thong_bao.config(text="Xóa hóa đơn thành công!", fg="green")
                else:
                    self.label_thong_bao.config(text=f"Không tìm thấy hóa đơn có mã {maHD}!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi xóa hóa đơn: {str(e)}", fg="red")

    def lamMoiForm(self):
        """Làm mới form nhập liệu"""
        # Check if the widgets exist before trying to clear them
        if hasattr(self, "entry_maHD") and self.entry_maHD.winfo_exists():
            self.entry_maHD.config(state="normal")
            self.entry_maHD.delete(0, tk.END)
        if hasattr(self, "entry_maNV") and self.entry_maNV.winfo_exists():
            self.entry_maNV.delete(0, tk.END)
        if hasattr(self, "entry_maKH") and self.entry_maKH.winfo_exists():
            self.entry_maKH.delete(0, tk.END)
        if hasattr(self, "entry_tongTien") and self.entry_tongTien.winfo_exists():
            self.entry_tongTien.delete(0, tk.END)
            self.entry_tongTien.insert(0, "0")
        if hasattr(self, "entry_ngayTao") and self.entry_ngayTao.winfo_exists():
            self.entry_ngayTao.config(state="normal")
            self.entry_ngayTao.delete(0, tk.END)
            self.entry_ngayTao.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.entry_ngayTao.config(state="readonly")
        if hasattr(self, "label_thong_bao") and self.label_thong_bao.winfo_exists():
            self.label_thong_bao.config(text="")

    def xemChiTietHD(self, event):
        """Xử lý sự kiện khi double click vào cột chi tiết"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        values = self.tree.item(item, "values")
        maHD = values[0]  # Lấy mã hóa đơn

        # Tạo cửa sổ mới để hiển thị chi tiết hóa đơn
        chi_tiet_window = tk.Toplevel(self.parent)
        chi_tiet_window.title(f"Chi tiết hóa đơn {maHD}")
        chi_tiet_window.geometry("800x600")
        
        # Center the window
        window_width = 800
        window_height = 600
        screen_width = chi_tiet_window.winfo_screenwidth()
        screen_height = chi_tiet_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        chi_tiet_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Tạo frame chính và căn giữa
        main_frame = ttk.Frame(chi_tiet_window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Tạo frame chứa chi tiết hóa đơn
        frame_chi_tiet = ttk.LabelFrame(main_frame, text="Danh sách chi tiết hóa đơn")
        frame_chi_tiet.pack(fill="both", expand=True, padx=10, pady=10)

        # Tạo Treeview hiển thị chi tiết
        columns = ("maSP", "soLuong", "donGia", "thanhTien")
        tree_chi_tiet = ttk.Treeview(frame_chi_tiet, columns=columns, show="headings")
        tree_chi_tiet.heading("maSP", text="Mã sản phẩm")
        tree_chi_tiet.heading("soLuong", text="Số lượng")
        tree_chi_tiet.heading("donGia", text="Đơn giá")
        tree_chi_tiet.heading("thanhTien", text="Thành tiền")

        # Thiết lập độ rộng cột
        tree_chi_tiet.column("maSP", width=150, anchor="center")
        tree_chi_tiet.column("soLuong", width=100, anchor="center")
        tree_chi_tiet.column("donGia", width=150, anchor="center")
        tree_chi_tiet.column("thanhTien", width=150, anchor="center")

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(frame_chi_tiet, orient="vertical", command=tree_chi_tiet.yview)
        tree_chi_tiet.configure(yscrollcommand=scrollbar.set)

        # Sắp xếp các thành phần
        tree_chi_tiet.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame chứa các nút chức năng
        frame_button = ttk.Frame(main_frame)
        frame_button.pack(fill="x", padx=10, pady=10)

        # Tạo các nút chức năng
        btn_them = ttk.Button(frame_button, text="Thêm", command=lambda: self.themChiTiet(maHD, tree_chi_tiet))
        btn_them.pack(side="left", padx=5)

        btn_sua = ttk.Button(frame_button, text="Sửa", command=lambda: self.suaChiTiet(maHD, tree_chi_tiet))
        btn_sua.pack(side="left", padx=5)

        btn_xoa = ttk.Button(frame_button, text="Xóa", command=lambda: self.xoaChiTiet(maHD, tree_chi_tiet))
        btn_xoa.pack(side="left", padx=5)

        # Tải dữ liệu chi tiết hóa đơn
        self.taiChiTietHD(maHD, tree_chi_tiet)

    def taiChiTietHD(self, maHD, tree):
        """Tải dữ liệu chi tiết hóa đơn vào Treeview"""
        # Xóa dữ liệu cũ
        for item in tree.get_children():
            tree.delete(item)

        # Tải dữ liệu mới
        dsCTHD = DSCTHoaDon()
        chi_tiet = dsCTHD.timKiem(maHD=maHD)
        for ct in chi_tiet:
            tree.insert("", "end", values=(
                ct.maSP,
                ct.soLuongSP,
                ct.donGia,
                ct.thanhTien
            ))

    def themChiTiet(self, maHD, tree):
        """Thêm chi tiết hóa đơn mới"""
        # Tạo cửa sổ nhập liệu
        them_window = tk.Toplevel(self.parent)
        them_window.title("Thêm chi tiết hóa đơn")
        them_window.geometry("400x300")
        
        # Center the window
        window_width = 400
        window_height = 300
        screen_width = them_window.winfo_screenwidth()
        screen_height = them_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        them_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Tạo frame chính và căn giữa
        main_frame = ttk.Frame(them_window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Tạo các trường nhập liệu
        frame_nhap = ttk.LabelFrame(main_frame, text="Nhập thông tin chi tiết")
        frame_nhap.pack(fill="both", expand=True, padx=10, pady=10)

        # Mã sản phẩm
        ttk.Label(frame_nhap, text="Mã sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_maSP = ttk.Entry(frame_nhap)
        entry_maSP.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Số lượng
        ttk.Label(frame_nhap, text="Số lượng:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_soLuong = ttk.Entry(frame_nhap)
        entry_soLuong.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Đơn giá
        ttk.Label(frame_nhap, text="Đơn giá:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_donGia = ttk.Entry(frame_nhap)
        entry_donGia.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        def luu():
            try:
                maSP = entry_maSP.get().strip()
                soLuong = int(entry_soLuong.get().strip())
                donGia = float(entry_donGia.get().strip())

                # Tạo chi tiết hóa đơn mới
                ct = ChiTietHD(maHD=maHD, maSP=maSP, soLuong=soLuong, donGia=donGia)
                
                # Lưu vào database
                dsCTHD = DSCTHoaDon()
                if dsCTHD.them(ct):
                    # Cập nhật lại danh sách
                    self.taiChiTietHD(maHD, tree)
                    them_window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không thể thêm chi tiết hóa đơn!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm chi tiết hóa đơn: {str(e)}")

        # Nút lưu
        btn_luu = ttk.Button(main_frame, text="Lưu", command=luu)
        btn_luu.pack(pady=10)

    def suaChiTiet(self, maHD, tree):
        """Sửa chi tiết hóa đơn"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết cần sửa!")
            return

        item = selected_items[0]
        values = tree.item(item, "values")
        maSP = values[0]

        # Tạo cửa sổ sửa
        sua_window = tk.Toplevel(self.parent)
        sua_window.title("Sửa chi tiết hóa đơn")
        sua_window.geometry("400x300")
        
        # Center the window
        window_width = 400
        window_height = 300
        screen_width = sua_window.winfo_screenwidth()
        screen_height = sua_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        sua_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Tạo frame chính và căn giữa
        main_frame = ttk.Frame(sua_window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Tạo các trường nhập liệu
        frame_nhap = ttk.LabelFrame(main_frame, text="Sửa thông tin chi tiết")
        frame_nhap.pack(fill="both", expand=True, padx=10, pady=10)

        # Mã sản phẩm (readonly)
        ttk.Label(frame_nhap, text="Mã sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_maSP = ttk.Entry(frame_nhap)
        entry_maSP.insert(0, values[0])
        entry_maSP.config(state="readonly")
        entry_maSP.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Số lượng
        ttk.Label(frame_nhap, text="Số lượng:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_soLuong = ttk.Entry(frame_nhap)
        entry_soLuong.insert(0, values[1])
        entry_soLuong.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Đơn giá
        ttk.Label(frame_nhap, text="Đơn giá:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_donGia = ttk.Entry(frame_nhap)
        entry_donGia.insert(0, values[2])
        entry_donGia.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        def luu():
            try:
                soLuong = int(entry_soLuong.get().strip())
                donGia = float(entry_donGia.get().strip())

                # Cập nhật chi tiết hóa đơn
                dsCTHD = DSCTHoaDon()
                if dsCTHD.xoa(maHD, maSP):
                    ct = ChiTietHD(maHD=maHD, maSP=maSP, soLuong=soLuong, donGia=donGia)
                    if dsCTHD.them(ct):
                        # Cập nhật lại danh sách
                        self.taiChiTietHD(maHD, tree)
                        sua_window.destroy()
                    else:
                        messagebox.showerror("Lỗi", "Không thể cập nhật chi tiết hóa đơn!")
                else:
                    messagebox.showerror("Lỗi", "Không thể cập nhật chi tiết hóa đơn!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật chi tiết hóa đơn: {str(e)}")

        # Nút lưu
        btn_luu = ttk.Button(main_frame, text="Lưu", command=luu)
        btn_luu.pack(pady=10)

    def xoaChiTiet(self, maHD, tree):
        """Xóa chi tiết hóa đơn"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết cần xóa!")
            return

        item = selected_items[0]
        values = tree.item(item, "values")
        maSP = values[0]

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa chi tiết này?"):
            try:
                dsCTHD = DSCTHoaDon()
                if dsCTHD.xoa(maHD, maSP):
                    # Cập nhật lại danh sách
                    self.taiChiTietHD(maHD, tree)
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa chi tiết hóa đơn!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa chi tiết hóa đơn: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý hóa đơn")
    root.geometry("800x600")
    app = HoaDonGUI(root)
    root.mainloop()
