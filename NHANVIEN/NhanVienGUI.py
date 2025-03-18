import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from PhieuNhap import PhieuNhap
from ChiTietPhieuNhap import ChiTietPhieuNhap
from DSPhieuNhap import DSPhieuNhap
from DSCTPhieuNhap import DSCTPhieuNhap

class PhieuNhapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Phiếu Nhập")
        self.root.geometry("900x600")
        
        self.ds_phieu_nhap = DSPhieuNhap()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tab_danh_sach = ttk.Frame(self.notebook)
        self.tab_them = ttk.Frame(self.notebook)
        self.tab_tim_kiem = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_danh_sach, text="Danh sách phiếu nhập")
        self.notebook.add(self.tab_them, text="Thêm phiếu nhập")
        self.notebook.add(self.tab_tim_kiem, text="Tìm kiếm")
        
        # Setup each tab
        self.setup_danh_sach_tab()
        self.setup_them_tab()
        self.setup_tim_kiem_tab()
    
    def setup_danh_sach_tab(self):
        # Frame for treeview
        frame_treeview = ttk.Frame(self.tab_danh_sach)
        frame_treeview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create Treeview for phiếu nhập
        self.tree_phieu_nhap = ttk.Treeview(frame_treeview, columns=("Mã PN", "Mã NV", "Ngày tạo", "Tổng tiền"))
        self.tree_phieu_nhap.heading("#0", text="STT")
        self.tree_phieu_nhap.heading("Mã PN", text="Mã PN")
        self.tree_phieu_nhap.heading("Mã NV", text="Mã NV")
        self.tree_phieu_nhap.heading("Ngày tạo", text="Ngày tạo")
        self.tree_phieu_nhap.heading("Tổng tiền", text="Tổng tiền")
        
        self.tree_phieu_nhap.column("#0", width=50)
        self.tree_phieu_nhap.column("Mã PN", width=100)
        self.tree_phieu_nhap.column("Mã NV", width=100)
        self.tree_phieu_nhap.column("Ngày tạo", width=150)
        self.tree_phieu_nhap.column("Tổng tiền", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=self.tree_phieu_nhap.yview)
        self.tree_phieu_nhap.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_phieu_nhap.pack(fill="both", expand=True)
        
        # Create Treeview for chi tiết phiếu nhập
        label_chi_tiet = ttk.Label(self.tab_danh_sach, text="Chi tiết phiếu nhập")
        label_chi_tiet.pack(pady=(20, 5))
        
        frame_chi_tiet = ttk.Frame(self.tab_danh_sach)
        frame_chi_tiet.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree_chi_tiet = ttk.Treeview(frame_chi_tiet, columns=("Mã SP", "Số lượng", "Đơn giá", "Thành tiền"))
        self.tree_chi_tiet.heading("#0", text="STT")
        self.tree_chi_tiet.heading("Mã SP", text="Mã SP")
        self.tree_chi_tiet.heading("Số lượng", text="Số lượng")
        self.tree_chi_tiet.heading("Đơn giá", text="Đơn giá")
        self.tree_chi_tiet.heading("Thành tiền", text="Thành tiền")
        
        self.tree_chi_tiet.column("#0", width=50)
        self.tree_chi_tiet.column("Mã SP", width=100)
        self.tree_chi_tiet.column("Số lượng", width=100)
        self.tree_chi_tiet.column("Đơn giá", width=150)
        self.tree_chi_tiet.column("Thành tiền", width=150)
        
        # Add scrollbar
        scrollbar_chi_tiet = ttk.Scrollbar(frame_chi_tiet, orient="vertical", command=self.tree_chi_tiet.yview)
        self.tree_chi_tiet.configure(yscrollcommand=scrollbar_chi_tiet.set)
        scrollbar_chi_tiet.pack(side="right", fill="y")
        self.tree_chi_tiet.pack(fill="both", expand=True)
        
        # Bind select event
        self.tree_phieu_nhap.bind("<<TreeviewSelect>>", self.on_phieu_nhap_select)
        
        # Buttons frame
        frame_buttons = ttk.Frame(self.tab_danh_sach)
        frame_buttons.pack(fill='x', padx=10, pady=10)
        
        # Buttons
        btn_refresh = ttk.Button(frame_buttons, text="Làm mới", command=self.load_phieu_nhap)
        btn_refresh.pack(side="left", padx=5)
        
        btn_sua = ttk.Button(frame_buttons, text="Sửa", command=self.sua_phieu_nhap)
        btn_sua.pack(side="left", padx=5)
    
    def setup_them_tab(self):
        # Frame for phiếu nhập info
        frame_info = ttk.LabelFrame(self.tab_them, text="Thông tin phiếu nhập")
        frame_info.pack(fill='x', padx=10, pady=10)
        
        # Phiếu nhập fields
        ttk.Label(frame_info, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_ma_pn = ttk.Entry(frame_info, width=30)
        self.entry_ma_pn.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_info, text="Mã nhân viên:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_ma_nv = ttk.Entry(frame_info, width=30)
        self.entry_ma_nv.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_info, text="Ngày tạo (YYYY/MM/DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_ngay_tao = ttk.Entry(frame_info, width=30)
        self.entry_ngay_tao.grid(row=2, column=1, padx=5, pady=5)
        self.entry_ngay_tao.insert(0, datetime.today().strftime("%Y/%m/%d"))
        
        # Frame for chi tiết phiếu nhập
        frame_chi_tiet = ttk.LabelFrame(self.tab_them, text="Chi tiết phiếu nhập")
        frame_chi_tiet.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for chi tiết
        self.tree_them_chi_tiet = ttk.Treeview(frame_chi_tiet, columns=("Mã SP", "Số lượng", "Đơn giá", "Thành tiền"))
        self.tree_them_chi_tiet.heading("#0", text="STT")
        self.tree_them_chi_tiet.heading("Mã SP", text="Mã SP")
        self.tree_them_chi_tiet.heading("Số lượng", text="Số lượng")
        self.tree_them_chi_tiet.heading("Đơn giá", text="Đơn giá")
        self.tree_them_chi_tiet.heading("Thành tiền", text="Thành tiền")
        
        self.tree_them_chi_tiet.column("#0", width=50)
        self.tree_them_chi_tiet.column("Mã SP", width=100)
        self.tree_them_chi_tiet.column("Số lượng", width=100)
        self.tree_them_chi_tiet.column("Đơn giá", width=150)
        self.tree_them_chi_tiet.column("Thành tiền", width=150)
        
        scrollbar = ttk.Scrollbar(frame_chi_tiet, orient="vertical", command=self.tree_them_chi_tiet.yview)
        self.tree_them_chi_tiet.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_them_chi_tiet.pack(fill="both", expand=True)
        
        # Frame for chi tiết input
        frame_input = ttk.Frame(self.tab_them)
        frame_input.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_input, text="Mã sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_ma_sp = ttk.Entry(frame_input, width=20)
        self.entry_ma_sp.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Số lượng:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_so_luong = ttk.Entry(frame_input, width=10)
        self.entry_so_luong.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Đơn giá:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.entry_don_gia = ttk.Entry(frame_input, width=15)
        self.entry_don_gia.grid(row=0, column=5, padx=5, pady=5)
        
        # Buttons
        frame_buttons = ttk.Frame(self.tab_them)
        frame_buttons.pack(fill='x', padx=10, pady=10)
        
        btn_them_chi_tiet = ttk.Button(frame_buttons, text="Thêm chi tiết", command=self.them_chi_tiet)
        btn_them_chi_tiet.pack(side="left", padx=5)
        
        btn_xoa_chi_tiet = ttk.Button(frame_buttons, text="Xóa chi tiết", command=self.xoa_chi_tiet)
        btn_xoa_chi_tiet.pack(side="left", padx=5)
        
        btn_luu = ttk.Button(frame_buttons, text="Lưu phiếu nhập", command=self.luu_phieu_nhap)
        btn_luu.pack(side="right", padx=5)
        
        # Initialize list for chi tiết
        self.ds_chi_tiet_moi = []
    
    def setup_tim_kiem_tab(self):
        # Frame for search
        frame_search = ttk.Frame(self.tab_tim_kiem)
        frame_search.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_search, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_tim_ma_pn = ttk.Entry(frame_search, width=30)
        self.entry_tim_ma_pn.grid(row=0, column=1, padx=5, pady=5)
        
        btn_tim = ttk.Button(frame_search, text="Tìm kiếm", command=self.tim_phieu_nhap)
        btn_tim.grid(row=0, column=2, padx=5, pady=5)
        
        # Frame for result
        frame_result = ttk.LabelFrame(self.tab_tim_kiem, text="Kết quả tìm kiếm")
        frame_result.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text widget for result
        self.text_result = tk.Text(frame_result, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(frame_result, orient="vertical", command=self.text_result.yview)
        self.text_result.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.text_result.pack(fill="both", expand=True)
    
    def load_phieu_nhap(self):
        # Clear treeview
        for item in self.tree_phieu_nhap.get_children():
            self.tree_phieu_nhap.delete(item)
        
        # Load data
        for i, pn in enumerate(self.ds_phieu_nhap.ds):
            self.tree_phieu_nhap.insert("", "end", text=str(i+1), 
                                        values=(pn.maPN, pn.maNV, pn.ngayTao, f"{pn.tongTien:,.2f}"))
    
    def on_phieu_nhap_select(self, event):
        # Clear chi tiết treeview
        for item in self.tree_chi_tiet.get_children():
            self.tree_chi_tiet.delete(item)
        
        # Get selected item
        selected_item = self.tree_phieu_nhap.selection()
        if not selected_item:
            return
        
        # Get phiếu nhập
        item = self.tree_phieu_nhap.item(selected_item[0])
        ma_pn = item['values'][0]
        
        # Find phiếu nhập
        for pn in self.ds_phieu_nhap.ds:
            if pn.maPN == ma_pn:
                # Load chi tiết
                for i, ctpn in enumerate(pn.dsctpn.ds):
                    self.tree_chi_tiet.insert("", "end", text=str(i+1), 
                                             values=(ctpn.maSP, ctpn.soLuong, 
                                                    f"{ctpn.donGia:,.2f}", 
                                                    f"{ctpn.thanhTien:,.2f}"))
                break
    
    def them_chi_tiet(self):
        # Get values
        ma_sp = self.entry_ma_sp.get().strip()
        so_luong_str = self.entry_so_luong.get().strip()
        don_gia_str = self.entry_don_gia.get().strip()
        
        # Validate
        if not ma_sp:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã sản phẩm")
            return
        
        try:
            so_luong = int(so_luong_str)
            if so_luong <= 0:
                raise ValueError("Số lượng phải lớn hơn 0")
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ")
            return
        
        try:
            don_gia = float(don_gia_str)
            if don_gia <= 0:
                raise ValueError("Đơn giá phải lớn hơn 0")
        except ValueError:
            messagebox.showerror("Lỗi", "Đơn giá không hợp lệ")
            return
        
        # Create chi tiết
        thanh_tien = so_luong * don_gia
        
        # Add to treeview
        index = len(self.tree_them_chi_tiet.get_children()) + 1
        self.tree_them_chi_tiet.insert("", "end", text=str(index), 
                                      values=(ma_sp, so_luong, f"{don_gia:,.2f}", f"{thanh_tien:,.2f}"))
        
        # Add to list
        ctpn = ChiTietPhieuNhap(maPN="", maSP=ma_sp, soLuong=so_luong, donGia=don_gia)
        self.ds_chi_tiet_moi.append(ctpn)
        
        # Clear entries
        self.entry_ma_sp.delete(0, tk.END)
        self.entry_so_luong.delete(0, tk.END)
        self.entry_don_gia.delete(0, tk.END)
        self.entry_ma_sp.focus()
    
    def xoa_chi_tiet(self):
        selected_item = self.tree_them_chi_tiet.selection()
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn chi tiết cần xóa")
            return
        
        # Get index
        item = self.tree_them_chi_tiet.item(selected_item[0])
        index = int(item['text']) - 1
        
        # Remove from list
        if 0 <= index < len(self.ds_chi_tiet_moi):
            self.ds_chi_tiet_moi.pop(index)
        
        # Remove from treeview
        self.tree_them_chi_tiet.delete(selected_item)
        
        # Update indices
        for i, item_id in enumerate(self.tree_them_chi_tiet.get_children()):
            self.tree_them_chi_tiet.item(item_id, text=str(i+1))
    
    def luu_phieu_nhap(self):
        # Get values
        ma_pn = self.entry_ma_pn.get().strip()
        ma_nv = self.entry_ma_nv.get().strip()
        ngay_tao_str = self.entry_ngay_tao.get().strip()
        
        # Validate
        if not ma_pn:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã phiếu nhập")
            return
        
        if not ma_nv:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã nhân viên")
            return
        
        try:
            ngay_tao = datetime.strptime(ngay_tao_str, "%Y/%m/%d").date()
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày tạo không hợp lệ (YYYY/MM/DD)")
            return
        
        if not self.ds_chi_tiet_moi:
            messagebox.showerror("Lỗi", "Vui lòng thêm ít nhất một chi tiết phiếu nhập")
            return
        
        # Check if maPN exists
        for pn in self.ds_phieu_nhap.ds:
            if pn.maPN == ma_pn:
                messagebox.showerror("Lỗi", "Mã phiếu nhập đã tồn tại")
                return
        
        # Create phiếu nhập
        pn_moi = PhieuNhap(maPN=ma_pn, maNV=ma_nv, ngayTao=ngay_tao)
        
        # Add chi tiết
        for ctpn in self.ds_chi_tiet_moi:
            ctpn.maPN = ma_pn
            pn_moi.dsctpn.ds.append(ctpn)
        
        # Calculate total
        pn_moi.tongTien = pn_moi.tinh_tong_tien()
        
        # Add to list
        self.ds_phieu_nhap.ds.append(pn_moi)
        
        # Refresh
        self.load_phieu_nhap()
        
        # Clear form
        self.entry_ma_pn.delete(0, tk.END)
        self.entry_ma_nv.delete(0, tk.END)
        self.entry_ngay_tao.delete(0, tk.END)
        self.entry_ngay_tao.insert(0, datetime.today().strftime("%Y/%m/%d"))
        
        for item in self.tree_them_chi_tiet.get_children():
            self.tree_them_chi_tiet.delete(item)
        
        self.ds_chi_tiet_moi = []
        
        messagebox.showinfo("Thành công", "Đã thêm phiếu nhập thành công")
        
        # Switch to list tab
        self.notebook.select(0)
    
    def sua_phieu_nhap(self):
        selected_item = self.tree_phieu_nhap.selection()
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn phiếu nhập cần sửa")
            return
        
        # Get phiếu nhập
        item = self.tree_phieu_nhap.item(selected_item[0])
        ma_pn = item['values'][0]
        
        # Find phiếu nhập
        for pn in self.ds_phieu_nhap.ds:
            if pn.maPN == ma_pn:
                # Create dialog
                dialog = SuaPhieuNhapDialog(self.root, pn)
                self.root.wait_window(dialog.top)
                
                # Refresh
                self.load_phieu_nhap()
                break
    
    def tim_phieu_nhap(self):
        ma_pn = self.entry_tim_ma_pn.get().strip()
        
        if not ma_pn:
            messagebox.showinfo("Thông báo", "Vui lòng nhập mã phiếu nhập cần tìm")
            return
        
        # Clear result
        self.text_result.delete(1.0, tk.END)
        
        # Find phiếu nhập
        found = False
        for pn in self.ds_phieu_nhap.ds:
            if pn.maPN == ma_pn:
                found = True
                
                # Display result
                self.text_result.insert(tk.END, f"Mã PN: {pn.maPN}\n")
                self.text_result.insert(tk.END, f"Mã nhân viên: {pn.maNV}\n")
                self.text_result.insert(tk.END, f"Ngày tạo: {pn.ngayTao}\n")
                self.text_result.insert(tk.END, f"Tổng tiền: {pn.tongTien:,.2f}\n\n")
                
                self.text_result.insert(tk.END, "Chi tiết phiếu nhập:\n")
                self.text_result.insert(tk.END, "| Mã SP   | Số lượng  | Đơn giá    | Thành tiền  |\n")
                self.text_result.insert(tk.END, "-" * 50 + "\n")
                
                for ctpn in pn.dsctpn.ds:
                    self.text_result.insert(tk.END, f"| {ctpn.maSP:<10} | {ctpn.soLuong:<9} | {ctpn.donGia:<10,.2f}| {ctpn.thanhTien:<11,.2f}|\n")
                
                break
        
        if not found:
            self.text_result.insert(tk.END, "Không tìm thấy phiếu nhập!")


class SuaPhieuNhapDialog:
    def __init__(self, parent, phieu_nhap):
        self.phieu_nhap = phieu_nhap
        
        self.top = tk.Toplevel(parent)
        self.top.title("Sửa phiếu nhập")
        self.top.geometry("600x500")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Frame for phiếu nhập info
        frame_info = ttk.LabelFrame(self.top, text="Thông tin phiếu nhập")
        frame_info.pack(fill='x', padx=10, pady=10)
        
        # Phiếu nhập fields
        ttk.Label(frame_info, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_ma_pn = ttk.Entry(frame_info, width=30)
        self.entry_ma_pn.grid(row=0, column=1, padx=5, pady=5)
        self.entry_ma_pn.insert(0, phieu_nhap.maPN)
        self.entry_ma_pn.configure(state="readonly")
        
        ttk.Label(frame_info, text="Mã nhân viên:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_ma_nv = ttk.Entry(frame_info, width=30)
        self.entry_ma_nv.grid(row=1, column=1, padx=5, pady=5)
        self.entry_ma_nv.insert(0, phieu_nhap.maNV)
        
        ttk.Label(frame_info, text="Ngày tạo (YYYY/MM/DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_ngay_tao = ttk.Entry(frame_info, width=30)
        self.entry_ngay_tao.grid(row=2, column=1, padx=5, pady=5)
        self.entry_ngay_tao.insert(0, phieu_nhap.ngayTao.strftime("%Y/%m/%d"))
        
        # Frame for chi tiết phiếu nhập
        frame_chi_tiet = ttk.LabelFrame(self.top, text="Chi tiết phiếu nhập")
        frame_chi_tiet.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for chi tiết
        self.tree_chi_tiet = ttk.Treeview(frame_chi_tiet, columns=("Mã SP", "Số lượng", "Đơn giá", "Thành tiền"))
        self.tree_chi_tiet.heading("#0", text="STT")
        self.tree_chi_tiet.heading("Mã SP", text="Mã SP")
        self.tree_chi_tiet.heading("Số lượng", text="Số lượng")
        self.tree_chi_tiet.heading("Đơn giá", text="Đơn giá")
        self.tree_chi_tiet.heading("Thành tiền", text="Thành tiền")
        
        self.tree_chi_tiet.column("#0", width=50)
        self.tree_chi_tiet.column("Mã SP", width=100)
        self.tree_chi_tiet.column("Số lượng", width=100)
        self.tree_chi_tiet.column("Đơn giá", width=150)
        self.tree_chi_tiet.column("Thành tiền", width=150)
        
        scrollbar = ttk.Scrollbar(frame_chi_tiet, orient="vertical", command=self.tree_chi_tiet.yview)
        self.tree_chi_tiet.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_chi_tiet.pack(fill="both", expand=True)
        
        # Load chi tiết
        for i, ctpn in enumerate(phieu_nhap.dsctpn.ds):
            self.tree_chi_tiet.insert("", "end", text=str(i+1), 
                                     values=(ctpn.maSP, ctpn.soLuong, 
                                            f"{ctpn.donGia:,.2f}", 
                                            f"{ctpn.thanhTien:,.2f}"))
        
        # Buttons
        frame_buttons = ttk.Frame(self.top)
        frame_buttons.pack(fill='x', padx=10, pady=10)
        
        btn_sua_chi_tiet = ttk.Button(frame_buttons, text="Sửa chi tiết", command=self.sua_chi_tiet)
        btn_sua_chi_tiet.pack(side="left", padx=5)
        
        btn_luu = ttk.Button(frame_buttons, text="Lưu thay đổi", command=self.luu_thay_doi)
        btn_luu.pack(side="right", padx=5)
        
        btn_huy = ttk.Button(frame_buttons, text="Hủy", command=self.top.destroy)
        btn_huy.pack(side="right", padx=5)
    
    def sua_chi_tiet(self):
        selected_item = self.tree_chi_tiet.selection()
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn chi tiết cần sửa")
            return
        
        # Get chi tiết
        item = self.tree_chi_tiet.item(selected_item[0])
        index = int(item['text']) - 1
        ma_sp = item['values'][0]
        so_luong_cu = item['values'][1]
        don_gia_cu = float(item['values'][2].replace(',', ''))
        
        # Create dialog
        dialog = SuaChiTietDialog(self.top, ma_sp, so_luong_cu, don_gia_cu)
        self.top.wait_window(dialog.top)
        
        if dialog.result:
            # Update chi tiết
            ctpn = self.phieu_nhap.dsctpn.ds[index]
            ctpn.soLuong = dialog.so_luong
            ctpn.donGia = dialog.don_gia
            ctpn.thanhTien = ctpn.soLuong * ctpn.donGia
            
            # Update treeview
            self.tree_chi_tiet.item(selected_item, values=(
                ctpn.maSP, ctpn.soLuong, f"{ctpn.donGia:,.2f}", f"{ctpn.thanhTien:,.2f}"
            ))
    
    def luu_thay_doi(self):
        # Get values
        ma_nv = self.entry_ma_nv.get().strip()
        ngay_tao_str = self.entry_ngay_tao.get().strip()
        
        # Validate
        if not ma_nv:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã nhân viên")
            return
        
        try:
            ngay_tao = datetime.strptime(ngay_tao_str, "%Y/%m/%d").date()
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày tạo không hợp lệ (YYYY/MM/DD)")
            return
        
        # Update phiếu nhập
        self.phieu_nhap.maNV = ma_nv
        self.phieu_nhap.ngayTao = ngay_tao
        self.phieu_nhap.tongTien = self.phieu_nhap.tinh_tong_tien()
        
        messagebox.showinfo("Thành công", "Đã cập nhật phiếu nhập thành công")
        self.top.destroy()


class SuaChiTietDialog:
    def __init__(self, parent, ma_sp, so_luong, don_gia):
        self.result = False
        
        self.top = tk.Toplevel(parent)
        self.top.title("Sửa chi tiết phiếu nhập")
        self.top.geometry("400x150")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Frame
        frame = ttk.Frame(self.top, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Fields
        ttk.Label(frame, text="Mã sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_ma_sp = ttk.Entry(frame, width=30)
        self.entry_ma_sp.grid(row=0, column=1, padx=5, pady=5)
        self.entry_ma_sp.insert(0, ma_sp)
        self.entry_ma_sp.configure(state="readonly")
        
        ttk.Label(frame, text="Số lượng:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_so_luong = ttk.Entry(frame, width=30)
        self.entry_so_luong.grid(row=1, column=1, padx=5, pady=5)
        self.entry_so_luong.insert(0, str(so_luong))
        
        ttk.Label(frame, text="Đơn giá:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_don_gia = ttk.Entry(frame, width=30)
        self.entry_don_gia.grid(row=2, column=1, padx=5, pady=5)
        self.entry_don_gia.insert(0, str(don_gia))
        
        # Buttons
        frame_buttons = ttk.Frame(frame)
        frame_buttons.grid(row=3, column=0, columnspan=2, pady=10)
        
        btn_luu = ttk.Button(frame_buttons, text="Lưu", command=self.luu)
        btn_luu.pack(side="left", padx=5)
        
        btn_huy = ttk.Button(frame_buttons, text="Hủy", command=self.top.destroy)
        btn_huy.pack(side="left", padx=5)
    
    def luu(self):
        # Get values
        so_luong_str = self.entry_so_luong.get().strip()
        don_gia_str = self.entry_don_gia.get().strip()
        
        # Validate
        try:
            so_luong = int(so_luong_str)
            if so_luong <= 0:
                raise ValueError("Số lượng phải lớn hơn 0")
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng không hợp lệ")
            return
        
        try:
            don_gia = float(don_gia_str)
            if don_gia <= 0:
                raise ValueError("Đơn giá phải lớn hơn 0")
        except ValueError:
            messagebox.showerror("Lỗi", "Đơn giá không hợp lệ")
            return
        
        # Set result
        self.so_luong = so_luong
        self.don_gia = don_gia
        self.result = True
        
        self.top.destroy()


def main():
    root = tk.Tk()
    app = PhieuNhapGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()