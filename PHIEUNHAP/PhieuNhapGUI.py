import os
import tkinter as tk
from datetime import datetime
from tkinter import PhotoImage, messagebox, ttk

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ghép đường dẫn đến fonts
font_path = os.path.join(base_path, 'font', 'DejaVuSans.ttf')

# Đăng ký font
pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

from .ChiTietPN import ChiTietPN
from .DSCTPhieuNhap import DSCTPhieuNhap
from .DSPhieuNhap import DSPhieuNhap
from .PhieuNhap import PhieuNhap


class PhieuNhapGUI:
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

        self.dsPhieuNhap = DSPhieuNhap()  # KẾT NỐI DATABASE
        self.taoGiaoDien()

        # Mặc định hiển thị danh sách phiếu nhập
        self.hienThi("Hiển thị phiếu nhập")

        # cờ trạng thái thao tác
        self.thanhCong = False

        # Biến lưu trạng thái tìm kiếm - không chọn mặc định
        self.search_type = tk.StringVar(value="")

        # Biến lưu trạng thái radio button đã chọn
        self.selected_radio = None

    def xuatPDF(self):
        try:
            # Get selected invoice
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn phiếu nhập cần xuất PDF")
                return

            maPN = self.tree.item(selected_item[0])['values'][0]

            # Get invoice details
            hoa_don = self.dsPhieuNhap.timKiem(maPN=maPN)
            if not hoa_don:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin phiếu nhập")
                return

            # Get invoice items
            ds_ct = DSCTPhieuNhap()
            chi_tiet = ds_ct.timKiem(maPN=maPN)

            # Create PDF
            filename = f"phieunhap_{maPN}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []

            # Add title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName='DejaVuSans',
                fontSize=16,
                spaceAfter=30
            )
            elements.append(Paragraph(f"PHIẾU NHẬP #{maPN}", title_style))

            # Add invoice info
            info_data = [
                ["Mã nhân viên:", hoa_don.maNV],
                ["Ngày tạo:", hoa_don.ngayTaoPN],
                ["Tổng tiền:", f"{hoa_don.tongTien:,.0f} VNĐ"]
            ]

            info_table = Table(info_data, colWidths=[2 * inch, 3 * inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 20))

            # Add invoice items
            elements.append(Paragraph("CHI TIẾT PHIẾU NHẬP", title_style))
            elements.append(Spacer(1, 10))

            items_data = [["Mã SP", "Số lượng", "Đơn giá", "Thành tiền"]]
            for item in chi_tiet:
                items_data.append([
                    item.maSP,
                    str(item.soLuongSP),
                    f"{item.donGia:,.0f} VNĐ",
                    f"{item.thanhTien:,.0f} VNĐ"
                ])

            items_table = Table(items_data, colWidths=[1.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(items_table)

            # Build PDF
            doc.build(elements)
            messagebox.showinfo("Thành công", f"Đã xuất phiếu nhập ra file {filename}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất PDF: {str(e)}")

    def xuatPDFChiTiet(self, maPN):
        """Xuất PDF cho chi tiết phiếu nhập"""
        try:
            # Lấy thông tin phiếu nhập
            hoa_don = self.dsPhieuNhap.timKiem(maPN=maPN)
            if not hoa_don:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin phiếu nhập")
                return

            # Lấy chi tiết phiếu nhập
            ds_ct = DSCTPhieuNhap()
            chi_tiet = ds_ct.timKiem(maPN=maPN)

            # Tạo file PDF
            filename = f"phieunhap_{maPN}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []

            # Tiêu đề
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName='DejaVuSans',
                fontSize=16,
                spaceAfter=30
            )
            elements.append(Paragraph(f"PHIẾU NHẬP #{maPN}", title_style))

            # Thông tin phiếu nhập
            info_data = [
                ["Mã nhân viên:", hoa_don.maNV],
                ["Ngày tạo:", str(hoa_don.ngayTaoPN)],
                ["Tổng tiền:", f"{hoa_don.tongTien:,.0f} VNĐ" if hoa_don.tongTien else "0 VNĐ"]
            ]
            info_table = Table(info_data, colWidths=[2 * inch, 3 * inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(info_table)

            # Thêm chi tiết phiếu nhập
            elements.append(Paragraph("CHI TIẾT PHIẾU NHẬP", title_style))
            elements.append(Spacer(1, 10))

            items_data = [["Mã SP", "Số lượng", "Đơn giá", "Thành tiền"]]
            for item in chi_tiet:
                items_data.append([
                    item.maSP,
                    str(item.soLuongSP),
                    f"{item.donGia:,.0f} VNĐ",
                    f"{item.thanhTien:,.0f} VNĐ"
                ])

            items_table = Table(items_data, colWidths=[1.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(items_table)

            # Xuất file PDF
            doc.build(elements)
            messagebox.showinfo("Thành công", f"Đã xuất phiếu nhập ra file {filename}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất PDF: {str(e)}")

    def hienThiDS(self):
        """Hiển thị danh sách phiếu nhập trong TreeView"""
        try:
            dsPhieuNhap = self.dsPhieuNhap.danhSachPN()  # Lấy danh sách phiếu nhập

            # Xóa dữ liệu cũ trong TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Thêm dữ liệu mới vào TreeView
            for pn in dsPhieuNhap:
                self.dsPhieuNhap.capNhatTongTien(pn.maPN)
                tong_tien = float(pn.tongTien) if pn.tongTien else 0
                self.tree.insert("", "end", values=(
                    pn.maPN,
                    pn.maNV,
                    f"{tong_tien:,.0f}",
                    pn.ngayTaoPN,
                    "👁"
                ))
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi hiển thị danh sách: {str(e)}", fg="red")

    def hienThi(self, action):
        # Ẩn mọi widget trong frame chính
        for widget in self.frame.winfo_children():
            widget.grid_forget()

        self.frame.grid(row=0, column=0, sticky="nsew")

        if action=="Hiển thị phiếu nhập":
            self.frame_danh_sach.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.hienThiDS()
            self.frame_nhap.grid_forget()
            self.frame_button.grid_forget()

        elif action=="Tìm kiếm phiếu nhập":
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
            # Ẩn khung tìm kiếm nếu đang tồn tại
            if hasattr(self, "search_frame"):
                self.search_frame.grid_forget()

            # Tạo lại form đầy đủ
            self.taoGiaoDien()
            self.lamMoiForm()

            self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")

            if action=="Tạo phiếu nhập":
                self.label_thong_bao.config(text="Nhập thông tin phiếu nhập mới", fg="blue")
                self.entry_maPN.config(state="normal")
                self.btn_luu.config(state="normal")
                self.btn_export_pdf.pack_forget()

            elif action=="Sửa phiếu nhập":
                self.label_thong_bao.config(text="Chọn phiếu nhập từ danh sách để sửa", fg="blue")
                self.entry_maPN.config(state="readonly")

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
                self.btn_export_pdf.pack_forget()

                # Frame chứa nút xác nhận/hủy sửa
                self.frame_suaPN = tk.Frame(self.frame)
                self.btn_huy_sua = tk.Button(self.frame_suaPN, text="Hủy",
                    command=self.lamMoiForm, bg="red", fg="white",
                    font=("Arial", 10, "bold"))
                self.btn_huy_sua.pack(side=tk.LEFT, padx=5, pady=5)

                self.btn_xac_nhan = tk.Button(self.frame_suaPN, text="Xác nhận sửa",
                    command=self.suaPhieuNhap, bg="green", fg="white",
                    font=("Arial", 10, "bold"))
                self.btn_xac_nhan.pack(side=tk.LEFT, padx=5, pady=5)

                # Đặt lại vị trí các frame
                self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                self.frame_suaPN.grid(row=1, column=0, padx=10, pady=5, sticky="w")
                self.frame_danh_sach.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

                # Separator
                self.separator = tk.Frame(self.frame, height=2, bg="gray")
                self.separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

                # Cấu hình lại layout
                self.frame.grid_rowconfigure(0, weight=0)
                self.frame.grid_rowconfigure(1, weight=0)
                self.frame.grid_rowconfigure(2, weight=1)
                self.frame.grid_columnconfigure(0, weight=1)

                # Vô hiệu hóa nút lưu (vì đã có xác nhận sửa riêng)
                self.btn_luu.config(state="disabled")

                self.hienThiDS()  # Hiển thị lại danh sách phiếu nhập

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
            text="Tìm kiếm phiếu nhập",
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
        self.radio_id_pn_var = tk.IntVar(value=0)
        self.radio_id_nv_var = tk.IntVar(value=0)

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
            text="Tìm theo mã phiếu nhập",
            variable=self.search_type,
            value="id_pn",
            style="Custom.TRadiobutton",
            command=lambda: self.toggleSearchOption("id_pn")
        )
        self.radio_id.grid(row=0, column=0)

        # Frame cho radio Name
        name_radio_frame = tk.Frame(radio_frame, bg="white")
        name_radio_frame.grid(row=0, column=1, padx=20)

        self.radio_name = ttk.Radiobutton(
            name_radio_frame,
            text="Tìm theo mã nhân viên",
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

        self.btn_export_pdf.pack_forget()

        # Ẩn danh sách phiếu nhập
        if hasattr(self, "frame_danh_sach"):
            self.frame_danh_sach.grid_forget()

    def toggleSearchOption(self, option):
        """Xử lý khi chọn hoặc bỏ chọn radio button"""
        if option=="id_pn":
            # Nếu đã chọn radio ID trước đó, bỏ chọn nó
            if self.selected_radio=="id_pn":
                self.radio_id_pn_var.set(0)
                self.selected_radio = None
                self.search_type.set("")
                self.input_frame.grid_forget()
                return

            # Nếu chưa chọn hoặc đã chọn radio khác, chọn radio ID
            self.radio_id_pn_var.set(1)
            self.radio_id_nv_var.set(0)
            self.selected_radio = "id_pn"
            self.search_type.set("id_pn")

        elif option=="id_nv":
            # Nếu đã chọn radio Name trước đó, bỏ chọn nó
            if self.selected_radio=="id_nv":
                self.radio_id_nv_var.set(0)
                self.selected_radio = None
                self.search_type.set("")
                self.input_frame.grid_forget()
                return

            # Nếu chưa chọn hoặc đã chọn radio khác, chọn radio Name
            self.radio_id_nv_var.set(1)
            self.radio_id_pn_var.set(0)
            self.selected_radio = "id_nv"
            self.search_type.set("id_nv")

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
            if self.search_type.get()=="id_pn":
                # Tìm kiếm chính xác theo mã
                pn = self.dsPhieuNhap.timKiem(search_text)
                dsPhieuNhap = [pn] if pn else []
            else:
                # Tìm kiếm theo mã nhân viên
                dsPhieuNhap = self.dsPhieuNhap.timKiem(maNV=search_text)
                if dsPhieuNhap is None:
                    dsPhieuNhap = []

            # Kiểm tra kết quả
            if not dsPhieuNhap:
                self.result_label.config(text="Không tìm thấy phiếu nhập", fg="red")
                return

            # Hiển thị danh sách phiếu nhập tìm được
            self.hienThiDSKetQua(dsPhieuNhap)
            self.result_label.config(text=f"Đã tìm thấy {len(dsPhieuNhap)} phiếu nhập", fg="green")

        except Exception as e:
            self.result_label.config(text="Không tìm thấy phiếu nhập", fg="red")

    def hienThiDSKetQua(self, dsPhieuNhap):
        """Hiển thị danh sách kết quả tìm kiếm"""
        # Tạo frame kết quả
        self.result_frame = tk.Frame(self.frame_nhap, bg="white")
        self.result_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Tạo Treeview để hiển thị kết quả
        columns = ("maPN", "maNV", "tongTien", "ngayTaoPN")
        tree = ttk.Treeview(self.result_frame, columns=columns, show="headings")

        # Đặt tiêu đề cột
        tree.heading("maPN", text="Mã phiếu nhập")
        tree.heading("maNV", text="Mã nhân viên")
        tree.heading("tongTien", text="Tổng tiền")
        tree.heading("ngayTaoPN", text="Ngày tạo")

        # Thêm dữ liệu vào Treeview
        for pn in dsPhieuNhap:
            tree.insert("", "end", values=(
                pn.maPN,
                pn.maNV,
                pn.tongTien,
                pn.ngayTaoPN
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
        if current_entry.get().strip()=="":  # Nếu ô đang trống
            return "break"  # Không làm gì cả

        next_widget = current_entry.tk_focusNext()  # Tìm ô tiếp theo
        if isinstance(next_widget, tk.Entry):  # Nếu ô tiếp theo là Entry thì chuyển
            next_widget.focus()
        return "break"  # Ngăn hành động mặc định

    def hienThiFrameSuaPN(self):
        print("Hiển thị frame_suaPN...")
        self.frame_suaPN.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")  # di chuyển xuống row 2, thêm columnspan

    def anGiaoDien(self):
        """Ẩn giao diện quản lý phiếu nhập"""
        self.frame.grid_forget()

    def taoGiaoDien(self):
        """Tạo giao diện chung cho quản lý phiếu nhập"""
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        # Frame nhập thông tin
        self.frame_nhap = ttk.LabelFrame(self.frame)

        self.label_thong_bao = tk.Label(self.frame_nhap, text="", fg="red")
        self.label_thong_bao.grid(row=0, column=0, columnspan=4, pady=5)

        ttk.Label(self.frame_nhap, text="Mã phiếu nhập:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_maPN = ttk.Entry(self.frame_nhap)
        self.entry_maPN.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Mã nhân viên:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_maNV = ttk.Entry(self.frame_nhap)
        self.entry_maNV.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Ngày tạo:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_ngayTao = ttk.Entry(self.frame_nhap, state="readonly")
        self.entry_ngayTao.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        self.entry_ngayTao.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Frame chứa các nút chức năng
        self.frame_button = tk.Frame(self.frame)

        self.btn_lam_moi = tk.Button(self.frame_button, text="Quay lại", command=self.lamMoiForm, bg="#9E9E9E",
            fg="white")
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)
        self.btn_luu = tk.Button(self.frame_button, text="OK", command=self.luuPhieuNhap, bg="#4CAF50", fg="white")
        self.btn_luu.pack(side=tk.LEFT, padx=5)

        # Add export PDF button
        self.btn_export_pdf = ttk.Button(self.frame_button, text="Xuất PDF", command=self.xuatPDF)
        self.btn_export_pdf.pack(side=tk.LEFT, padx=5)

        # Tạo frame chứa các nút sửa nếu chưa có
        self.frame_suaPN = tk.Frame(self.parent)

        # Frame hiển thị danh sách
        self.frame_danh_sach = ttk.LabelFrame(self.frame, text="Danh sách phiếu nhập")

        # Tạo Treeview để hiển thị danh sách
        self.tree = ttk.Treeview(
            self.frame_danh_sach,
            columns=("maPN", "maNV", "tongTien", "ngayTaoPN", "chiTiet"),
            displaycolumns=("maPN", "maNV", "tongTien", "ngayTaoPN", "chiTiet"),
            show="headings",
            height=15
        )
        self.tree.heading("maPN", text="Mã phiếu nhập")
        self.tree.heading("maNV", text="Mã nhân viên")
        self.tree.heading("tongTien", text="Tổng tiền")
        self.tree.heading("ngayTaoPN", text="Ngày tạo")
        self.tree.heading("chiTiet", text="Chi tiết")

        # Thiết lập độ rộng cột
        self.tree.column("maPN", width=100, anchor="center")
        self.tree.column("maNV", width=100, anchor="center")
        self.tree.column("tongTien", width=150, anchor="center")
        self.tree.column("ngayTaoPN", width=150, anchor="center")
        self.tree.column("chiTiet", width=100, anchor="center")

        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(self.frame_danh_sach, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_danh_sach, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sắp xếp các thành phần
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Bắt sự kiện khi chọn một phiếu nhập trong danh sách
        self.tree.bind("<<TreeviewSelect>>", self.chonPN)
        self.tree.bind("<Button-1>", self.xuLyClickXemPN)

        # Frame hiển thị trạng thái (sẽ được tạo khi cần)
        self.frame_trang_thai = None

        # Gán sự kiện khi nhấn Enter để di chuyển đến ô tiếp theo
        entries = [self.entry_maPN, self.entry_maNV, self.entry_ngayTao]
        for entry in entries:
            entry.bind("<Return>", self.diChuyen)

    def xuLyClickXemPN(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region=="cell":
            col = self.tree.identify_column(event.x)
            row = self.tree.identify_row(event.y)
            print(f"Click vào cột: {col}, dòng: {row}")
            if col=="#5":
                if row:
                    item = self.tree.item(row)
                    values = item["values"]
                    print(f"Giá trị dòng: {values}")
                    maPN = values[0]
                    print(f"Mã phiếu nhập được chọn: {maPN}")
                    self.xemChiTietPN(maPN)


    def chonPN(self, event):
        """Xử lý sự kiện khi chọn một phiếu nhập trong danh sách"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")

            # Hiển thị thông tin phiếu nhập được chọn lên form
            if self.entry_maPN and self.entry_maPN.winfo_exists():
                self.entry_maPN.config(state="normal")

            self.entry_maPN.delete(0, tk.END)
            self.entry_maPN.insert(0, values[0])
            self.entry_maPN.config(state="readonly")  # khoa lai

            self.entry_maNV.delete(0, tk.END)
            self.entry_maNV.insert(0, values[1])

            self.entry_ngayTao.config(state="normal")
            self.entry_ngayTao.delete(0, tk.END)
            self.entry_ngayTao.insert(0, values[3])  # Sửa lại index để lấy ngày tạo
            self.entry_ngayTao.config(state="readonly")

    def luuPhieuNhap(self):
        """Lưu thông tin phiếu nhập mới"""
        try:
            maPN = self.entry_maPN.get().strip()
            maNV = self.entry_maNV.get().strip()
            ngayTao = self.entry_ngayTao.get().strip()
            tongTien = 0  # Khởi tạo tổng tiền là 0

            if not all([maPN, maNV, ngayTao]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            # Kiểm tra xem mã nhân viên có tồn tại không
            cursor = self.dsPhieuNhap.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM NHANVIEN WHERE maNV = ?", (maNV,))
            if cursor.fetchone()[0]==0:
                self.label_thong_bao.config(text=f"Lỗi! Mã nhân viên {maNV} không tồn tại.", fg="red")
                return

            # Tạo phiếu nhập mới
            pn = PhieuNhap(
                maPN=maPN,
                maNV=maNV,
                tongTien=tongTien,
                ngayTaoPN=ngayTao
            )

            if self.dsPhieuNhap.themPN(pn):
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Thêm phiếu nhập thành công!", fg="green")
            else:
                self.label_thong_bao.config(text=f'Lỗi! Mã phiếu nhập {maPN} đã tồn tại.', fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi: {str(e)}", fg="red")

    def suaPhieuNhap(self):
        """Sửa thông tin phiếu nhập"""
        try:
            maPN = self.entry_maPN.get().strip()
            if not maPN:
                self.label_thong_bao.config(text="Vui lòng chọn phiếu nhập cần sửa!", fg="red")
                return

            maNV = self.entry_maNV.get().strip()
            ngayTao = self.entry_ngayTao.get().strip()

            if not all([maNV, ngayTao]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            # Xác nhận trước khi sửa
            confirm = messagebox.askyesno("Xác nhận sửa", f"Bạn có chắc muốn sửa thông tin phiếu nhập có mã {maPN}?")
            if not confirm:
                return

            # Cập nhật phiếu nhập
            if self.dsPhieuNhap.sua(maPN, maNV=maNV, ngayTaoPN=ngayTao):
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Sửa thông tin phiếu nhập thành công!", fg="green")
            else:
                self.label_thong_bao.config(text=f"Không tìm thấy phiếu nhập có mã {maPN}!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi sửa phiếu nhập: {str(e)}", fg="red")

    def xoaPhieuNhap(self):
        """Xóa phiếu nhập"""
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                self.label_thong_bao.config(text="Vui lòng chọn phiếu nhập cần xóa!", fg="red")
                return

            item = selected_items[0]
            maPN = self.tree.item(item, "values")[0]

            # Hiển thị hộp thoại xác nhận
            confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa phiếu nhập có mã {maPN}?")
            if confirm:
                if self.dsPhieuNhap.xoa(maPN):
                    self.hienThiDS()
                    self.lamMoiForm()
                    self.label_thong_bao.config(text="Xóa phiếu nhập thành công!", fg="green")
                else:
                    self.label_thong_bao.config(text=f"Không tìm thấy phiếu nhập có mã {maPN}!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi xóa phiếu nhập: {str(e)}", fg="red")

    def lamMoiForm(self):
        """Làm mới form nhập liệu"""
        # Check if the widgets exist before trying to clear them
        if hasattr(self, "entry_maPN") and self.entry_maPN.winfo_exists():
            self.entry_maPN.config(state="normal")
            self.entry_maPN.delete(0, tk.END)
        if hasattr(self, "entry_maNV") and self.entry_maNV.winfo_exists():
            self.entry_maNV.delete(0, tk.END)
        if hasattr(self, "entry_ngayTao") and self.entry_ngayTao.winfo_exists():
            self.entry_ngayTao.config(state="normal")
            self.entry_ngayTao.delete(0, tk.END)
            self.entry_ngayTao.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.entry_ngayTao.config(state="readonly")
        if hasattr(self, "label_thong_bao") and self.label_thong_bao.winfo_exists():
            self.label_thong_bao.config(text="")

    def xemChiTietPN(self, maPN):
        """Xử lý sự kiện khi double click vào cột chi tiết"""
        # Kiểm tra nếu cửa sổ chi tiết đã tồn tại thì đóng nó
        if hasattr(self, 'chi_tiet_window') and self.chi_tiet_window.winfo_exists():
            self.chi_tiet_window.destroy()

        # Tạo cửa sổ mới để hiển thị chi tiết phiếu nhập
        self.chi_tiet_window = tk.Toplevel(self.parent)
        self.chi_tiet_window.title(f"Chi tiết phiếu nhập {maPN}")
        self.chi_tiet_window.geometry("800x600")

        # Center the window
        window_width = 800
        window_height = 600
        screen_width = self.chi_tiet_window.winfo_screenwidth()
        screen_height = self.chi_tiet_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.chi_tiet_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Tạo frame chính và căn giữa
        main_frame = ttk.Frame(self.chi_tiet_window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Tạo frame chứa chi tiết phiếu nhập
        frame_chi_tiet = ttk.LabelFrame(main_frame, text="Danh sách chi tiết phiếu nhập")
        frame_chi_tiet.pack(fill="both", expand=True, padx=10, pady=10)

        # Tạo Treeview hiển thị chi tiết
        columns = ("maSP", "soLuongSP", "donGia", "thanhTien")
        tree_chi_tiet = ttk.Treeview(frame_chi_tiet, columns=columns, show="headings")
        tree_chi_tiet.heading("maSP", text="Mã sản phẩm")
        tree_chi_tiet.heading("soLuongSP", text="Số lượng")
        tree_chi_tiet.heading("donGia", text="Đơn giá")
        tree_chi_tiet.heading("thanhTien", text="Thành tiền")

        # Thiết lập độ rộng cột
        tree_chi_tiet.column("maSP", width=150, anchor="center")
        tree_chi_tiet.column("soLuongSP", width=100, anchor="center")
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
        btn_them = ttk.Button(frame_button, text="Thêm", command=lambda: self.themChiTiet(maPN, tree_chi_tiet))
        btn_them.pack(side="left", padx=5)

        btn_sua = ttk.Button(frame_button, text="Sửa", command=lambda: self.suaChiTiet(maPN, tree_chi_tiet))
        btn_sua.pack(side="left", padx=5)

        btn_xoa = ttk.Button(frame_button, text="Xóa", command=lambda: self.xoaChiTiet(maPN, tree_chi_tiet))
        btn_xoa.pack(side="left", padx=5)

        # Add PDF export button
        btn_export_pdf = ttk.Button(frame_button, text="Xuất PDF", command=lambda: self.xuatPDFChiTiet(maPN))
        btn_export_pdf.pack(side="left", padx=5)

        # Tải dữ liệu chi tiết phiếu nhập
        self.taiChiTietPN(maPN, tree_chi_tiet)

        # Đặt focus vào cửa sổ mới
        self.chi_tiet_window.focus_set()

    def taiChiTietPN(self, maPN, tree):
        """Tải dữ liệu chi tiết phiếu nhập vào Treeview"""
        # Xóa dữ liệu cũ
        for item in tree.get_children():
            tree.delete(item)

        # Tải dữ liệu mới
        dsCTPN = DSCTPhieuNhap()
        chi_tiet = dsCTPN.timKiem(maPN=maPN)

        # Tính tổng tiền
        tong_tien = 0
        for ct in chi_tiet:
            # Thêm vào Treeview
            tree.insert("", "end", values=(
                ct.maSP,
                ct.soLuongSP,
                f"{ct.donGia:,.0f}",
                f"{ct.thanhTien:,.0f}"
            ))
            tong_tien += ct.thanhTien

        # Cập nhật tổng tiền trong phiếu nhập
        dsPN = DSPhieuNhap()
        dsPN.capNhatTongTien(maPN)

        # Cập nhật lại danh sách phiếu nhập để hiển thị tổng tiền mới
        self.hienThiDS()

    def themChiTiet(self, maPN, tree):
        """Thêm chi tiết phiếu nhập mới"""
        # Tạo cửa sổ nhập liệu
        them_window = tk.Toplevel(self.parent)
        them_window.title("Thêm chi tiết phiếu nhập")
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
                soLuongSP = int(entry_soLuong.get().strip())
                donGia = float(entry_donGia.get().replace(',', '').strip())

                # Tạo chi tiết phiếu nhập mới
                ct = ChiTietPN(maPN=maPN, maSP=maSP, soLuongSP=soLuongSP, donGia=donGia)

                # Lưu vào database
                dsCTPN = DSCTPhieuNhap()
                if dsCTPN.them(ct):
                    # Cập nhật lại danh sách
                    self.taiChiTietPN(maPN, tree)
                    them_window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không thể thêm chi tiết phiếu nhập!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm chi tiết phiếu nhập: {str(e)}")

        # Nút lưu
        btn_luu = ttk.Button(main_frame, text="Lưu", command=luu)
        btn_luu.pack(pady=10)

    def suaChiTiet(self, maPN, tree):
        """Sửa chi tiết phiếu nhập"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết cần sửa!")
            return

        item = selected_items[0]
        values = tree.item(item, "values")
        maSP = values[0]

        # Tạo cửa sổ sửa
        sua_window = tk.Toplevel(self.parent)
        sua_window.title("Sửa chi tiết phiếu nhập")
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
                soLuongSP = int(entry_soLuong.get().strip())
                donGia = float(entry_donGia.get().replace(',', '').strip())

                # Cập nhật chi tiết phiếu nhập
                dsCTPN = DSCTPhieuNhap()
                if dsCTPN.xoa(maPN, maSP):
                    ct = ChiTietPN(maPN=maPN, maSP=maSP, soLuongSP=soLuongSP, donGia=donGia)
                    if dsCTPN.them(ct):
                        # Cập nhật lại danh sách
                        self.taiChiTietPN(maPN, tree)
                        sua_window.destroy()
                    else:
                        messagebox.showerror("Lỗi", "Không thể cập nhật chi tiết phiếu nhập!")
                else:
                    messagebox.showerror("Lỗi", "Không thể cập nhật chi tiết phiếu nhập!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật chi tiết phiếu nhập: {str(e)}")

        # Nút lưu
        btn_luu = ttk.Button(main_frame, text="Lưu", command=luu)
        btn_luu.pack(pady=10)

    def xoaChiTiet(self, maPN, tree):
        """Xóa chi tiết phiếu nhập"""
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết cần xóa!")
            return

        item = selected_items[0]
        values = tree.item(item, "values")
        maSP = values[0]

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa chi tiết này?"):
            try:
                dsCTPN = DSCTPhieuNhap()
                if dsCTPN.xoa(maPN, maSP):
                    # Cập nhật lại danh sách
                    self.taiChiTietPN(maPN, tree)
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa chi tiết phiếu nhập!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa chi tiết phiếu nhập: {str(e)}")


if __name__=="__main__":
    root = tk.Tk()
    root.title("Quản lý phiếu nhập")
    root.geometry("800x600")
    app = PhieuNhapGUI(root)
    root.mainloop()