import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from .DSNhanVien import DSNhanVien
from .NhanVien import NhanVien


class NhanVienGUI:

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

        self.dsNhanVien = DSNhanVien()  # KẾT NỐI DATABASE
        self.taoGiaoDien()

        # Mặc định hiển thị danh sách nhân viên
        self.hienThiDS()

        # cờ trạng thái thao tác
        self.thanhCong = False

        # Biến lưu trạng thái tìm kiếm - không chọn mặc định
        self.search_type = tk.StringVar(value="")

        # Biến lưu trạng thái radio button đã chọn
        self.selected_radio = None

    def hienThiDS(self):
        """Hiển thị danh sách nhân viên trong TreeView"""
        try:
            dsNhanVien = self.dsNhanVien.danhSachNV()  # Lấy danh sách nhân viên

            # Xóa dữ liệu cũ trong TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Thêm dữ liệu mới vào TreeView
            for nv in dsNhanVien:
                trangThaiText = "Còn làm" if nv.trangThai==1 else "Nghỉ làm"
                self.tree.insert("", "end", values=(
                nv.maNV, nv.tenNV, nv.chucVu, nv.luong, nv.diaChi, nv.SĐT, trangThaiText))

            # Đảm bảo frame hiển thị đúng
            self.frame_danh_sach.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
            self.frame_danh_sach.tkraise()  # Đưa frame danh sách lên trên cùng

        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi hiển thị danh sách: {str(e)}", fg="red")


    def hienThi(self, action):
        """Ẩn tất cả widgets, sau đó hiển thị giao diện theo hành động."""

        # Ẩn mọi widget trong frame chính
        for widget in self.frame.winfo_children():
            widget.grid_forget()

        self.frame.grid(row=0, column=0, sticky="nsew")

        # Mặc định hiển thị nút làm mới và lưu
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)
        self.btn_luu.pack(side=tk.LEFT, padx=5)
        self.btn_luu.config(state="normal")

        if action=="Hiển thị danh sách":
            # Hiện danh sách nhân viên
            self.frame_danh_sach.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.hienThiDS()

            btn_xuat_excel = tk.Button(self.frame_danh_sach, text="Xuất Excel", command=self.xuatExcel,
                bg="#2196F3", fg="white")
            btn_xuat_excel.pack(pady=5)

        elif action=="Tìm kiếm nhân viên":
            # Ẩn form nhập nếu có
            for widget in self.frame_nhap.winfo_children():
                widget.grid_forget()

            # Hiện giao diện tìm kiếm
            self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")
            self.taoGiaoDienTimKiem()

            # Ẩn các nút không cần thiết
            self.btn_luu.pack_forget()
            self.btn_lam_moi.pack_forget()

        else:
            # Tạo hoặc sửa nhân viên

            # Ẩn form tìm kiếm nếu đang tồn tại
            if hasattr(self, "search_frame"):
                self.search_frame.grid_forget()

            # Tạo lại form
            self.taoGiaoDien()
            self.lamMoiForm()

            self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")

            if action=="Thêm nhân viên":
                self.label_thong_bao.config(text="Nhập thông tin nhân viên mới", fg="blue")
                self.entry_maNV.config(state="normal")
                self.btn_luu.config(state="normal")

            elif action=="Sửa thông tin nhân viên":
                self.label_thong_bao.config(text="Chọn nhân viên từ danh sách để sửa", fg="blue")
                self.entry_maNV.config(state="readonly")

                # Hiện form sửa nếu có
                if hasattr(self, "frame_form"):
                    self.frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                    for widget in self.frame_form.winfo_children():
                        if isinstance(widget, (tk.Label, tk.Entry)):
                            widget.grid_configure(sticky="ew")

                # Ẩn tất cả widget sau row 1
                for widget in self.frame.winfo_children():
                    grid_info = widget.grid_info()
                    if int(grid_info.get('row', -1)) > 1:
                        widget.grid_forget()

                self.btn_lam_moi.pack_forget()
                self.btn_luu.pack_forget()

                # Frame chứa nút xác nhận/hủy sửa
                self.frame_suaNV = tk.Frame(self.frame)
                self.btn_huy_sua = tk.Button(self.frame_suaNV, text="Hủy",
                    command=self.lamMoiForm, bg="red", fg="white",
                    font=("Arial", 10, "bold"))
                self.btn_huy_sua.pack(side=tk.LEFT, padx=5, pady=5)

                self.btn_xac_nhan = tk.Button(self.frame_suaNV, text="Xác nhận sửa",
                    command=self.suaNhanVien, bg="green", fg="white",
                    font=("Arial", 10, "bold"))
                self.btn_xac_nhan.pack(side=tk.LEFT, padx=5, pady=5)

                self.frame_suaNV.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

                # Separator
                self.separator = tk.Frame(self.frame, height=2, bg="gray")
                self.separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

                # Hiện danh sách nhân viên
                self.frame_danh_sach.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
                self.hienThiDS()  # Load danh sách nhân viên

                # Cấu hình lại layout
                self.frame.grid_rowconfigure(0, weight=0)
                self.frame.grid_rowconfigure(2, weight=0)
                self.frame.grid_rowconfigure(3, weight=0)
                self.frame.grid_rowconfigure(4, weight=1)
                self.frame.grid_columnconfigure(0, weight=1)

                self.btn_luu.config(state="disabled")

            else:
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
            text="Tìm kiếm nhân viên",
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
        self.radio_id_var = tk.IntVar(value=0)
        self.radio_name_var = tk.IntVar(value=0)

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
            text="Tìm theo mã nhân viên",
            variable=self.search_type,
            value="id",
            style="Custom.TRadiobutton",
            command=lambda: self.toggleSearchOption("id")
        )
        self.radio_id.grid(row=0, column=0)

        # Frame cho radio Name
        name_radio_frame = tk.Frame(radio_frame, bg="white")
        name_radio_frame.grid(row=0, column=1, padx=20)

        self.radio_name = ttk.Radiobutton(
            name_radio_frame,
            text="Tìm theo tên",
            variable=self.search_type,
            value="name",
            style="Custom.TRadiobutton",
            command=lambda: self.toggleSearchOption("name")
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

        # Ẩn danh sách nhân viên
        if hasattr(self, "frame_danh_sach"):
            self.frame_danh_sach.grid_forget()

    def toggleSearchOption(self, option):
        """Xử lý khi chọn hoặc bỏ chọn radio button"""
        if option=="id":
            # Nếu đã chọn radio ID trước đó, bỏ chọn nó
            if self.selected_radio=="id":
                self.radio_id_var.set(0)
                self.selected_radio = None
                self.search_type.set("")
                self.input_frame.grid_forget()
                return

            # Nếu chưa chọn hoặc đã chọn radio khác, chọn radio ID
            self.radio_id_var.set(1)
            self.radio_name_var.set(0)
            self.selected_radio = "id"
            self.search_type.set("id")

        elif option=="name":
            # Nếu đã chọn radio Name trước đó, bỏ chọn nó
            if self.selected_radio=="name":
                self.radio_name_var.set(0)
                self.selected_radio = None
                self.search_type.set("")
                self.input_frame.grid_forget()
                return

            # Nếu chưa chọn hoặc đã chọn radio khác, chọn radio Name
            self.radio_name_var.set(1)
            self.radio_id_var.set(0)
            self.selected_radio = "name"
            self.search_type.set("name")

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
            self.result_frame.destroy()  # hủy frame cũ
        self.result_frame = tk.Frame(self.frame_nhap, bg="white")
        self.result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Thực hiện tìm kiếm
        try:
            if self.search_type.get()=="id":
                dsNhanVien = self.dsNhanVien.timKiemNV(maNV=search_text)
            else:
                dsNhanVien = self.timKiemGanDungTheoTen(search_text)

            if not dsNhanVien:
                self.result_label.config(text="Không tìm thấy nhân viên", fg="red")
                return

            self.result_label.config(text=f"Đã tìm thấy {len(dsNhanVien)} nhân viên", fg="green")

            # Hiển thị danh sách nhân viên trong Treeview
            columns = ("ma", "ten", "diachi", "sdt", "luong", "chucvu", "trangthai")
            tree = ttk.Treeview(self.result_frame, columns=columns, show="headings", height=8)

            # Đặt tiêu đề cột
            tree.heading("ma", text="Mã nhân viên")
            tree.heading("ten", text="Họ tên")
            tree.heading("diachi", text="Địa chỉ")
            tree.heading("sdt", text="SĐT")
            tree.heading("luong", text="Lương")
            tree.heading("chucvu", text="Chức vụ")
            tree.heading("trangthai", text="Trạng thái")


            # Căn lề và độ rộng
            tree.column("ma", width=80)
            tree.column("ten", width=150)
            tree.column("diachi", width=80)
            tree.column("sdt", width=100)
            tree.column("luong", width=150)
            tree.column("chucvu", width=80)
            tree.column("trangthai", width=70)


            # Thêm dữ liệu vào bảng
            for nv in dsNhanVien:
                tree.insert("", "end", values=(
                    nv.maNV,
                    nv.tenNV,
                    nv.diaChi,
                    nv.SĐT,
                    nv.luong,
                    nv.chucVu,
                    nv.trangThai
                ))

            tree.pack(fill="both", expand=True)

        except Exception as e:
            self.result_label.config(text="Có lỗi xảy ra khi tìm kiếm", fg="red")
            print("Lỗi khi tìm kiếm:", e)

    def timKiemGanDungTheoTen(self, ten_tim_kiem):
        """Tìm kiếm gần đúng theo tên nhân viên"""
        dsNhanVien = self.dsNhanVien.danhSachNV()
        ket_qua = []

        # Chuyển tên tìm kiếm về chữ thường và loại bỏ dấu cách thừa
        ten_tim_kiem = ten_tim_kiem.lower().strip()

        # Tách từ khóa tìm kiếm thành các từ riêng biệt
        tu_tim_kiem = ten_tim_kiem.split()

        for nv in dsNhanVien:
            ten_nv = nv.tenNV.lower()

            # Kiểm tra từng từ trong từ khóa tìm kiếm
            for tu in tu_tim_kiem:
                # Nếu từ này xuất hiện trong tên nhân viên, thêm vào kết quả
                if tu in ten_nv.split():
                    ket_qua.append(nv)
                    break  # Tìm thấy một từ khớp là đủ, không cần kiểm tra các từ khác

        return ket_qua

    def hienThiThongTinNhanVien(self, nv):
        """Hiển thị thông tin chi tiết của nhân viên"""
        # Tạo lại frame kết quả - không có viền
        self.result_frame = tk.Frame(self.frame_nhap, bg="white")
        self.result_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Tiêu đề
        tk.Label(
            self.result_frame,
            text="Thông tin nhân viên",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333333"
        ).grid(row=0, column=0, pady=(15, 10), sticky="ew")
        self.result_frame.columnconfigure(0, weight=1)

        # Frame chứa thông tin
        info_frame = tk.Frame(self.result_frame, bg="white")
        info_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Tạo grid layout cho thông tin
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=2)

        # Hiển thị thông tin
        fields = [
            ("Mã nhân viên:", nv.maNV),
            ("Tên nhân viên:", nv.tenNV),
            ("Chức vụ:", nv.chucVu),
            ("Lương:", f"{nv.luong:,.0f} VNĐ"),
            ("Địa chỉ:", nv.diaChi),
            ("SĐT:", nv.SĐT),
            ("Trạng thái:", "Còn làm" if nv.trangThai==1 else "Nghỉ làm")
        ]

        for i, (label_text, value) in enumerate(fields):
            tk.Label(
                info_frame,
                text=label_text,
                font=("Arial", 11),
                bg="white",
                fg="#555555",
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=5)

            tk.Label(
                info_frame,
                text=str(value),
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#333333",
                anchor="w"
            ).grid(row=i, column=1, sticky="w", pady=5, padx=10)

        # Nút quay lại
        tk.Button(
            self.result_frame,
            text="Tìm kiếm khác",
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 11),
            bd=0,
            padx=15,
            pady=5,
            command=lambda: self.toggleSearchOption(self.selected_radio)
        ).grid(row=2, column=0, pady=(10, 20))

    def diChuyen(self, event):
        current_entry = event.widget  # Lấy ô nhập liệu hiện tại
        if current_entry.get().strip()=="":  # Nếu ô đang trống
            return "break"  # Không làm gì cả

        next_widget = current_entry.tk_focusNext()  # Tìm ô tiếp theo
        if isinstance(next_widget, tk.Entry):  # Nếu ô tiếp theo là Entry thì chuyển
            next_widget.focus()
        return "break"  # Ngăn hành động mặc định

    def hienThiFrameSuaNV(self):
        print("Hiển thị frame_suaNV...")
        self.frame_suaNV.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")  # di chuyển xuống row 2, thêm columnspan

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

        ttk.Label(self.frame_nhap, text="Trạng thái (1: Còn làm, 0: Nghỉ làm):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_trangThai = ttk.Entry(self.frame_nhap)
        self.entry_trangThai.grid(row=5, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Frame chứa các nút chức năng
        self.frame_button = tk.Frame(self.frame)

        self.btn_lam_moi = tk.Button(self.frame_button, text="Quay lại", command=self.lamMoiForm, bg="#9E9E9E",
            fg="white")
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)
        self.btn_luu = tk.Button(self.frame_button, text="OK", command=self.luuNhanVien, bg="#4CAF50", fg="white")
        self.btn_luu.pack(side=tk.LEFT, padx=5)

        # Tạo frame chứa các nút sửa nếu chưa có
        self.frame_suaNV = tk.Frame(self.parent)

        # Frame hiển thị danh sách
        self.frame_danh_sach = ttk.LabelFrame(self.frame, text="Danh sách nhân viên")

        # Tạo Treeview để hiển thị danh sách
        self.tree = ttk.Treeview(self.frame_danh_sach, columns=(
        "maNV", "tenNV", "chucVu", "luong", "diaChi", "SĐT", "trangThai"),
            show="headings", height=15)
        self.tree.heading("maNV", text="Mã nhân viên")
        self.tree.heading("tenNV", text="Tên nhân viên")
        self.tree.heading("chucVu", text="Chức vụ")
        self.tree.heading("luong", text="Lương")
        self.tree.heading("diaChi", text="Địa chỉ")
        self.tree.heading("SĐT", text="SĐT")
        self.tree.heading("trangThai", text="Trạng thái")

        # Thiết lập độ rộng cột
        self.tree.column("maNV", width=100)
        self.tree.column("tenNV", width=200)
        self.tree.column("chucVu", width=150)
        self.tree.column("luong", width=100)
        self.tree.column("diaChi", width=200)
        self.tree.column("SĐT", width=120)
        self.tree.column("trangThai", width=120)

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
        self.frame_trang_thai = None

        # Gán sự kiện khi nhấn Enter để di chuyển đến ô tiếp theo
        entries = [self.entry_maNV, self.entry_tenNV, self.entry_chucVu, self.entry_luong, self.entry_diaChi,
                   self.entry_SĐT, self.entry_trangThai]
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

            self.entry_trangThai.delete(0, tk.END)
            self.entry_trangThai.insert(0, values[6])

    def luuNhanVien(self):
        """Lưu thông tin nhân viên mới"""
        try:
            maNV = self.entry_maNV.get()
            tenNV = self.entry_tenNV.get()
            chucVu = self.entry_chucVu.get()
            luong = self.entry_luong.get()
            diaChi = self.entry_diaChi.get()
            SĐT = self.entry_SĐT.get()
            trangThai = self.entry_trangThai.get()

            if not all([maNV, tenNV, chucVu, luong, diaChi, SĐT, trangThai]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            # Convert numeric fields
            try:
                luong = float(luong)
                trangThai = int(trangThai)
            except ValueError:
                self.label_thong_bao.config(text="Lỗi: Lương phải là số và Trạng thái phải là 0 hoặc 1!", fg="red")
                return

            # Create NhanVien object with correct parameter order
            nvien = NhanVien(maNV, tenNV, diaChi, SĐT, luong, chucVu, trangThai)

            if self.dsNhanVien.themNV(nvien):
                # Cập nhật danh sách
                self.hienThiDS()
                # Làm mới form
                self.lamMoiForm()
                # Hiển thị thông báo thành công
                self.label_thong_bao.config(text="Thêm nhân viên thành công!", fg="green")
                
                # Đảm bảo form nhập liệu luôn hiển thị trên cùng
                self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
                self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")
                self.frame_danh_sach.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
                
                # Cấu hình lại layout
                self.frame.grid_rowconfigure(0, weight=0)
                self.frame.grid_rowconfigure(1, weight=0)
                self.frame.grid_rowconfigure(2, weight=1)
                self.frame.grid_columnconfigure(0, weight=1)
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
            diaChi = self.entry_diaChi.get()
            SĐT = self.entry_SĐT.get()
            luong = self.entry_luong.get()
            chucVu = self.entry_chucVu.get()
            trangThai = self.entry_trangThai.get()

            if not all([tenNV, diaChi, SĐT, luong, chucVu, trangThai]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            # Convert numeric fields
            try:
                luong = float(luong)
                if trangThai=="Còn làm":
                    trangThai = 1
                elif trangThai=="Nghỉ làm":
                    trangThai = 0
                else:
                    trangThai = int(trangThai)
            except ValueError:
                self.label_thong_bao.config(text="Lỗi: Lương phải là số và Trạng thái phải là 0, 1, 'Còn làm' hoặc 'Nghỉ làm'!", fg="red")
                return

            # Xác nhận trước khi sửa
            confirm = messagebox.askyesno("Xác nhận sửa",
                f"Bạn có chắc chắn muốn sửa thông tin nhân viên có mã {maNV}?")
            if not confirm:
                return

            # Sử dụng phương thức suaNV với kwargs
            self.dsNhanVien.suaNV(maNV, tenNV=tenNV, diaChi=diaChi, SĐT=SĐT, luong=luong, chucVu=chucVu, trangThai=trangThai)
            self.hienThiDS()
            self.lamMoiForm()
            self.label_thong_bao.config(text="Sửa thông tin nhân viên thành công!", fg="green")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi sửa nhân viên: {str(e)}", fg="red")

    def timKiemNhanVien(self):
        """Hiển thị giao diện tìm kiếm nhân viên"""
        self.hienThi("Tìm kiếm nhân viên")

    def lamMoiForm(self):
        """Làm mới form nhập liệu"""
        # Check if the widgets exist before trying to clear them
        if hasattr(self, "entry_maNV") and self.entry_maNV.winfo_exists():
            self.entry_maNV.config(state="normal")  # Mở khóa trường mã nhân viên
            self.entry_maNV.delete(0, tk.END)
        if hasattr(self, "entry_tenNV") and self.entry_tenNV.winfo_exists():
            self.entry_tenNV.delete(0, tk.END)
        if hasattr(self, "entry_chucVu") and self.entry_chucVu.winfo_exists():
            self.entry_chucVu.delete(0, tk.END)
        if hasattr(self, "entry_luong") and self.entry_luong.winfo_exists():
            self.entry_luong.delete(0, tk.END)
        if hasattr(self, "entry_diaChi") and self.entry_diaChi.winfo_exists():
            self.entry_diaChi.delete(0, tk.END)
        if hasattr(self, "entry_SĐT") and self.entry_SĐT.winfo_exists():
            self.entry_SĐT.delete(0, tk.END)
        if hasattr(self, "entry_trangThai") and self.entry_trangThai.winfo_exists():
            self.entry_trangThai.delete(0, tk.END)
        if hasattr(self, "label_thong_bao") and self.label_thong_bao.winfo_exists():
            self.label_thong_bao.config(text="")  # Xóa thông báo
            
        # Xóa selection trong treeview nếu có
        if hasattr(self, "tree") and self.tree.winfo_exists():
            self.tree.selection_remove(self.tree.selection())

    def xuatExcel(self):
        """Xuất danh sách nhân viên ra file Excel"""
        try:
            # Lấy danh sách nhân viên
            dsNhanVien = self.dsNhanVien.danhSachNV()
            
            if not dsNhanVien:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu nhân viên để xuất!")
                return
                
            # Mở hộp thoại chọn nơi lưu file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Lưu file Excel"
            )
            
            if not file_path:  # Người dùng hủy việc lưu file
                return
                
            # Tạo workbook mới
            wb = Workbook()
            ws = wb.active
            ws.title = "Danh sách nhân viên"
            
            # Đặt tiêu đề cho các cột
            headers = ["Mã NV", "Họ tên", "Địa chỉ", "SĐT", "Lương", "Chức vụ", "Trạng thái"]
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
            
            # Thêm dữ liệu
            for row, nv in enumerate(dsNhanVien, 2):
                ws.cell(row=row, column=1, value=nv.maNV)
                ws.cell(row=row, column=2, value=nv.tenNV)
                ws.cell(row=row, column=3, value=nv.diaChi)
                ws.cell(row=row, column=4, value=nv.SĐT)
                ws.cell(row=row, column=5, value=nv.luong)
                ws.cell(row=row, column=6, value=nv.chucVu)
                ws.cell(row=row, column=7, value="Còn làm" if nv.trangThai==1 else "Nghỉ làm")
            
            # Điều chỉnh độ rộng cột
            for col in range(1, len(headers) + 1):
                ws.column_dimensions[get_column_letter(col)].width = 15
            
            # Lưu file
            wb.save(file_path)
            messagebox.showinfo("Thành công", f"Đã xuất danh sách nhân viên thành công!\nFile được lưu tại: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi xuất file Excel:\n{str(e)}")


if __name__=="__main__":
    root = tk.Tk()
    root.title("Quản lý nhân viên")
    app = NhanVienGUI(root)
    root.mainloop()