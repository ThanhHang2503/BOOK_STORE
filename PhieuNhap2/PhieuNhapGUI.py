import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

from PhieuNhapBUSS import PhieuNhapBUSS
from CTPhieuNhapBUSS import CTPhieuNhapBUSS
from PhieuNhapDTO import PhieuNhapDTO
from CTPhieuNhapDTO import CTPhieuNhapDTO

class PhieuNhapGUI:
    def __init__(self, root):
        self.root = root
        self.phieu_nhap_buss = PhieuNhapBUSS()
        self.ct_phieu_nhap_buss = CTPhieuNhapBUSS()
        
        # Current receipt and details
        self.current_phieu_nhap = None
        self.temp_ct_phieu_nhap_list = []
        
        # Create the notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the tabs
        self.danh_sach_tab = ttk.Frame(self.notebook)
        self.them_tab = ttk.Frame(self.notebook)
        self.tim_kiem_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.danh_sach_tab, text="Danh sách phiếu nhập")
        self.notebook.add(self.them_tab, text="Thêm phiếu nhập")
        self.notebook.add(self.tim_kiem_tab, text="Tìm kiếm")
        
        # Initialize the tabs
        self.init_danh_sach_tab()
        self.init_them_tab()
        self.init_tim_kiem_tab()
        
        # Load the initial data
        self.load_phieu_nhap_list()
    
    def init_danh_sach_tab(self):
        """Initialize the list tab"""
        # Create frames
        list_frame = ttk.LabelFrame(self.danh_sach_tab, text="Danh sách phiếu nhập")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        detail_frame = ttk.LabelFrame(self.danh_sach_tab, text="Chi tiết phiếu nhập")
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the treeview for the list of receipts
        columns = ("maPN", "maNV", "ngayTao", "tongTien")
        self.phieu_nhap_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.phieu_nhap_tree.heading("maPN", text="Mã phiếu nhập")
        self.phieu_nhap_tree.heading("maNV", text="Mã nhân viên")
        self.phieu_nhap_tree.heading("ngayTao", text="Ngày tạo")
        self.phieu_nhap_tree.heading("tongTien", text="Tổng tiền")
        
        # Define columns
        self.phieu_nhap_tree.column("maPN", width=100)
        self.phieu_nhap_tree.column("maNV", width=100)
        self.phieu_nhap_tree.column("ngayTao", width=100)
        self.phieu_nhap_tree.column("tongTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.phieu_nhap_tree.yview)
        self.phieu_nhap_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.phieu_nhap_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind the treeview selection event
        self.phieu_nhap_tree.bind("<<TreeviewSelect>>", self.on_phieu_nhap_select)
        
        # Create the treeview for the details
        columns = ("maSP", "soLuong", "donGia", "thanhTien")
        self.ct_phieu_nhap_tree = ttk.Treeview(detail_frame, columns=columns, show="headings")
        
        # Define headings
        self.ct_phieu_nhap_tree.heading("maSP", text="Mã sản phẩm")
        self.ct_phieu_nhap_tree.heading("soLuong", text="Số lượng")
        self.ct_phieu_nhap_tree.heading("donGia", text="Đơn giá")
        self.ct_phieu_nhap_tree.heading("thanhTien", text="Thành tiền")
        
        # Define columns
        self.ct_phieu_nhap_tree.column("maSP", width=100)
        self.ct_phieu_nhap_tree.column("soLuong", width=100)
        self.ct_phieu_nhap_tree.column("donGia", width=150)
        self.ct_phieu_nhap_tree.column("thanhTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=self.ct_phieu_nhap_tree.yview)
        self.ct_phieu_nhap_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.ct_phieu_nhap_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the button frame
        button_frame = ttk.Frame(self.danh_sach_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create buttons
        ttk.Button(button_frame, text="Sửa", command=self.edit_phieu_nhap).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.delete_phieu_nhap).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="In phiếu nhập", command=self.display_phieu_nhap).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm mới", command=self.load_phieu_nhap_list).pack(side=tk.RIGHT, padx=5)
    
    def init_them_tab(self):
        """Initialize the add tab"""
        # Create frames
        info_frame = ttk.LabelFrame(self.them_tab, text="Thông tin phiếu nhập")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        detail_frame = ttk.LabelFrame(self.them_tab, text="Chi tiết phiếu nhập")
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the form for receipt information
        ttk.Label(info_frame, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ma_pn_entry = ttk.Entry(info_frame, width=20)
        self.ma_pn_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(info_frame, text="Mã nhân viên:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.ma_nv_entry = ttk.Entry(info_frame, width=20)
        self.ma_nv_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(info_frame, text="Ngày tạo (dd/mm/yyyy):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ngay_tao_entry = ttk.Entry(info_frame, width=20)
        self.ngay_tao_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        # Set default date
        today = date.today().strftime("%d/%m/%Y")
        self.ngay_tao_entry.insert(0, today)
        
        # Create the treeview for the details
        columns = ("maSP", "soLuong", "donGia", "thanhTien")
        self.them_ct_tree = ttk.Treeview(detail_frame, columns=columns, show="headings")
        
        # Define headings
        self.them_ct_tree.heading("maSP", text="Mã sản phẩm")
        self.them_ct_tree.heading("soLuong", text="Số lượng")
        self.them_ct_tree.heading("donGia", text="Đơn giá")
        self.them_ct_tree.heading("thanhTien", text="Thành tiền")
        
        # Define columns
        self.them_ct_tree.column("maSP", width=100)
        self.them_ct_tree.column("soLuong", width=100)
        self.them_ct_tree.column("donGia", width=150)
        self.them_ct_tree.column("thanhTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=self.them_ct_tree.yview)
        self.them_ct_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.them_ct_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the detail form frame
        detail_form_frame = ttk.Frame(self.them_tab)
        detail_form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create the form for detail information
        ttk.Label(detail_form_frame, text="Mã sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ma_sp_entry = ttk.Entry(detail_form_frame, width=20)
        self.ma_sp_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(detail_form_frame, text="Số lượng:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.so_luong_entry = ttk.Entry(detail_form_frame, width=20)
        self.so_luong_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(detail_form_frame, text="Đơn giá:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.don_gia_entry = ttk.Entry(detail_form_frame, width=20)
        self.don_gia_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Create the detail button frame
        detail_button_frame = ttk.Frame(self.them_tab)
        detail_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create buttons for details
        ttk.Button(detail_button_frame, text="Thêm chi tiết", command=self.add_detail).pack(side=tk.LEFT, padx=5)
        ttk.Button(detail_button_frame, text="Sửa chi tiết", command=self.edit_detail).pack(side=tk.LEFT, padx=5)
        ttk.Button(detail_button_frame, text="Xóa chi tiết", command=self.delete_detail).pack(side=tk.LEFT, padx=5)
        
        # Create the main button frame
        button_frame = ttk.Frame(self.them_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create buttons
        ttk.Button(button_frame, text="Lưu phiếu nhập", command=self.save_phieu_nhap).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm mới", command=self.reset_them_tab).pack(side=tk.LEFT, padx=5)
        
        # Initialize the form
        self.reset_them_tab()
    
    def init_tim_kiem_tab(self):
        """Initialize the search tab"""
        # Create frames
        search_frame = ttk.LabelFrame(self.tim_kiem_tab, text="Tìm kiếm phiếu nhập")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        result_frame = ttk.LabelFrame(self.tim_kiem_tab, text="Kết quả tìm kiếm")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the search form
        ttk.Label(search_frame, text="Tìm theo:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.search_type = tk.StringVar()
        self.search_type.set("maPN")
        
        ttk.Radiobutton(search_frame, text="Mã phiếu nhập", variable=self.search_type, value="maPN").grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(search_frame, text="Mã nhân viên", variable=self.search_type, value="maNV").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(search_frame, text="Ngày tạo", variable=self.search_type, value="ngayTao").grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(search_frame, text="Giá trị tìm kiếm:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_value_entry = ttk.Entry(search_frame, width=30)
        self.search_value_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Date range for date search
        ttk.Label(search_frame, text="Từ ngày (dd/mm/yyyy):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.from_date_entry = ttk.Entry(search_frame, width=20)
        self.from_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.from_date_entry.insert(0, "01/01/2023")
        
        ttk.Label(search_frame, text="Đến ngày (dd/mm/yyyy):").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.to_date_entry = ttk.Entry(search_frame, width=20)
        self.to_date_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        self.to_date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        
        # Create the search button
        ttk.Button(search_frame, text="Tìm kiếm", command=self.search_phieu_nhap).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Create the treeview for the search results
        columns = ("maPN", "maNV", "ngayTao", "tongTien")
        self.search_tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        # Define headings
        self.search_tree.heading("maPN", text="Mã phiếu nhập")
        self.search_tree.heading("maNV", text="Mã nhân viên")
        self.search_tree.heading("ngayTao", text="Ngày tạo")
        self.search_tree.heading("tongTien", text="Tổng tiền")
        
        # Define columns
        self.search_tree.column("maPN", width=100)
        self.search_tree.column("maNV", width=100)
        self.search_tree.column("ngayTao", width=100)
        self.search_tree.column("tongTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.search_tree.yview)
        self.search_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind the treeview selection event
        self.search_tree.bind("<Double-1>", self.on_search_result_double_click)
        self.search_tree.bind("<<TreeviewSelect>>", self.on_search_result_select)
        
        # Create a detail frame for search results
        self.search_detail_frame = ttk.LabelFrame(self.tim_kiem_tab, text="Chi tiết phiếu nhập")
        self.search_detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create the treeview for the details
        columns = ("maSP", "soLuong", "donGia", "thanhTien")
        self.search_detail_tree = ttk.Treeview(self.search_detail_frame, columns=columns, show="headings")
        
        # Define headings
        self.search_detail_tree.heading("maSP", text="Mã sản phẩm")
        self.search_detail_tree.heading("soLuong", text="Số lượng")
        self.search_detail_tree.heading("donGia", text="Đơn giá")
        self.search_detail_tree.heading("thanhTien", text="Thành tiền")
        
        # Define columns
        self.search_detail_tree.column("maSP", width=100)
        self.search_detail_tree.column("soLuong", width=100)
        self.search_detail_tree.column("donGia", width=150)
        self.search_detail_tree.column("thanhTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.search_detail_frame, orient=tk.VERTICAL, command=self.search_detail_tree.yview)
        self.search_detail_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.search_detail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the button frame
        button_frame = ttk.Frame(self.tim_kiem_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create buttons
        ttk.Button(button_frame, text="Xem chi tiết", command=self.view_search_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="In danh sách", command=self.display_search_results).pack(side=tk.LEFT, padx=5)
    
    def load_phieu_nhap_list(self):
        """Load the list of import receipts"""
        # Clear the treeview
        for item in self.phieu_nhap_tree.get_children():
            self.phieu_nhap_tree.delete(item)
        
        # Get the list of receipts
        phieu_nhap_list = self.phieu_nhap_buss.lay_danh_sach()
        
        # Add the receipts to the treeview
        for pn in phieu_nhap_list:
            self.phieu_nhap_tree.insert("", "end", values=(
                pn.maPN,
                pn.maNV,
                pn.ngayTao.strftime("%d/%m/%Y"),
                f"{pn.tongTien:,.0f}"
            ))
    
    def on_phieu_nhap_select(self, event):
        """Handle receipt selection"""
        # Get the selected item
        selection = self.phieu_nhap_tree.selection()
        if not selection:
            return
        
        # Get the receipt ID
        item = self.phieu_nhap_tree.item(selection[0])
        maPN = item["values"][0]
        
        # Load the receipt details
        self.load_ct_phieu_nhap(maPN)
    
    def on_search_result_select(self, event):
        """Handle search result selection"""
        # Get the selected item
        selection = self.search_tree.selection()
        if not selection:
            return
        
        # Get the receipt ID
        item = self.search_tree.item(selection[0])
        maPN = item["values"][0]
        
        # Load the receipt details into the search detail tree
        self.load_search_detail(maPN)
    
    def load_search_detail(self, maPN):
        """Load the details of an import receipt into the search detail tree"""
        # Clear the treeview
        for item in self.search_detail_tree.get_children():
            self.search_detail_tree.delete(item)
        
        # Get the receipt with details
        phieu_nhap = self.phieu_nhap_buss.tim_theo_ma(maPN)
        if not phieu_nhap:
            return
        
        # Add the details to the treeview
        for ctpn in phieu_nhap.dsCTPN:
            self.search_detail_tree.insert("", "end", values=(
                ctpn.maSP,
                ctpn.soLuong,
                f"{ctpn.donGia:,.0f}",
                f"{ctpn.thanhTien:,.0f}"
            ))
    
    def load_ct_phieu_nhap(self, maPN):
        """Load the details of an import receipt"""
        # Clear the treeview
        for item in self.ct_phieu_nhap_tree.get_children():
            self.ct_phieu_nhap_tree.delete(item)
        
        # Get the receipt with details
        phieu_nhap = self.phieu_nhap_buss.tim_theo_ma(maPN)
        if not phieu_nhap:
            return
        
        # Add the details to the treeview
        for ctpn in phieu_nhap.dsCTPN:
            self.ct_phieu_nhap_tree.insert("", "end", values=(
                ctpn.maSP,
                ctpn.soLuong,
                f"{ctpn.donGia:,.0f}",
                f"{ctpn.thanhTien:,.0f}"
            ))
    
    def edit_phieu_nhap(self):
        """Edit an import receipt"""
        # Get the selected item
        selection = self.phieu_nhap_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phiếu nhập để sửa.")
            return
        
        # Get the receipt ID
        item = self.phieu_nhap_tree.item(selection[0])
        maPN = item["values"][0]
        
        # Load the receipt with details
        phieu_nhap = self.phieu_nhap_buss.tim_theo_ma(maPN)
        if not phieu_nhap:
            messagebox.showerror("Lỗi", "Không thể tải thông tin phiếu nhập.")
            return
        
        # Switch to the add tab
        self.notebook.select(self.them_tab)
        
        # Fill the form with the receipt information
        self.ma_pn_entry.delete(0, tk.END)
        self.ma_pn_entry.insert(0, phieu_nhap.maPN)
        self.ma_pn_entry.config(state="readonly")  # Disable editing of the ID
        
        self.ma_nv_entry.delete(0, tk.END)
        self.ma_nv_entry.insert(0, phieu_nhap.maNV)
        
        self.ngay_tao_entry.delete(0, tk.END)
        self.ngay_tao_entry.insert(0, phieu_nhap.ngayTao.strftime("%d/%m/%Y"))
        
        # Clear the details treeview
        for item in self.them_ct_tree.get_children():
            self.them_ct_tree.delete(item)
        
        # Add the details to the treeview and temporary list
        self.temp_ct_phieu_nhap_list = []
        for ctpn in phieu_nhap.dsCTPN:
            self.temp_ct_phieu_nhap_list.append(ctpn)
            self.them_ct_tree.insert("", "end", values=(
                ctpn.maSP,
                ctpn.soLuong,
                f"{ctpn.donGia:,.0f}",
                f"{ctpn.thanhTien:,.0f}"
            ))
        
        # Set the current receipt
        self.current_phieu_nhap = phieu_nhap
    
    def delete_phieu_nhap(self):
        """Delete an import receipt"""
        # Get the selected item
        selection = self.phieu_nhap_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phiếu nhập để xóa.")
            return
        
        # Get the receipt ID
        item = self.phieu_nhap_tree.item(selection[0])
        maPN = item["values"][0]
        
        # Confirm deletion
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa phiếu nhập {maPN}?"):
            return
        
        # Delete the receipt
        if self.phieu_nhap_buss.xoa(maPN):
            messagebox.showinfo("Thông báo", "Xóa phiếu nhập thành công.")
            self.load_phieu_nhap_list()
        else:
            messagebox.showerror("Lỗi", "Không thể xóa phiếu nhập.")
    
    def display_phieu_nhap(self):
        """Display an import receipt in a separate window"""
        # Get the selected item
        selection = self.phieu_nhap_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phiếu nhập để hiển thị.")
            return
        
        # Get the receipt ID
        item = self.phieu_nhap_tree.item(selection[0])
        maPN = item["values"][0]
        
        # Get the receipt with details
        phieu_nhap = self.phieu_nhap_buss.tim_theo_ma(maPN)
        if not phieu_nhap:
            messagebox.showerror("Lỗi", "Không thể tải thông tin phiếu nhập.")
            return
        
        # Display the receipt in a separate window
        self.display_receipt_window(phieu_nhap)
    
    def display_receipt_window(self, phieu_nhap):
        """Display a receipt in a separate window"""
        # Create a new window
        window = tk.Toplevel(self.root)
        window.title(f"Chi tiết phiếu nhập {phieu_nhap.maPN}")
        window.geometry("800x600")
        
        # Create a frame for the receipt information
        info_frame = ttk.LabelFrame(window, text="Thông tin phiếu nhập")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add the receipt information
        ttk.Label(info_frame, text=f"Mã phiếu nhập: {phieu_nhap.maPN}").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text=f"Mã nhân viên: {phieu_nhap.maNV}").grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text=f"Ngày tạo: {phieu_nhap.ngayTao.strftime('%d/%m/%Y')}").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text=f"Tổng tiền: {phieu_nhap.tongTien:,.0f} VND").grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Create a frame for the details
        detail_frame = ttk.LabelFrame(window, text="Chi tiết phiếu nhập")
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the treeview for the details
        columns = ("maSP", "soLuong", "donGia", "thanhTien")
        tree = ttk.Treeview(detail_frame, columns=columns, show="headings")
        
        # Define headings
        tree.heading("maSP", text="Mã sản phẩm")
        tree.heading("soLuong", text="Số lượng")
        tree.heading("donGia", text="Đơn giá")
        tree.heading("thanhTien", text="Thành tiền")
        
        # Define columns
        tree.column("maSP", width=100)
        tree.column("soLuong", width=100)
        tree.column("donGia", width=150)
        tree.column("thanhTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add the details to the treeview
        for ctpn in phieu_nhap.dsCTPN:
            tree.insert("", "end", values=(
                ctpn.maSP,
                ctpn.soLuong,
                f"{ctpn.donGia:,.0f}",
                f"{ctpn.thanhTien:,.0f}"
            ))
        
        # Create a button frame
        button_frame = ttk.Frame(window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a close button
        ttk.Button(button_frame, text="Đóng", command=window.destroy).pack(side=tk.RIGHT)
        
        # Focus the window
        window.focus_set()
        window.grab_set()
        window.wait_window()
    
    def display_search_results(self):
        """Display the search results in a separate window"""
        # Get the items in the search tree
        items = self.search_tree.get_children()
        if not items:
            messagebox.showwarning("Cảnh báo", "Không có kết quả tìm kiếm để hiển thị.")
            return
        
        # Create a list of receipts
        phieu_nhap_list = []
        for item in items:
            values = self.search_tree.item(item)["values"]
            maPN = values[0]
            
            # Get the receipt
            phieu_nhap = self.phieu_nhap_buss.tim_theo_ma(maPN)
            if phieu_nhap:
                phieu_nhap_list.append(phieu_nhap)
        
        # Display the list in a separate window
        self.display_list_window(phieu_nhap_list)
    
    def display_list_window(self, phieu_nhap_list):
        """Display a list of receipts in a separate window"""
        # Create a new window
        window = tk.Toplevel(self.root)
        window.title("Danh sách phiếu nhập")
        window.geometry("800x600")
        
        # Create a frame for the list
        list_frame = ttk.LabelFrame(window, text="Danh sách phiếu nhập")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the treeview for the list of receipts
        columns = ("maPN", "maNV", "ngayTao", "tongTien")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        tree.heading("maPN", text="Mã phiếu nhập")
        tree.heading("maNV", text="Mã nhân viên")
        tree.heading("ngayTao", text="Ngày tạo")
        tree.heading("tongTien", text="Tổng tiền")
        
        # Define columns
        tree.column("maPN", width=100)
        tree.column("maNV", width=100)
        tree.column("ngayTao", width=100)
        tree.column("tongTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add the receipts to the treeview
        for pn in phieu_nhap_list:
            tree.insert("", "end", values=(
                pn.maPN,
                pn.maNV,
                pn.ngayTao.strftime("%d/%m/%Y"),
                f"{pn.tongTien:,.0f}"
            ))
        
        # Create a detail frame
        detail_frame = ttk.LabelFrame(window, text="Chi tiết phiếu nhập")
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the treeview for the details
        columns = ("maSP", "soLuong", "donGia", "thanhTien")
        detail_tree = ttk.Treeview(detail_frame, columns=columns, show="headings")
        
        # Define headings
        detail_tree.heading("maSP", text="Mã sản phẩm")
        detail_tree.heading("soLuong", text="Số lượng")
        detail_tree.heading("donGia", text="Đơn giá")
        detail_tree.heading("thanhTien", text="Thành tiền")
        
        # Define columns
        detail_tree.column("maSP", width=100)
        detail_tree.column("soLuong", width=100)
        detail_tree.column("donGia", width=150)
        detail_tree.column("thanhTien", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=detail_tree.yview)
        detail_tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        detail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Function to handle receipt selection
        def on_receipt_select(event):
            # Get the selected item
            selection = tree.selection()
            if not selection:
                return
            
            # Get the receipt ID
            item = tree.item(selection[0])
            maPN = item["values"][0]
            
            # Clear the detail treeview
            for item in detail_tree.get_children():
                detail_tree.delete(item)
            
            # Get the receipt with details
            phieu_nhap = self.phieu_nhap_buss.tim_theo_ma(maPN)
            if not phieu_nhap:
                return
            
            # Add the details to the treeview
            for ctpn in phieu_nhap.dsCTPN:
                detail_tree.insert("", "end", values=(
                    ctpn.maSP,
                    ctpn.soLuong,
                    f"{ctpn.donGia:,.0f}",
                    f"{ctpn.thanhTien:,.0f}"
                ))
        
        # Bind the treeview selection event
        tree.bind("<<TreeviewSelect>>", on_receipt_select)
        
        # Create a button frame
        button_frame = ttk.Frame(window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a close button
        ttk.Button(button_frame, text="Đóng", command=window.destroy).pack(side=tk.RIGHT)
        
        # Focus the window
        window.focus_set()
        window.grab_set()
        window.wait_window()
    
    def reset_them_tab(self):
        """Reset the add tab form"""
        # Clear the form
        self.ma_pn_entry.config(state="normal")
        self.ma_pn_entry.delete(0, tk.END)
        self.ma_pn_entry.insert(0, self.phieu_nhap_buss.tao_ma_phieu_nhap_moi())
        
        self.ma_nv_entry.delete(0, tk.END)
        self.ngay_tao_entry.delete(0, tk.END)
        self.ngay_tao_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        
        self.ma_sp_entry.delete(0, tk.END)
        self.so_luong_entry.delete(0, tk.END)
        self.don_gia_entry.delete(0, tk.END)
        
        # Clear the details treeview
        for item in self.them_ct_tree.get_children():
            self.them_ct_tree.delete(item)
        
        # Reset the temporary list
        self.temp_ct_phieu_nhap_list = []
        
        # Reset the current receipt
        self.current_phieu_nhap = None
    
    def add_detail(self):
        """Add a detail to the temporary list"""
        # Get the values from the form
        maSP = self.ma_sp_entry.get().strip()
        soLuong_str = self.so_luong_entry.get().strip()
        donGia_str = self.don_gia_entry.get().strip()
        
        # Validate the input
        if not maSP:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã sản phẩm.")
            return
        
        try:
            soLuong = int(soLuong_str)
            if soLuong <= 0:
                raise ValueError("Số lượng phải lớn hơn 0.")
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập số lượng hợp lệ.")
            return
        
        try:
            donGia = float(donGia_str)
            if donGia <= 0:
                raise ValueError("Đơn giá phải lớn hơn 0.")
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đơn giá hợp lệ.")
            return
        
        # Calculate the total
        thanhTien = soLuong * donGia
        
        # Create a new detail
        maPN = self.ma_pn_entry.get().strip()
        ct_phieu_nhap = CTPhieuNhapDTO(maPN, maSP, soLuong, donGia, thanhTien)
        
        # Check if the product already exists
        for i, ctpn in enumerate(self.temp_ct_phieu_nhap_list):
            if ctpn.maSP == maSP:
                # Update the existing detail
                self.temp_ct_phieu_nhap_list[i] = ct_phieu_nhap
                
                # Update the treeview
                for item in self.them_ct_tree.get_children():
                    if self.them_ct_tree.item(item)["values"][0] == maSP:
                        self.them_ct_tree.item(item, values=(
                            maSP,
                            soLuong,
                            f"{donGia:,.0f}",
                            f"{thanhTien:,.0f}"
                        ))
                        
                        # Clear the form
                        self.ma_sp_entry.delete(0, tk.END)
                        self.so_luong_entry.delete(0, tk.END)
                        self.don_gia_entry.delete(0, tk.END)
                        
                        return
        
        # Add the detail to the temporary list
        self.temp_ct_phieu_nhap_list.append(ct_phieu_nhap)
        
        # Add the detail to the treeview
        self.them_ct_tree.insert("", "end", values=(
            maSP,
            soLuong,
            f"{donGia:,.0f}",
            f"{thanhTien:,.0f}"
        ))
        
        # Clear the form
        self.ma_sp_entry.delete(0, tk.END)
        self.so_luong_entry.delete(0, tk.END)
        self.don_gia_entry.delete(0, tk.END)
    
    def edit_detail(self):
        """Edit a detail in the temporary list"""
        # Get the selected item
        selection = self.them_ct_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một chi tiết để sửa.")
            return
        
        # Get the product ID
        item = self.them_ct_tree.item(selection[0])
        maSP = item["values"][0]
        
        # Find the detail in the temporary list
        for ctpn in self.temp_ct_phieu_nhap_list:
            if ctpn.maSP == maSP:
                # Fill the form with the detail information
                self.ma_sp_entry.delete(0, tk.END)
                self.ma_sp_entry.insert(0, ctpn.maSP)
                
                self.so_luong_entry.delete(0, tk.END)
                self.so_luong_entry.insert(0, ctpn.soLuong)
                
                self.don_gia_entry.delete(0, tk.END)
                self.don_gia_entry.insert(0, ctpn.donGia)
                
                # Remove the detail from the temporary list and treeview
                self.temp_ct_phieu_nhap_list.remove(ctpn)
                self.them_ct_tree.delete(selection[0])
                
                break
    
    def delete_detail(self):
        """Delete a detail from the temporary list"""
        # Get the selected item
        selection = self.them_ct_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một chi tiết để xóa.")
            return
        
        # Get the product ID
        item = self.them_ct_tree.item(selection[0])
        maSP = item["values"][0]
        
        # Find the detail in the temporary list
        for ctpn in self.temp_ct_phieu_nhap_list:
            if ctpn.maSP == maSP:
                # Remove the detail from the temporary list
                self.temp_ct_phieu_nhap_list.remove(ctpn)
                
                # Remove the detail from the treeview
                self.them_ct_tree.delete(selection[0])
                
                break
    
    def save_phieu_nhap(self):
        """Save the import receipt"""
        # Get the values from the form
        maPN = self.ma_pn_entry.get().strip()
        maNV = self.ma_nv_entry.get().strip()
        ngayTao_str = self.ngay_tao_entry.get().strip()
        
        # Validate the input
        if not maPN:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập.")
            return
        
        if not maNV:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã nhân viên.")
            return
        
        if not self.temp_ct_phieu_nhap_list:
            messagebox.showwarning("Cảnh báo", "Vui lòng thêm ít nhất một chi tiết phiếu nhập.")
            return
        
        # Parse the date
        try:
            day, month, year = map(int, ngayTao_str.split('/'))
            ngayTao = date(year, month, day)
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ngày tạo hợp lệ (dd/mm/yyyy).")
            return
        
        # Create a new receipt
        phieu_nhap = PhieuNhapDTO(maPN, maNV, ngayTao, 0, self.temp_ct_phieu_nhap_list)
        
        # Save the receipt
        if self.current_phieu_nhap:
            # Update the existing receipt
            if self.phieu_nhap_buss.sua(phieu_nhap):
                messagebox.showinfo("Thông báo", "Cập nhật phiếu nhập thành công.")
                self.reset_them_tab()
                self.load_phieu_nhap_list()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật phiếu nhập.")
        else:
            # Add a new receipt
            if self.phieu_nhap_buss.them(phieu_nhap):
                messagebox.showinfo("Thông báo", "Thêm phiếu nhập thành công.")
                self.reset_them_tab()
                self.load_phieu_nhap_list()
            else:
                messagebox.showerror("Lỗi", "Không thể thêm phiếu nhập.")
    
    def search_phieu_nhap(self):
        """Search for import receipts"""
        # Clear the treeview
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Clear the detail treeview
        for item in self.search_detail_tree.get_children():
            self.search_detail_tree.delete(item)
        
        # Get the search type and value
        search_type = self.search_type.get()
        
        if search_type == "maPN":
            # Search by receipt ID
            maPN = self.search_value_entry.get().strip()
            if not maPN:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập.")
                return
            
            phieu_nhap = self.phieu_nhap_buss.tim_theo_ma(maPN)
            if phieu_nhap:
                self.search_tree.insert("", "end", values=(
                    phieu_nhap.maPN,
                    phieu_nhap.maNV,
                    phieu_nhap.ngayTao.strftime("%d/%m/%Y"),
                    f"{phieu_nhap.tongTien:,.0f}"
                ))
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập.")
        
        elif search_type == "maNV":
            # Search by employee ID
            maNV = self.search_value_entry.get().strip()
            if not maNV:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã nhân viên.")
                return
            
            phieu_nhap_list = self.phieu_nhap_buss.tim_theo_nhan_vien(maNV)
            if phieu_nhap_list:
                for pn in phieu_nhap_list:
                    self.search_tree.insert("", "end", values=(
                        pn.maPN,
                        pn.maNV,
                        pn.ngayTao.strftime("%d/%m/%Y"),
                        f"{pn.tongTien:,.0f}"
                    ))
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập.")
        
        elif search_type == "ngayTao":
            # Search by date range
            from_date_str = self.from_date_entry.get().strip()
            to_date_str = self.to_date_entry.get().strip()
            
            # Parse the dates
            try:
                day, month, year = map(int, from_date_str.split('/'))
                from_date = date(year, month, day)
                
                day, month, year = map(int, to_date_str.split('/'))
                to_date = date(year, month, day)
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập ngày hợp lệ (dd/mm/yyyy).")
                return
            
            phieu_nhap_list = self.phieu_nhap_buss.tim_theo_ngay(from_date, to_date)
            if phieu_nhap_list:
                for pn in phieu_nhap_list:
                    self.search_tree.insert("", "end", values=(
                        pn.maPN,
                        pn.maNV,
                        pn.ngayTao.strftime("%d/%m/%Y"),
                        f"{pn.tongTien:,.0f}"
                    ))
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập.")
    
    def on_search_result_double_click(self, event):
        """Handle double click on search result"""
        self.view_search_result()
    
    def view_search_result(self):
        """View details of a search result"""
        # Get the selected item
        selection = self.search_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phiếu nhập để xem chi tiết.")
            return
        
        # Get the receipt ID
        item = self.search_tree.item(selection[0])
        maPN = item["values"][0]
        
        # Switch to the list tab
        self.notebook.select(self.danh_sach_tab)
        
        # Find and select the receipt in the list
        for item in self.phieu_nhap_tree.get_children():
            if self.phieu_nhap_tree.item(item)["values"][0] == maPN:
                self.phieu_nhap_tree.selection_set(item)
                self.phieu_nhap_tree.focus(item)
                self.phieu_nhap_tree.see(item)
                
                # Load the details
                self.load_ct_phieu_nhap(maPN)
                
                break
