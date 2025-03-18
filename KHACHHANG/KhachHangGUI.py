import tkinter as tk
from tkinter import ttk, messagebox

class KhachHangUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        # Tạo thanh tiêu đề + nút Đóng cho khung này
        top_bar = tk.Frame(self, bg="#F0F0F0")
        top_bar.pack(fill='x', pady=5)
        
        label_title = tk.Label(top_bar, text="Quản Lý Khách Hàng", font=("Arial", 14, "bold"), bg="#F0F0F0")
        label_title.pack(side="left", padx=10)
        
        btn_close = tk.Button(top_bar, text="Đóng", command=self.close_frame, bg="red", fg="white")
        btn_close.pack(side="right", padx=10)
        
        # Dữ liệu khách hàng (giả lập CSDL)
        self.customers = [
            {"maKH": "KH001", "tenKH": "Nguyễn Văn A", "diaChi": "Hà Nội",   "dienThoai": "0123456789"},
            {"maKH": "KH002", "tenKH": "Trần Thị B",    "diaChi": "TP.HCM",  "dienThoai": "0987654321"},
            {"maKH": "KH003", "tenKH": "Lê Văn C",      "diaChi": "Đà Nẵng", "dienThoai": "0909090909"}
        ]
        
        # Notebook chứa các tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        # Tạo 5 tab: Thêm, Sửa, Tìm kiếm, Danh sách, Xóa
        self.tab_them = ttk.Frame(self.notebook)
        self.tab_sua = ttk.Frame(self.notebook)
        self.tab_tim = ttk.Frame(self.notebook)
        self.tab_danhsach = ttk.Frame(self.notebook)
        self.tab_xoa = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_them, text="Thêm khách hàng")
        self.notebook.add(self.tab_sua, text="Sửa thông tin khách hàng")
        self.notebook.add(self.tab_tim, text="Tìm kiếm khách hàng")
        self.notebook.add(self.tab_danhsach, text="Danh sách khách hàng")
        self.notebook.add(self.tab_xoa, text="Xóa khách hàng")
        
        # Xây dựng giao diện cho từng tab
        self.create_tab_them()
        self.create_tab_sua()
        self.create_tab_tim()
        self.create_tab_danhsach()
        self.create_tab_xoa()

    def close_frame(self):
        """Đóng khung Quản Lý Khách Hàng."""
        self.destroy()

    def create_tab_them(self):
        frame = self.tab_them
        tk.Label(frame, text="Mã khách hàng:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_id = tk.Entry(frame)
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tên khách hàng:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Địa chỉ:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_address = tk.Entry(frame)
        self.entry_address.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Điện thoại:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_phone = tk.Entry(frame)
        self.entry_phone.grid(row=3, column=1, padx=10, pady=10)
        
        btn_add = tk.Button(frame, text="Thêm khách hàng", command=self.add_customer)
        btn_add.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

    def create_tab_sua(self):
        frame = self.tab_sua
        tk.Label(frame, text="Mã khách hàng cần sửa:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_id = tk.Entry(frame)
        self.entry_update_id.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tên mới:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_name = tk.Entry(frame)
        self.entry_update_name.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Địa chỉ mới:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_address = tk.Entry(frame)
        self.entry_update_address.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Điện thoại mới:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_phone = tk.Entry(frame)
        self.entry_update_phone.grid(row=3, column=1, padx=10, pady=10)
        
        btn_update = tk.Button(frame, text="Sửa khách hàng", command=self.update_customer)
        btn_update.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

    def create_tab_tim(self):
        frame = self.tab_tim
        tk.Label(frame, text="Nhập từ khóa tìm kiếm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_search = tk.Entry(frame)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)
        
        btn_search = tk.Button(frame, text="Tìm kiếm", command=self.search_customer)
        btn_search.grid(row=0, column=2, padx=10, pady=10)
        
        columns = ("maKH", "tenKH", "diaChi", "dienThoai")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def create_tab_danhsach(self):
        frame = self.tab_danhsach
        btn_refresh = tk.Button(frame, text="Tải lại danh sách", command=self.load_all_customers)
        btn_refresh.pack(pady=10)

        columns = ("maKH", "tenKH", "diaChi", "dienThoai")
        self.tree_ds = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_ds.heading(col, text=col)
        self.tree_ds.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_all_customers()

    def create_tab_xoa(self):
        frame = self.tab_xoa
        tk.Label(frame, text="Mã khách hàng cần xóa:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_delete_id = tk.Entry(frame)
        self.entry_delete_id.grid(row=0, column=1, padx=10, pady=10)
        
        btn_delete = tk.Button(frame, text="Xóa khách hàng", command=self.delete_customer)
        btn_delete.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def load_all_customers(self):
        for item in self.tree_ds.get_children():
            self.tree_ds.delete(item)
        for customer in self.customers:
            self.tree_ds.insert("", "end", values=(
                customer["maKH"],
                customer["tenKH"],
                customer["diaChi"],
                customer["dienThoai"]
            ))

    # ==========================
    # Các hàm xử lý sự kiện
    # ==========================
    def add_customer(self):
        maKH = self.entry_id.get().strip()
        tenKH = self.entry_name.get().strip()
        diaChi = self.entry_address.get().strip()
        dienThoai = self.entry_phone.get().strip()
        
        if not maKH or not tenKH:
            messagebox.showerror("Lỗi", "Mã và tên khách hàng không được để trống!")
            return
        
        if any(cust["maKH"] == maKH for cust in self.customers):
            messagebox.showerror("Lỗi", "Mã khách hàng đã tồn tại!")
            return

        new_customer = {"maKH": maKH, "tenKH": tenKH, "diaChi": diaChi, "dienThoai": dienThoai}
        self.customers.append(new_customer)
        messagebox.showinfo("Thành công", f"Đã thêm khách hàng {maKH}")
        self.load_all_customers()
        
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)

    def update_customer(self):
        maKH = self.entry_update_id.get().strip()
        tenKH = self.entry_update_name.get().strip()
        diaChi = self.entry_update_address.get().strip()
        dienThoai = self.entry_update_phone.get().strip()
        
        for customer in self.customers:
            if customer["maKH"] == maKH:
                customer["tenKH"] = tenKH or customer["tenKH"]
                customer["diaChi"] = diaChi or customer["diaChi"]
                customer["dienThoai"] = dienThoai or customer["dienThoai"]
                messagebox.showinfo("Thành công", f"Đã cập nhật khách hàng {maKH}")
                self.load_all_customers()
                return
        messagebox.showerror("Lỗi", "Không tìm thấy khách hàng cần sửa!")

    def search_customer(self):
        keyword = self.entry_search.get().strip().lower()
        results = [cust for cust in self.customers if keyword in cust["maKH"].lower() 
                   or keyword in cust["tenKH"].lower() 
                   or keyword in cust["diaChi"].lower() 
                   or keyword in cust["dienThoai"].lower()]
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        for customer in results:
            self.tree.insert("", "end", values=(
                customer["maKH"],
                customer["tenKH"],
                customer["diaChi"],
                customer["dienThoai"]
            ))
        if not results:
            messagebox.showinfo("Thông báo", "Không tìm thấy khách hàng phù hợp.")

    def delete_customer(self):
        maKH = self.entry_delete_id.get().strip()
        for idx, customer in enumerate(self.customers):
            if customer["maKH"] == maKH:
                if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng {maKH}?"):
                    del self.customers[idx]
                    messagebox.showinfo("Thành công", f"Đã xóa khách hàng {maKH}")
                    self.load_all_customers()
                return
        messagebox.showerror("Lỗi", "Không tìm thấy khách hàng cần xóa!")


# =========================================
# Code chạy chính (giao diện tổng thể)
# =========================================
if __name__ == "__main__":
    import tkinter as tk
    
    root = tk.Tk()
    root.title("***********QUẢN LÍ CỬA HÀNG*********")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    
    # Tiêu đề MENU màu hồng
    f_tl = tk.Frame(root, height=80, width=screen_width, bg="#FFCAd4")
    f_tl.grid(row=0, column=0, sticky="ew")
    f_tl.grid_propagate(False)
    f_tl.grid_columnconfigure(0, weight=1)
    tl = tk.Label(f_tl, text="MENU", font=("Arial", 24, "bold"), fg="black", bg="#FFCAd4")
    tl.grid(pady=20)
    
    # Thanh menu chính (màu xám)
    top_menu = tk.Frame(root, height=100, width=screen_width, background="#D3D3D3")
    top_menu.grid(row=1, column=0, sticky="ew")
    
    # Khung chính để hiển thị nội dung (ban đầu để trống)
    main_content = tk.Frame(root, bg="white")
    main_content.grid(row=2, column=0, sticky="nsew")
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Thay vì submenu với mũi tên, ta tạo 1 nút Quản Lí Khách hàng duy nhất
    def show_khach_hang_ui():
        for widget in main_content.winfo_children():
            widget.destroy()
        kh_frame = KhachHangUI(main_content)
        kh_frame.pack(fill="both", expand=True)

    # Hàm tạo menu: Tạo menubutton cho label khác, riêng "Quản Lí Khách hàng" tạo 1 nút
    def create_menu(parent, label, values):
        frame = tk.Frame(parent, bd=2, relief="ridge")
        if label == "Quản Lí Khách hàng":
            # Chỉ tạo 1 nút thay vì menubutton
            single_button = tk.Button(frame, text=label, command=show_khach_hang_ui)
            single_button.pack(fill="both", expand=True)
        else:
            menubutton = ttk.Menubutton(frame, text=label, direction="below")
            menu = tk.Menu(menubutton, tearoff=0)
            menubutton.config(menu=menu)
            
            for item in values:
                menu.add_command(label=item, command=lambda i=item: print(f"Chọn: {i}"))
            
            menubutton.pack(fill="both", expand=True)
        return frame

    # Dictionary menu
    options = {
        "Quản Lí Nhân viên": ["Thêm nhân viên", "Sửa thông tin nhân viên", "Tìm kiếm nhân viên", "Trạng thái"],
        "Quản Lí Hóa đơn": ["Tạo hóa đơn", "Tìm kiếm hóa đơn", "Sửa hóa đơn"],
        "Quản Lí Khách hàng": ["Thêm khách hàng", "Sửa thông tin khách hàng", "Tìm kiếm khách hàng", "Xóa khách hàng"],
        "Quản Lí Sách": ["Thêm sản phẩm", "Sửa thông tin sản phẩm", "Tìm kiếm sản phẩm", "Trạng Thái"],
        "Thống Kê Doanh thu": ["Báo cáo ngày", "Báo cáo quý", "Báo cáo năm"],
        "Quản Lí Phiếu nhập": ["Tạo phiếu nhập", "Tìm kiếm phiếu nhập", "Sửa phiếu nhập"]
    }

    i = 0
    for label, vals in options.items():
        top_menu.grid_columnconfigure(i, weight=1)
        menu_btn = create_menu(top_menu, label, vals)
        menu_btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
        i += 1
    
    root.mainloop()


