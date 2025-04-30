import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from .CTPhieuNhapBUSS import CTPhieuNhapBUSS
from .PhieuNhapBUSS import PhieuNhapBUSS


class PhieuNhapGUI:

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_remove()

        # Configure grid weights for centering
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.phieu_nhap_buss = PhieuNhapBUSS()
        self.phieu_nhap_buss.lay_du_lieu_tu_sql()
        self.ctphieu_nhap_buss = CTPhieuNhapBUSS()
        self.ctphieu_nhap_buss.lay_du_lieu_tu_sql()

        # Main container frame for centering
        self.main_container = ttk.Frame(self.frame)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Title frame
        self.frame_title = ttk.Frame(self.main_container)
        self.frame_title.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # Title label with better styling
        # self.title_label = ttk.Label(
        #     self.frame_title,
        #     text="QUẢN LÝ PHIẾU NHẬP",
        #     font=("Arial", 16, "bold")
        # )
        # self.title_label.grid(row=0, column=0, sticky="ew")
        # self.frame_title.grid_columnconfigure(0, weight=1)

        # Content frame
        self.frame_thong_tin = ttk.Frame(self.main_container)
        self.frame_thong_tin.grid(row=1, column=0, sticky="nsew")

        self.hien_thi_them()

    def xoa_thong_tin_frame(self):
        for widget in self.frame_thong_tin.winfo_children():
            widget.destroy()

    def hien_thi_them(self):
        self.xoa_thong_tin_frame()

        # Configure grid weights for centering
        self.frame_thong_tin.grid_columnconfigure(1, weight=1)

        # Create a style for consistent widget appearance
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 10))
        style.configure("Custom.TEntry", font=("Arial", 10))
        style.configure("Custom.TButton", font=("Arial", 10))

        # Labels and entries with consistent styling
        labels = [
            ("Mã Phiếu Nhập", "entry_maPN"),
            ("Ngày Tạo", "entry_ngayTao"),
            ("Mã Nhân Viên", "entry_maNV")
        ]

        for i, (label_text, entry_name) in enumerate(labels):
            label = ttk.Label(self.frame_thong_tin, text=label_text, style="Custom.TLabel")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            
            entry = ttk.Entry(self.frame_thong_tin, width=30, style="Custom.TEntry")
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            setattr(self, entry_name, entry)

        # Set ngayTao to current datetime
        self.entry_ngayTao.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.entry_ngayTao.config(state="disabled")

        # Button with consistent styling
        self.btn_them_phieu_nhap = ttk.Button(
            self.frame_thong_tin, 
            text="Thêm Phiếu Nhập", 
            command=self.them_phieu_nhap,
            style="Custom.TButton"
        )
        self.btn_them_phieu_nhap.grid(row=len(labels), column=0, columnspan=2, pady=20)


    def them_phieu_nhap(self):
        maPN = self.entry_maPN.get()
        ngayTao = self.entry_ngayTao.get()
        maNV = self.entry_maNV.get()
        tongTien = 0  # Khởi tạo tổng tiền là 0

        if not maPN or not ngayTao or not maNV:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        self.phieu_nhap_buss.them(maPN, ngayTao, maNV, tongTien)
        messagebox.showinfo("Thông báo", "Thêm phiếu nhập thành công!")
        self.hien_thi_danh_sach()


    def hien_thi_sua(self):
        self.xoa_thong_tin_frame()
        
        # Configure grid weights for centering
        self.frame_thong_tin.grid_columnconfigure(1, weight=1)
        
        # Create a style for consistent widget appearance
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 10))
        style.configure("Custom.TEntry", font=("Arial", 10))
        style.configure("Custom.TButton", font=("Arial", 10))
        
        # Title
        title_label = ttk.Label(
            self.frame_thong_tin, 
            text="Sửa Phiếu Nhập", 
            font=("Arial", 14, "bold"),
            style="Custom.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="ew")
        
        # Search frame
        search_frame = ttk.Frame(self.frame_thong_tin)
        search_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Nhập Mã Phiếu Nhập:", style="Custom.TLabel").grid(row=0, column=0, padx=5, sticky="w")
        self.entry_maPN = ttk.Entry(search_frame, width=30, style="Custom.TEntry")
        self.entry_maPN.grid(row=0, column=1, padx=5, sticky="ew")
        btn_tim = ttk.Button(
            search_frame, 
            text="Tìm kiếm", 
            command=self.sua_phieu_nhap,
            style="Custom.TButton"
        )
        btn_tim.grid(row=0, column=2, padx=5)

    def sua_phieu_nhap(self):
        ma_pn = self.entry_maPN.get().strip()
        if not ma_pn:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập!")
            return

        phieu_nhap = self.phieu_nhap_buss.tim_kiem(ma_pn)
        if not phieu_nhap:
            messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập!")
            return

        self.xoa_thong_tin_frame()
        
        # Configure grid weights for centering
        self.frame_thong_tin.grid_columnconfigure(1, weight=1)
        
        # Create a style for consistent widget appearance
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 10))
        style.configure("Custom.TEntry", font=("Arial", 10))
        style.configure("Custom.TButton", font=("Arial", 10))
        
        # Title
        title_label = ttk.Label(
            self.frame_thong_tin, 
            text="Sửa Thông Tin Phiếu Nhập", 
            font=("Arial", 14, "bold"),
            style="Custom.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        maPN, ngayTao, maNV, tongTien = phieu_nhap

        # Form fields
        fields = [
            ("Mã Phiếu Nhập:", maPN, True),
            ("Ngày Tạo:", ngayTao, True),
            ("Mã Nhân Viên:", maNV, False)
        ]

        for i, (label_text, value, disabled) in enumerate(fields, start=1):
            ttk.Label(self.frame_thong_tin, text=label_text, style="Custom.TLabel").grid(
                row=i, column=0, padx=10, pady=5, sticky="w"
            )
            entry = ttk.Entry(self.frame_thong_tin, width=30, style="Custom.TEntry")
            entry.insert(0, value)
            if disabled:
                entry.config(state="disabled")
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            setattr(self, f"entry_{label_text.split(':')[0].lower().replace(' ', '_')}", entry)

        # Buttons frame
        btn_frame = ttk.Frame(self.frame_thong_tin)
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        btn_xac_nhan = ttk.Button(
            btn_frame, 
            text="Xác nhận sửa", 
            command=self.xac_nhan_sua,
            style="Custom.TButton"
        )
        btn_xac_nhan.grid(row=0, column=0, padx=5)

        # Chi tiết phiếu nhập
        columns = ("maPN", "maSP", "soLuong", "donGia", "thanhTien")
        self.tree_ct = ttk.Treeview(
            self.frame_thong_tin, 
            columns=columns, 
            show="headings", 
            height=5,
            style="Custom.Treeview"
        )
        
        # Configure treeview columns
        for col in columns:
            self.tree_ct.heading(col, text=col)
            self.tree_ct.column(col, width=100, anchor="center")
            
        self.tree_ct.grid(row=len(fields) + 2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Load data
        dsct = self.ctphieu_nhap_buss.tim_kiem(maPN)
        for ct in dsct:
            self.tree_ct.insert("", "end", values=(ct.maPN, ct.maSP, ct.soLuong, ct.donGia, ct.thanhTien))

        # Action buttons frame
        action_btn_frame = ttk.Frame(self.frame_thong_tin)
        action_btn_frame.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10)
        action_btn_frame.grid_columnconfigure(0, weight=1)

        buttons = [
            ("Sửa Chi Tiết Phiếu Nhập", self.sua_chi_tiet_phiieu_nhap),
            ("Thêm Chi Tiết Phiếu Nhập", self.them_chi_tiet_phiieu_nhap),
            ("Xóa Chi Tiết Phiếu Nhập", self.xoa_chi_tiet_phiieu_nhap)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(
                action_btn_frame, 
                text=text, 
                command=command,
                style="Custom.TButton"
            )
            btn.grid(row=0, column=i, padx=5)


    def sua_chi_tiet_phiieu_nhap(self):
        selected = self.tree_ct.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết phiếu nhập cần sửa!")
            return
        values = self.tree_ct.item(selected[0], 'values')
        maPN, maSP, soLuong, donGia, thanhTien = values

        win = tk.Toplevel()
        win.title("Sửa chi tiết phiếu nhập")
        
        # Configure grid weights for centering
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        
        # Main container
        main_frame = ttk.Frame(win)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Create a style for consistent widget appearance
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 10))
        style.configure("Custom.TEntry", font=("Arial", 10))
        style.configure("Custom.TButton", font=("Arial", 10))

        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Sửa Chi Tiết Phiếu Nhập", 
            font=("Arial", 14, "bold"),
            style="Custom.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Display read-only fields
        ttk.Label(main_frame, text=f"Mã phiếu nhập:", style="Custom.TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(main_frame, text=maPN, style="Custom.TLabel").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(main_frame, text=f"Mã sản phẩm:", style="Custom.TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(main_frame, text=maSP, style="Custom.TLabel").grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Editable fields
        ttk.Label(main_frame, text="Số lượng:", style="Custom.TLabel").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_soLuong = ttk.Entry(main_frame, width=30, style="Custom.TEntry")
        entry_soLuong.insert(0, soLuong)
        entry_soLuong.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(main_frame, text="Đơn giá:", style="Custom.TLabel").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        entry_donGia = ttk.Entry(main_frame, width=30, style="Custom.TEntry")
        entry_donGia.insert(0, donGia)
        entry_donGia.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)

        btn_capnhat = ttk.Button(
            btn_frame,
            text="Cập nhật",
            command=lambda: self.cap_nhat(maPN, maSP, entry_soLuong, entry_donGia, win),
            style="Custom.TButton"
        )
        btn_capnhat.grid(row=0, column=0, padx=5)


    def cap_nhat(self, maPN, maSP, entry_soLuong, entry_donGia, win):
        try:
            soLuong_moi = int(entry_soLuong.get())
            donGia_moi = float(entry_donGia.get())
            thanhTien_moi = soLuong_moi * donGia_moi

            # Cập nhật chi tiết phiếu nhập
            self.ctphieu_nhap_buss.sua(maPN, maSP, soLuong_moi, donGia_moi, thanhTien_moi)
            
            # Cập nhật tổng tiền
            self.phieu_nhap_buss.cap_nhat_tong_tien(maPN)
            
            # Cập nhật lại danh sách
            self.hien_thi_danh_sach()

            win.destroy()
            messagebox.showinfo("Thành công", "Cập nhật chi tiết phiếu nhập thành công.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho số lượng và đơn giá.")


    def them_chi_tiet_phiieu_nhap(self):
        maPN = self.entry_maPN.get().strip()
        if not maPN:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập!")
            return

        win = tk.Toplevel()
        win.title("Thêm Chi Tiết Phiếu Nhập")
        
        # Configure grid weights for centering
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        
        # Main container
        main_frame = ttk.Frame(win)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Create a style for consistent widget appearance
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 10))
        style.configure("Custom.TEntry", font=("Arial", 10))
        style.configure("Custom.TButton", font=("Arial", 10))

        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Thêm Chi Tiết Phiếu Nhập", 
            font=("Arial", 14, "bold"),
            style="Custom.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Form fields
        fields = [
            ("Mã sản phẩm:", "entry_maSP"),
            ("Số lượng:", "entry_soLuong"),
            ("Đơn giá:", "entry_donGia")
        ]

        for i, (label_text, entry_name) in enumerate(fields, start=1):
            ttk.Label(main_frame, text=label_text, style="Custom.TLabel").grid(
                row=i, column=0, padx=10, pady=5, sticky="w"
            )
            entry = ttk.Entry(main_frame, width=30, style="Custom.TEntry")
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            setattr(self, entry_name, entry)

        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)

        btn_them = ttk.Button(
            btn_frame,
            text="Thêm",
            command=lambda: self.cap_nhat_them_chi_tiet(
                maPN, 
                self.entry_maSP.get(), 
                self.entry_soLuong.get(), 
                self.entry_donGia.get(), 
                win
            ),
            style="Custom.TButton"
        )
        btn_them.grid(row=0, column=0, padx=5)


    def cap_nhat_them_chi_tiet(self, maPN, maSP, soLuong, donGia, win):
        try:
            soLuong_moi = int(soLuong)
            donGia_moi = float(donGia)
            thanhTien_moi = soLuong_moi * donGia_moi
            
            # Thêm chi tiết phiếu nhập
            self.ctphieu_nhap_buss.them(maPN, maSP, soLuong_moi, donGia_moi, thanhTien_moi)
            
            # Cập nhật tổng tiền
            self.phieu_nhap_buss.cap_nhat_tong_tien(maPN)
            
            # Cập nhật lại danh sách
            self.hien_thi_danh_sach()
            
            win.destroy()
            messagebox.showinfo("Thành công", "Thêm chi tiết phiếu nhập thành công.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho số lượng và đơn giá.")


    def xoa_chi_tiet_phiieu_nhap(self):
        selected = self.tree_ct.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết phiếu nhập cần xóa!")
            return
        values = self.tree_ct.item(selected[0], 'values')
        maPN, maSP, _, _, _ = values
        
        # Xóa chi tiết phiếu nhập
        self.ctphieu_nhap_buss.xoa(maPN, maSP)
        
        # Cập nhật tổng tiền
        self.phieu_nhap_buss.cap_nhat_tong_tien(maPN)
        
        # Cập nhật lại danh sách
        self.hien_thi_danh_sach()
        
        messagebox.showinfo("Thành công", "Xóa chi tiết phiếu nhập thành công.")


    def xac_nhan_sua(self):
        maPN = self.entry_maPN.get().strip()
        maNV = self.entry_maNV.get().strip()
        ngayTao = self.entry_ngayTao.get().strip()
        tongTien = self.entry_tongTien.get().strip()

        if not maPN or not maNV or not ngayTao or not tongTien:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            datetime.strptime(ngayTao.strip(), "%Y-%m-%d")  # Kiểm tra định dạng ngày
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày tạo phải có định dạng YYYY-MM-DD.")
            return

        try:
            tongTien = float(tongTien.replace(".", "").replace(",", "."))
        except ValueError:
            messagebox.showerror("Lỗi", "Tổng tiền phải là một số hợp lệ.")
            return

        ket_qua_sua_phieu_nhap = self.phieu_nhap_buss.sua_phieu_nhap(maPN, ngayTao, maNV, tongTien)

        if ket_qua_sua_phieu_nhap:
            for item in self.tree_ct.get_children():
                values = self.tree_ct.item(item, 'values')
                maPN_ct, maSP, soLuong, donGia, thanhTien = values
                soLuong_moi = int(soLuong)
                donGia_moi = float(donGia)
                thanhTien_moi = soLuong_moi * donGia_moi
                ket_qua_ct = self.ctphieu_nhap_buss.sua(maPN_ct, maSP, soLuong_moi, donGia_moi, thanhTien_moi)

                if not ket_qua_ct:
                    messagebox.showerror("Lỗi", f"Cập nhật chi tiết phiếu nhập cho sản phẩm {maSP} thất bại.")
                    return

            messagebox.showinfo("Thành công", "Cập nhật phiếu nhập và chi tiết phiếu nhập vào cơ sở dữ liệu thành công.")
            self.hien_thi_sua()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật phiếu nhập.")


    def hien_thi_tim(self):
        self.xoa_thong_tin_frame()
        
        # Configure grid weights for centering
        self.frame_thong_tin.grid_columnconfigure(1, weight=1)
        
        # Create a style for consistent widget appearance
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 10))
        style.configure("Custom.TEntry", font=("Arial", 10))
        style.configure("Custom.TButton", font=("Arial", 10))
        
        # Title
        title_label = ttk.Label(
            self.frame_thong_tin, 
            text="Tìm Kiếm Phiếu Nhập", 
            font=("Arial", 14, "bold"),
            style="Custom.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="ew")
        
        # Search frame
        search_frame = ttk.Frame(self.frame_thong_tin)
        search_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Nhập Mã Phiếu Nhập:", style="Custom.TLabel").grid(row=0, column=0, padx=5, sticky="w")
        self.entry_maPN = ttk.Entry(search_frame, width=30, style="Custom.TEntry")
        self.entry_maPN.grid(row=0, column=1, padx=5, sticky="ew")
        btn_tim = ttk.Button(
            search_frame, 
            text="Tìm kiếm", 
            command=self.tim_kiem,
            style="Custom.TButton"
        )
        btn_tim.grid(row=0, column=2, padx=5)

    def tim_kiem(self):
        ma_pn = self.entry_maPN.get().strip()
        if not ma_pn:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập!")
            return

        self.xoa_thong_tin_frame()

        # Lấy thông tin phiếu nhập từ danh sách
        phieu_nhap = self.phieu_nhap_buss.tim_kiem(ma_pn)

        if not phieu_nhap:
            messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập!")
            return

        ttk.Label(self.frame_thong_tin, text="Thông tin phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # Treeview hiển thị phiếu nhập
        columns = ("maPN", "ngayNhap", "nhaCungCap",  "tongTien")
        tree_phieu_nhap = ttk.Treeview(self.frame_thong_tin, columns=columns, show="headings")
        for col, text in zip(columns, ["Mã Phiếu Nhập", "Ngày Nhập","Mã Nhà Cung Cấp",  "Tổng Tiền"]):
            tree_phieu_nhap.heading(col, text=text)
            tree_phieu_nhap.column(col, width=150)

        tree_phieu_nhap.pack(fill="x", padx=10)

        # Giả sử phieu_nhap = (maPN, nhaCungCap, ngayNhap, tongTien)
        maPN, nhaCungCap, ngayNhap, tongTien = phieu_nhap

        # Định dạng tổng tiền: VD: 120.000
        tongTien_str = "{:,.0f}".format(float(tongTien)).replace(",", ".")

        # Chèn dữ liệu vào treeview
        tree_phieu_nhap.insert("", "end", values=(maPN, nhaCungCap, ngayNhap, tongTien_str))

        # Treeview hiển thị chi tiết phiếu nhập
        ttk.Label(self.frame_thong_tin, text="Chi tiết phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 10))

        columns_ct = ("maPN", "maSP", "soLuongSP", "donGia", "thanhTien")
        tree_ctpn = ttk.Treeview(self.frame_thong_tin, columns=columns_ct, show="headings")
        for col in columns_ct:
            tree_ctpn.heading(col, text=col)
            tree_ctpn.column(col, width=120)
        tree_ctpn.pack(fill="x", padx=10)

        for ct in self.ctphieu_nhap_buss.dsctpn:
            if str(ct.maPN) == ma_pn:
                donGia_str = "{:,.0f}".format(float(ct.donGia)).replace(",", ".")
                thanhTien_str = "{:,.0f}".format(float(ct.thanhTien)).replace(",", ".")
                tree_ctpn.insert("", "end", values=(ct.maPN, ct.maSP, ct.soLuong, donGia_str, thanhTien_str))


    def hien_thi_in_danh_sach(self):
        self.xoa_thong_tin_frame()

        self.frame_trai = tk.Frame(self.frame_thong_tin)
        self.frame_trai.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_phai = tk.Frame(self.frame_thong_tin, bg="#F0F0F0")
        self.frame_phai.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        tk.Label(self.frame_trai, text=f"Danh sách phiếu nhập", font=("Arial", 14, "bold"), bg="#F0F0F0").pack(pady=10)

        self.treeview = ttk.Treeview(
            self.frame_trai,
            columns=("Mã PN", "Ngày Tạo", "Mã NV", "Tổng Tiền"),
            show="headings"
        )
        self.treeview.pack(fill="both", expand=True)

        self.treeview.heading("Mã PN", text="Mã Phiếu Nhập")
        self.treeview.heading("Ngày Tạo", text="Ngày Tạo")
        self.treeview.heading("Mã NV", text="Mã Nhân Viên")
        self.treeview.heading("Tổng Tiền", text="Tổng Tiền")

        self.treeview.column("Mã PN", width=150)
        self.treeview.column("Ngày Tạo", width=150)
        self.treeview.column("Mã NV", width=150)
        self.treeview.column("Tổng Tiền", width=150)

        self.treeview.bind("<<TreeviewSelect>>", self.hien_thi_chi_tiet_phieu_nhap)

        self.hien_thi_danh_sach()

    def hien_thi_danh_sach(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for phieu in self.phieu_nhap_buss.dsphieunhap:
            self.treeview.insert("", "end", values=(phieu[0], phieu[1], phieu[2], phieu[3]))

    def hien_thi_chi_tiet_phieu_nhap(self, event):
        selected = self.treeview.focus()
        values = self.treeview.item(selected, "values")
        maPN, ngayTao, maNV, tongTien = values
        # Xóa các widget cũ trong frame chi tiết
        for widget in self.frame_phai.winfo_children():
            widget.destroy()

        tk.Label(self.frame_phai, text=f"Chi tiết phiếu nhập", font=("Arial", 14, "bold"), bg="#F0F0F0").pack(pady=10)
        tk.Label(self.frame_phai, text=f"Mã Phiếu Nhập: {maPN}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)
        tk.Label(self.frame_phai, text=f"Ngày Tạo: {ngayTao}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)
        tk.Label(self.frame_phai, text=f"Mã Nhân Viên: {maNV}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)
        tk.Label(self.frame_phai, text=f"Tổng Tiền: {tongTien}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)

        # Hiển thị danh sách chi tiết phiếu nhập
        tree_ctpn = ttk.Treeview(self.frame_phai, columns=("Mã SP", "Số Lượng", "Đơn Giá", "Thành Tiền"), show="headings", height=8)
        tree_ctpn.pack(padx=20, pady=10, fill="x")

        tree_ctpn.heading("Mã SP", text="Mã Sản Phẩm")
        tree_ctpn.heading("Số Lượng", text="Số Lượng")
        tree_ctpn.heading("Đơn Giá", text="Đơn Giá")
        tree_ctpn.heading("Thành Tiền", text="Thành Tiền")

        tree_ctpn.column("Mã SP", width=100)
        tree_ctpn.column("Số Lượng", width=100)
        tree_ctpn.column("Đơn Giá", width=100)
        tree_ctpn.column("Thành Tiền", width=100)
        for ct in self.ctphieu_nhap_buss.dsctpn:
            if str(ct.maPN) == str(maPN):
                tree_ctpn.insert("", "end", values=(ct.maSP, ct.soLuong, ct.donGia, ct.thanhTien))

    def anGiaoDien(self):
        """Ẩn giao diện quản lý hóa đơn"""
        self.frame.grid_forget()

    def hienThi(self, action=None):
        """Hiển thị giao diện tương ứng với action"""
        self.frame.grid(row=0, column=0, sticky="nsew")
        if action=="Tạo phiếu nhập":
            self.hien_thi_them()
        elif action=="Tìm kiếm phiếu nhập":
            self.hien_thi_tim()
        elif action=="Sửa phiếu nhập":
            self.hien_thi_sua()
        elif action=="Hiển thị danh sách":
            self.hien_thi_in_danh_sach()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = PhieuNhapGUI(root)
    root.mainloop()
