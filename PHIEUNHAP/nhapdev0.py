from decimal import Decimal
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import scrolledtext
import datetime
from DSCTPhieuNhap import DSCTPhieuNhap
from DSPhieuNhap import DSPhieuNhap

class PhieuNhapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Phiếu Nhập")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")
        
        self.style = ttk.Style()
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", background="white", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Pink.TFrame", background="#ffcad4")  
        
        # Biến lưu trữ thông tin phiếu nhập tạm thời
        self.current_phieu_nhap = None
        self.temp_ct_phieu_nhap = []  
        self.load_data()
        #frame main
        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        #frame header
        self.header_frame = ttk.Frame(self.main_frame, style="Pink.TFrame")
        self.header_frame.pack(fill=tk.X, padx=5, pady=5)
        header_label = ttk.Label(self.header_frame, text="QUẢN LÝ PHIẾU NHẬP", 
                                style="Header.TLabel", background="#ffcad4")
        header_label.pack(pady=10)
        
        #frame tìm kiếm
        self.search_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.search_frame, text="Tìm kiếm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.search_var.trace("w", self.search_phieu_nhap)
        
        #khung btn
        self.button_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.them_button = tk.Button(self.button_frame, text="Thêm", command=self.them_phieu_nhap,
                                  bg="#ffcad4", fg="black", padx=10, pady=5)
        self.them_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.sua_button = tk.Button(self.button_frame, text="Sửa", command=self.sua_phieu_nhap,
                                 bg="#ffcad4", fg="black", padx=10, pady=5)
        self.sua_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.tim_button = tk.Button(self.button_frame, text="Tìm kiếm", command=self.tim_kiem_phieu_nhap,
                                 bg="#ffcad4", fg="black", padx=10, pady=5)
        self.tim_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.in_button = tk.Button(self.button_frame, text="In DS", command=self.in_danh_sach,
                                bg="#ffcad4", fg="black", padx=10, pady=5)
        self.in_button.grid(row=0, column=3, padx=5, pady=5)
        

    def load_data(self):
        self.ds_phieu_nhap = DSPhieuNhap() 
        self.ds_phieu_nhap = self.ds_phieu_nhap.lay_du_lieu_tu_sql()
        self.ds_ct_phieu_nhap = DSCTPhieuNhap()
        self.ds_ct_phieu_nhap= self.ds_ct_phieu_nhap.lay_du_lieu_tu_sql()
        
    def load_phieu_nhap_treeview(self):
       
        for item in self.phieu_nhap_tree.get_children():
            self.phieu_nhap_tree.delete(item)
        
        for pn in self.ds_phieu_nhap:
            formatted_tong_tien = f"{pn[3]:,} VNĐ"
            self.phieu_nhap_tree.insert("", "end", values=(
                pn[0],
                pn[1],
                pn[2],
                formatted_tong_tien
            ))
            
            
    def load_ct_phieu_nhap_treeview(self, maPN):
        """Tải danh sách chi tiết phiếu nhập dựa vào mã phiếu nhập"""
        for item in self.ct_phieu_nhap_tree.get_children():
            self.ct_phieu_nhap_tree.delete(item)

        self.ct_label.configure(text=f"Chi tiết phiếu nhập: {maPN}")

        # Chuyển đổi từ tuple sang dictionary
        column_names = ["id", "maPN", "maSP", "donGia", "thanhTien"]  # Đổi thành tên cột phù hợp với database của bạn
        self.ds_ct_phieu_nhap = [dict(zip(column_names, row)) for row in self.ds_ct_phieu_nhap]

        # Kiểm tra kiểu dữ liệu maPN để tránh lỗi so sánh str vs int
        if len(self.ds_ct_phieu_nhap) > 0 and isinstance(self.ds_ct_phieu_nhap[0]["maPN"], int):
            maPN = int(maPN)

        # Lọc danh sách chi tiết
        ct_list = [ct for ct in self.ds_ct_phieu_nhap if ct["maPN"] == maPN]

        for ct in ct_list:
            formatted_don_gia = f"{ct['donGia']:,} VNĐ"
            formatted_thanh_tien = f"{ct['thanhTien']:,} VNĐ"

            self.ct_phieu_nhap_tree.insert("", "end", values=(
                ct["maSP"],
                ct["donGia"],
                formatted_don_gia,
                formatted_thanh_tien
            ))


    def on_phieu_nhap_select(self, event):
        selected_items = self.phieu_nhap_tree.selection()
        if not selected_items:
            return
        
        selected_item = selected_items[0]
        values = self.phieu_nhap_tree.item(selected_item, "values")

        maPN = values[0]  # Lấy mã phiếu nhập đúng cách

        # Tải chi tiết phiếu nhập
        self.load_ct_phieu_nhap_treeview(maPN)

    def search_phieu_nhap(self, *args):
        search_text = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.phieu_nhap_tree.get_children():
            self.phieu_nhap_tree.delete(item)
            
        # Filter and add phieu nhap data
        for pn in self.ds_phieu_nhap:
            if (search_text in pn["maPN"].lower() or
                search_text in pn["maNV"].lower()):
                
                formatted_tong_tien = f"{pn['tongTien']:,} VNĐ"
                self.phieu_nhap_tree.insert("", "end", values=(
                    pn["maPN"],
                    pn["maNV"],
                    pn["ngayTao"],
                    formatted_tong_tien
                ))

    def tim_kiem_phieu_nhap(self):
        """Show search dialog for advanced searching"""
        search_dialog = tk.Toplevel(self.root)
        search_dialog.title("Tìm kiếm phiếu nhập")
        search_dialog.geometry("400x200")
        search_dialog.transient(self.root)
        search_dialog.grab_set()
        
        # Create search fields
        ttk.Label(search_dialog, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ma_pn_var = tk.StringVar()
        ttk.Entry(search_dialog, textvariable=ma_pn_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(search_dialog, text="Mã nhân viên:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ma_nv_var = tk.StringVar()
        ttk.Entry(search_dialog, textvariable=ma_nv_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        def do_search():
            ma_pn = ma_pn_var.get().lower()
            ma_nv = ma_nv_var.get().lower()
            
            # Clear existing items
            for item in self.phieu_nhap_tree.get_children():
                self.phieu_nhap_tree.delete(item)
                
            # Filter and add phieu nhap data
            for pn in self.ds_phieu_nhap:
                if ((not ma_pn or ma_pn in pn["maPN"].lower()) and
                    (not ma_nv or ma_nv in pn["maNV"].lower())):
                    
                    formatted_tong_tien = f"{pn['tongTien']:,} VNĐ"
                    self.phieu_nhap_tree.insert("", "end", values=(
                        pn["maPN"],
                        pn["maNV"],
                        pn["ngayTao"],
                        formatted_tong_tien
                    ))
            
            search_dialog.destroy()
            
        # Add search button
        ttk.Button(search_dialog, text="Tìm kiếm", command=do_search).grid(row=3, column=1, padx=5, pady=15, sticky="e")

    def them_phieu_nhap(self):
        """Open dialog to add a new phieu nhap"""
        them_dialog = tk.Toplevel(self.root)
        them_dialog.title("Thêm phiếu nhập mới")
        them_dialog.geometry("700x600")
        them_dialog.transient(self.root)
        them_dialog.grab_set()
        
        # Create form fields
        form_frame = ttk.Frame(them_dialog)
        form_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Phieu Nhap info
        ttk.Label(form_frame, text="Thông tin phiếu nhập", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        ttk.Label(form_frame, text="Mã phiếu nhập:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ma_pn_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=ma_pn_var, width=30).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(form_frame, text="Mã nhân viên:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ma_nv_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=ma_nv_var, width=30).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(form_frame, text="Ngày tạo:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ngay_tao_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        date_entry = date_entry(form_frame, width=30, textvariable=ngay_tao_var, date_pattern="yyyy-mm-dd")
        date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        # Chi Tiet Phieu Nhap info
        ttk.Label(form_frame, text="Chi tiết phiếu nhập", font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 10))
        
        ct_frame = ttk.Frame(form_frame)
        ct_frame.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        
        ttk.Label(ct_frame, text="Mã sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ma_sp_var = tk.StringVar()
        ttk.Entry(ct_frame, textvariable=ma_sp_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(ct_frame, text="Số lượng:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        so_luong_var = tk.IntVar(value=1)
        ttk.Spinbox(ct_frame, from_=1, to=1000, textvariable=so_luong_var, width=10).grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        ttk.Label(ct_frame, text="Đơn giá:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        don_gia_var = tk.IntVar(value=0)
        don_gia_entry = ttk.Entry(ct_frame, textvariable=don_gia_var, width=20)
        don_gia_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Function to calculate thanh tien
        def calculate_thanh_tien():
            return so_luong_var.get() * don_gia_var.get()
        
        # Add product button
        def add_product():
            if not ma_sp_var.get():
                messagebox.showerror("Lỗi", "Vui lòng nhập mã sản phẩm!")
                return
                
            # Check if this product already exists in the temp list
            for ct in self.temp_ct_phieu_nhap:
                if ct["maSP"] == ma_sp_var.get():
                    messagebox.showerror("Lỗi", "Sản phẩm này đã tồn tại trong phiếu nhập!")
                    return
            
            so_luong = so_luong_var.get()
            don_gia = don_gia_var.get()
            thanh_tien = calculate_thanh_tien()
            
            # Add to temp list
            self.temp_ct_phieu_nhap.append({
                "maPN": ma_pn_var.get(),
                "maSP": ma_sp_var.get(),
                "soLuong": so_luong,
                "donGia": don_gia,
                "thanhTien": thanh_tien
            })
            
            # Update the temp treeview
            formatted_don_gia = f"{don_gia:,} VNĐ"
            formatted_thanh_tien = f"{thanh_tien:,} VNĐ"
            
            temp_tree.insert("", "end", values=(
                ma_sp_var.get(),
                so_luong,
                formatted_don_gia,
                formatted_thanh_tien
            ))
            
            # Reset product fields
            ma_sp_var.set("")
            so_luong_var.set(1)
            don_gia_var.set(0)
            
            # Update total
            update_total()
        
        ttk.Button(ct_frame, text="Thêm sản phẩm", command=add_product).grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # Create a treeview to display the temp products
        ttk.Label(form_frame, text="Danh sách sản phẩm đã thêm:").grid(row=7, column=0, columnspan=2, sticky="w", pady=(10, 5))
        
        temp_tree_frame = ttk.Frame(form_frame)
        temp_tree_frame.grid(row=8, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        
        temp_tree = ttk.Treeview(temp_tree_frame, 
                              columns=("maSP", "soLuong", "donGia", "thanhTien"),
                              show="headings", height=5)
        
        # Define headings
        temp_tree.heading("maSP", text="Mã SP")
        temp_tree.heading("soLuong", text="SL")
        temp_tree.heading("donGia", text="Đơn Giá")
        temp_tree.heading("thanhTien", text="Thành Tiền")
        
        # Define columns
        temp_tree.column("maSP", width=120)
        temp_tree.column("soLuong", width=80)
        temp_tree.column("donGia", width=120)
        temp_tree.column("thanhTien", width=120)
        
        # Add scrollbar
        temp_scrollbar = ttk.Scrollbar(temp_tree_frame, orient="vertical", command=temp_tree.yview)
        temp_tree.configure(yscrollcommand=temp_scrollbar.set)
        
        # Pack the Treeview and scrollbar
        temp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        temp_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Total amount label
        total_frame = ttk.Frame(form_frame)
        total_frame.grid(row=9, column=0, columnspan=4, sticky="e", padx=5, pady=5)
        
        ttk.Label(total_frame, text="Tổng tiền:").pack(side=tk.LEFT, padx=5)
        total_var = tk.StringVar(value="0 VNĐ")
        ttk.Label(total_frame, textvariable=total_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Function to update total
        def update_total():
            total = sum(ct["thanhTien"] for ct in self.temp_ct_phieu_nhap)
            total_var.set(f"{total:,} VNĐ")
        
        # Button to remove selected product
        def remove_product():
            selected = temp_tree.selection()
            if not selected:
                return
                
            index = temp_tree.index(selected[0])
            temp_tree.delete(selected[0])
            self.temp_ct_phieu_nhap.pop(index)
            update_total()
        
        ttk.Button(temp_tree_frame, text="Xóa sản phẩm", command=remove_product).pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(them_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_phieu_nhap():
            # Validate required fields
            if not ma_pn_var.get() or not ma_nv_var.get() or not ngay_tao_var.get():
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin phiếu nhập!")
                return
                
            # Check if no products added
            if not self.temp_ct_phieu_nhap:
                messagebox.showerror("Lỗi", "Vui lòng thêm ít nhất một sản phẩm vào phiếu nhập!")
                return
                
            # Check if ma_phieu_nhap already exists
            for pn in self.ds_phieu_nhap:
                if pn["maPN"] == ma_pn_var.get():
                    messagebox.showerror("Lỗi", "Mã phiếu nhập đã tồn tại!")
                    return
            
            # Calculate total
            tong_tien = sum(ct["thanhTien"] for ct in self.temp_ct_phieu_nhap)
            
            # Create new phieu nhap
            new_phieu_nhap = {
                "maPN": ma_pn_var.get(),
                "maNV": ma_nv_var.get(),
                "ngayTao": ngay_tao_var.get(),
                "tongTien": tong_tien
            }
            
            # Save to SQL using your existing functions
            # DSPhieuNhap.luu_thong_tin_vao_sql(new_phieu_nhap)
            
            # Save chi tiet phieu nhap
            for ct in self.temp_ct_phieu_nhap:
                # Make sure each CT has the correct maPN
                ct["maPN"] = ma_pn_var.get()
                # DSCTPhieuNhap.luu_thong_tin_vao_sql(ct)
            
            # Add to local data
            self.ds_phieu_nhap.append(new_phieu_nhap)
            self.ds_ct_phieu_nhap.extend(self.temp_ct_phieu_nhap)
            
            # Refresh treeview
            self.load_phieu_nhap_treeview()
            
            # Reset temp list
            self.temp_ct_phieu_nhap = []
            
            # Close dialog
            them_dialog.destroy()
            
            messagebox.showinfo("Thành công", "Đã thêm phiếu nhập mới!")
        
        ttk.Button(button_frame, text="Lưu", command=save_phieu_nhap).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Hủy", command=them_dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def sua_phieu_nhap(self):
        """Open dialog to edit the selected phieu nhap"""
        if not self.current_phieu_nhap:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một phiếu nhập để sửa!")
            return
            
        sua_dialog = tk.Toplevel(self.root)
        sua_dialog.title(f"Sửa phiếu nhập: {self.current_phieu_nhap['maPN']}")
        sua_dialog.geometry("500x300")
        sua_dialog.transient(self.root)
        sua_dialog.grab_set()
        
        # Create form fields
        form_frame = ttk.Frame(sua_dialog)
        form_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ma_pn_var = tk.StringVar(value=self.current_phieu_nhap["maPN"])
        ttk.Entry(form_frame, textvariable=ma_pn_var, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(form_frame, text="Mã nhân viên:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ma_nv_var = tk.StringVar(value=self.current_phieu_nhap["maNV"])
        ttk.Entry(form_frame, textvariable=ma_nv_var).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(form_frame, text="Ngày tạo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ngay_tao_var = tk.StringVar(value=self.current_phieu_nhap["ngayTao"])
        date_entry = date_entry(form_frame, width=30, textvariable=ngay_tao_var, date_pattern="yyyy-mm-dd")
        date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Buttons
        button_frame = ttk.Frame(sua_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_changes():
            # Update phieu nhap
            self.current_phieu_nhap["maNV"] = ma_nv_var.get()
            self.current_phieu_nhap["ngayTao"] = ngay_tao_var.get()
            
            # Save to SQL using your existing functions
            # DSPhieuNhap.luu_thong_tin_vao_sql(self.current_phieu_nhap)
            
            # Update local data
            for i, pn in enumerate(self.ds_phieu_nhap):
                if pn["maPN"] == self.current_phieu_nhap["maPN"]:
                    self.ds_phieu_nhap[i] = self.current_phieu_nhap
                    break
            
            # Refresh treeview
            self.load_phieu_nhap_treeview()
            
            # Close dialog
            sua_dialog.destroy()
            
            messagebox.showinfo("Thành công", "Đã cập nhật phiếu nhập!")
        
        ttk.Button(button_frame, text="Lưu", command=save_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Hủy", command=sua_dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def in_danh_sach(self):
       
        # frmae phieunhap
        self.phieu_nhap_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.phieu_nhap_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(self.phieu_nhap_frame, text="Danh sách phiếu nhập:", 
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        #treeview hthi dspn
        self.phieu_nhap_tree = ttk.Treeview(self.phieu_nhap_frame, 
                                          columns=("maPN", "maNV", "ngayTao", "tongTien"),
                                          show="headings")
        
        self.phieu_nhap_tree.heading("maPN", text="Mã Phiếu Nhập")
        self.phieu_nhap_tree.heading("maNV", text="Mã Nhân Viên")
        self.phieu_nhap_tree.heading("ngayTao", text="Ngày Tạo")
        self.phieu_nhap_tree.heading("tongTien", text="Tổng Tiền")
        self.phieu_nhap_tree.column("maPN", width=120)
        self.phieu_nhap_tree.column("maNV", width=120)
        self.phieu_nhap_tree.column("ngayTao", width=120)
        self.phieu_nhap_tree.column("tongTien", width=120)
        
        
        phieu_nhap_scrollbar = ttk.Scrollbar(self.phieu_nhap_frame, orient="vertical", command=self.phieu_nhap_tree.yview)
        self.phieu_nhap_tree.configure(yscrollcommand=phieu_nhap_scrollbar.set)#thêm thanh cuon
        self.phieu_nhap_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        phieu_nhap_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.phieu_nhap_tree.bind("<<TreeviewSelect>>", self.on_phieu_nhap_select) # Gán sự kiện khi chọn một hàng
        
        # Chi tiet Phieu Nhap Treeview
        self.ct_phieu_nhap_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.ct_phieu_nhap_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.ct_label = ttk.Label(self.ct_phieu_nhap_frame, text="Chi tiết phiếu nhập:", 
                                font=("Arial", 12, "bold"))
        self.ct_label.pack(anchor="w", pady=(10, 5))
        
        # Create Chi tiet Treeview
        self.ct_phieu_nhap_tree = ttk.Treeview(self.ct_phieu_nhap_frame, 
                                            columns=("maSP", "soLuong", "donGia", "thanhTien"),
                                            show="headings")
        
        # Define headings
        self.ct_phieu_nhap_tree.heading("maSP", text="Mã Sản Phẩm")
        self.ct_phieu_nhap_tree.heading("soLuong", text="Số Lượng")
        self.ct_phieu_nhap_tree.heading("donGia", text="Đơn Giá")
        self.ct_phieu_nhap_tree.heading("thanhTien", text="Thành Tiền")
        
        # Define columns
        self.ct_phieu_nhap_tree.column("maSP", width=120)
        self.ct_phieu_nhap_tree.column("soLuong", width=80)
        self.ct_phieu_nhap_tree.column("donGia", width=120)
        self.ct_phieu_nhap_tree.column("thanhTien", width=120)
        
        # Add scrollbar
        ct_scrollbar = ttk.Scrollbar(self.ct_phieu_nhap_frame, orient="vertical", command=self.ct_phieu_nhap_tree.yview)
        self.ct_phieu_nhap_tree.configure(yscrollcommand=ct_scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.ct_phieu_nhap_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ct_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load phieu nhap data
        self.load_phieu_nhap_treeview()
        # Thêm sự kiện khi chọn một phiếu nhập
        self.tree_phieu_nhap.bind("<<TreeviewSelect>>", self.hien_thi_chi_tiet_phieu_nhap)

        danh_sach = self.ds_phieu_nhap.lay_du_lieu_tu_sql()
        if danh_sach:
            for phieu in danh_sach:
                self.tree_phieu_nhap.insert("", "end", values=(phieu[0], phieu[1], phieu[2], phieu[3]))
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

        # Tạo Treeview hiển thị danh sách chi tiết phiếu nhập
        columns_ct = ("maPN", "maSP", "soLuongSP", "donGia", "thanhTien")
        self.tree_chi_tiet = ttk.Treeview(self.frame_thong_tin, columns=columns_ct, show="headings")

        self.tree_chi_tiet.heading("maPN", text="Mã Phiếu Nhập")
        self.tree_chi_tiet.heading("maSP", text="Mã Sản Phẩm")
        self.tree_chi_tiet.heading("soLuongSP", text="Số Lượng")
        self.tree_chi_tiet.heading("donGia", text="Đơn Giá")
        self.tree_chi_tiet.heading("thanhTien", text="Thành Tiền")
        self.tree_chi_tiet.column("maPN", width=100)
        self.tree_chi_tiet.column("maSP", width=100)
        self.tree_chi_tiet.column("soLuongSP", width=100)
        self.tree_chi_tiet.column("donGia", width=100)
        self.tree_chi_tiet.column("thanhTien", width=100)
        self.tree_chi_tiet.pack(fill="both", expand=True)

    def hien_thi_chi_tiet_phieu_nhap(self, event):
        selected_item = self.tree_phieu_nhap.selection()
        if selected_item:
            maPN = self.tree_phieu_nhap.item(selected_item[0])["values"][0]
            # Xóa dữ liệu cũ trên danh sách chi tiết
            for item in self.tree_chi_tiet.get_children():
                self.tree_chi_tiet.delete(item)
                
            danh_sach_ct = self.dsctpn.lay_du_lieu_tu_sql()  
            for ct in danh_sach_ct:
                if ct[0] == maPN:
                    self.tree_chi_tiet.insert("", "end", values=(ct[0], ct[1], ct[2], ct[3], ct[4]))

    
if __name__ == "__main__":
    root = tk.Tk()
    app = PhieuNhapGUI(root)
    root.mainloop()