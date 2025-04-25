import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class SanPhamGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.customers = []  # Danh sách khách hàng được tải từ SQL
        self.conn = self.ket_noi_sql()  # Thiết lập kết nối SQL
        self.create_widgets()

    def ket_noi_sql(self):
        """ Kết nối với SQL Server """
        try:
            conn = pyodbc.connect(
                "DRIVER={SQL Server};"
                "SERVER=LAPTOP-H2KMKBBS\MSSQLSERVER01;"  # Thay bằng tên server của bạn
                "DATABASE=DOANPYTHON;"            # Thay bằng tên database của bạn
            )
            print("✅ Kết nối SQL thành công!")
            return conn
        except Exception as e:
            messagebox.showerror("Lỗi kết nối SQL", str(e))
            return None
    def load_products_from_sql(self):
        """Tải danh sách sản phẩm từ SQL Server"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan FROM SanPham")
            rows = cursor.fetchall()
            
            self.products = []  # Khởi tạo danh sách sản phẩm
            for row in rows:
                self.products.append({
                    "maSP": row[0],
                    "tenSP": row[1],
                    "soLuongTon": row[2],
                    "donGia": row[3],
                    "tacGia": row[4],
                    "nhaXuatBan": row[5]
                })
            print(f"✅ Đã tải {len(self.products)} sản phẩm từ SQL!")
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))

    def create_widgets(self):
        # Tạo thanh tiêu đề + nút Đóng
        top_bar = tk.Frame(self, bg="#F0F0F0")
        top_bar.pack(fill='x', pady=5)

        label_title = tk.Label(top_bar, text="Quản Lý Sản Phẩm", font=("Arial", 14, "bold"), bg="#F0F0F0")
        label_title.pack(side="left", padx=10)

        btn_close = tk.Button(top_bar, text="Đóng", command=self.close_frame, bg="red", fg="white")
        btn_close.pack(side="right", padx=10)

        # Tạo Notebook với các tab chức năng
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Các tab: Thêm, Sửa, Xóa, Tìm kiếm, Trạng thái
        self.tab_them = ttk.Frame(self.notebook)
        self.tab_sua = ttk.Frame(self.notebook)
        self.tab_xoa = ttk.Frame(self.notebook)
        self.tab_danhsach = ttk.Frame(self.notebook)
        self.tab_tim = ttk.Frame(self.notebook)  # Tab Tìm kiếm
        

        # Thêm tab vào notebook
        self.notebook.add(self.tab_them, text="Thêm sản phẩm")
        self.notebook.add(self.tab_sua, text="Sửa thông tin sản phẩm")
        self.notebook.add(self.tab_xoa, text="Xóa sản phẩm")
        self.notebook.add(self.tab_danhsach, text="Danh sách sản phẩm")
        self.notebook.add(self.tab_tim, text="Tìm kiếm sản phẩm") 
        

        # Gọi các hàm tạo giao diện chi tiết cho từng tab
        self.create_tab_them()
        self.create_tab_sua()
        self.create_tab_xoa()
        self.create_tab_danhsach()
        self.create_tab_tim()  # Đảm bảo hàm này tồn tại
        

    
    def close_frame(self):
        """Đóng khung Quản Lý Sản Phẩm."""
        self.destroy()

    def create_tab_them(self):
        frame = self.tab_them
        tk.Label(frame, text="Mã sản phẩm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_id = tk.Entry(frame)
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tên sản phẩm:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Số lượng tồn:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_quantity = tk.Entry(frame)
        self.entry_quantity.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Đơn giá:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_price = tk.Entry(frame)
        self.entry_price.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tác giả:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_author = tk.Entry(frame)
        self.entry_author.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Nhà xuất bản:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_publisher = tk.Entry(frame)
        self.entry_publisher.grid(row=5, column=1, padx=10, pady=10)
        
        btn_add = tk.Button(frame, text="Thêm sản phẩm", command=self.add_product)
        btn_add.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    def create_tab_sua(self):
        frame = self.tab_sua
        tk.Label(frame, text="Mã sản phẩm cần sửa:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_id = tk.Entry(frame)
        self.entry_update_id.grid(row=0, column=1, padx=10, pady=10)
        self.entry_update_id.bind("<FocusOut>", self.prefill_product_info)
        
        tk.Label(frame, text="Tên mới:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_name = tk.Entry(frame)
        self.entry_update_name.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Đơn giá mới:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_price = tk.Entry(frame)
        self.entry_update_price.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Số lượng tồn mới:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_quantity = tk.Entry(frame)
        self.entry_update_quantity.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tác giả mới:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_author = tk.Entry(frame)
        self.entry_update_author.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Nhà xuất bản mới:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_publisher = tk.Entry(frame)
        self.entry_update_publisher.grid(row=5, column=1, padx=10, pady=10)
        
        btn_update = tk.Button(frame, text="Sửa sản phẩm", command=self.update_product)
        btn_update.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    def create_tab_tim(self):
        frame = self.tab_tim
        tk.Label(frame, text="Nhập mã sản phẩm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_search = tk.Entry(frame)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)

        btn_search = tk.Button(frame, text="Tìm kiếm", command=self.search_product)
        btn_search.grid(row=0, column=2, padx=10, pady=10)

        columns = ("Mã SP", "Tên SP", "Số Lượng", "Đơn Giá", "Tác Giả", "Nhà Xuất Bản")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)
    def create_tab_danhsach(self):
        frame = self.tab_danhsach
        btn_refresh = tk.Button(frame, text="Tải lại danh sách", command=self.load_all_products)
        btn_refresh.pack(pady=10)

        # Cập nhật danh sách các cột, thêm cột trạng thái
        columns = ("maSP", "tenSP", "soLuong", "giaSP", "tacGia", "nhaXuatBan", "trangThai")
        self.tree_ds = ttk.Treeview(frame, columns=columns, show="headings")

        # Đặt tiêu đề cho các cột
        self.tree_ds.heading("maSP", text="Mã SP")
        self.tree_ds.heading("tenSP", text="Tên SP")
        self.tree_ds.heading("soLuong", text="Số Lượng")
        self.tree_ds.heading("giaSP", text="Giá Sản Phẩm")
        self.tree_ds.heading("tacGia", text="Tác Giả")
        self.tree_ds.heading("nhaXuatBan", text="Xuất Bản")
        self.tree_ds.heading("trangThai", text="Trạng Thái")

        self.tree_ds.pack(fill="both", expand=True, padx=10, pady=10)

        # Tải lại danh sách sản phẩm
        self.load_all_products()

    def create_tab_xoa(self):
        frame = self.tab_xoa
        tk.Label(frame, text="Mã sản phẩm cần xóa:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_delete_id = tk.Entry(frame)
        self.entry_delete_id.grid(row=0, column=1, padx=10, pady=10)
        
        btn_delete = tk.Button(frame, text="Xóa sản phẩm", command=self.delete_product)
        btn_delete.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def create_tab_trangthai(self):
        frame = self.tab_trangthai
        tk.Label(frame, text="Thống kê trạng thái sản phẩm", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame chứa các thống kê
        stats_frame = tk.Frame(frame)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Các thống kê cần hiển thị
        tk.Label(stats_frame, text="Tổng số sản phẩm:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.lbl_total_products = tk.Label(stats_frame, text="0")
        self.lbl_total_products.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(stats_frame, text="Sản phẩm có số lượng < 10:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.lbl_low_stock = tk.Label(stats_frame, text="0")
        self.lbl_low_stock.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(stats_frame, text="Giá trị tồn kho:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.lbl_stock_value = tk.Label(stats_frame, text="0 VND")
        self.lbl_stock_value.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Bảng hiển thị sản phẩm có số lượng thấp
        tk.Label(frame, text="Sản phẩm cần nhập thêm (số lượng < 10)", font=("Arial", 11)).pack(pady=5)
        
        columns = ("maSP", "tenSP", "soLuongTon", "donGia", "tacGia", "nhaXuatBan")
        self.tree_low_stock = ttk.Treeview(frame, columns=columns, show="headings", height=5)
        for col in columns:
            self.tree_low_stock.heading(col, text=col)
        self.tree_low_stock.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Nút cập nhật trạng thái
        btn_update_status = tk.Button(frame, text="Cập nhật trạng thái", command=self.update_product_status)
        btn_update_status.pack(pady=10)

    def load_all_products(self):
        # Cập nhật dữ liệu từ SQL trước
        self.load_products_from_sql()

        # Xóa toàn bộ dữ liệu hiện có trong treeview
        for item in self.tree_ds.get_children():
            self.tree_ds.delete(item)

        # Chèn lại dữ liệu từ self.products
        for product in self.products:
            # Tính trạng thái sản phẩm dựa trên số lượng
            trang_thai = "Còn hàng" if product["soLuongTon"] > 0 else "Hết hàng"
            
            self.tree_ds.insert("", "end", values=(
                product["maSP"],
                product["tenSP"],
                product["soLuongTon"],
                product["donGia"],
                product["tacGia"],
                product["nhaXuatBan"],
                trang_thai  # Trạng thái sản phẩm
            ))


    
    # ==========================
    # Các hàm xử lý sự kiện
    # ==========================
    def add_product(self):
        maSP = self.entry_id.get().strip()
        tenSP = self.entry_name.get().strip()
        soLuongTon = self.entry_quantity.get().strip()
        donGia = self.entry_price.get().strip()
        tacGia = self.entry_author.get().strip()
        nhaXuatBan = self.entry_publisher.get().strip()
        
        if not maSP or not tenSP:
            messagebox.showerror("Lỗi", "Mã và tên sản phẩm không được để trống!")
            return
        
        # Kiểm tra số lượng và đơn giá có phải là số không
        try:
            if soLuongTon:
                soLuongTon = int(soLuongTon)
            else:
                soLuongTon = 0
                
            if donGia:
                donGia = float(donGia)
            else:
                donGia = 0.0
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng tồn và đơn giá phải là số!")
            return
        
        # Kiểm tra tồn tại trên SQL (nếu cần) hoặc trong danh sách cục bộ
        if any(prod["maSP"] == maSP for prod in self.products):
            messagebox.showerror("Lỗi", "Mã sản phẩm đã tồn tại!")
            return

        # Thêm sản phẩm vào SQL
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO SanPham (maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan) VALUES (?, ?, ?, ?, ?, ?)",
                    (maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan)
                )
                self.conn.commit()
            except Exception as e:
                messagebox.showerror("Lỗi SQL", str(e))
                return

        new_product = {"maSP": maSP, "tenSP": tenSP, "soLuongTon": soLuongTon, "donGia": donGia, "tacGia": tacGia, "nhaXuatBan": nhaXuatBan}
        self.products.append(new_product)
        messagebox.showinfo("Thành công", f"Đã thêm sản phẩm {maSP}")
        self.load_all_products()
        
        # Xóa các trường nhập
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_publisher.delete(0, tk.END)

    def update_product(self):
        maSP_str = self.entry_update_id.get().strip()
        tenSP = self.entry_update_name.get().strip()
        soLuongTon_str = self.entry_update_quantity.get().strip()
        donGia_str = self.entry_update_price.get().strip()
        tacGia = self.entry_update_author.get().strip()
        nhaXuatBan = self.entry_update_publisher.get().strip()

        if not maSP_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã sản phẩm!")
            return

        try:
            # Chuyển đổi mã sản phẩm sang kiểu số nguyên nếu có thể
            maSP = int(maSP_str)
        except ValueError:
            # Nếu không thể chuyển sang số nguyên, giữ nguyên dạng chuỗi
            maSP = maSP_str

        # Chuyển đổi số lượng tồn và đơn giá sang số (nếu có)
        soLuongTon = None
        if soLuongTon_str:
            try:
                soLuongTon = int(soLuongTon_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng tồn phải là số nguyên!")
                return

        donGia = None
        if donGia_str:
            try:
                donGia = float(donGia_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Đơn giá phải là số!")
                return

        # Tải lại danh sách trước khi tìm
        self.load_products_from_sql()

        # Tìm sản phẩm trong self.products
        product = next((p for p in self.products if p["maSP"] == maSP), None)
        if not product:
            messagebox.showerror("Lỗi", f"Không tìm thấy sản phẩm với mã {maSP_str}")
            return

        # Kiểm tra xem người dùng đã nhập thông tin mới chưa
        if not any([tenSP, soLuongTon is not None, donGia is not None, tacGia, nhaXuatBan]):
            messagebox.showwarning("Cảnh báo", "Không có thông tin nào được cập nhật!")
            return
        
        # Hiển thị hộp thoại xác nhận trước khi cập nhật
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn cập nhật thông tin sản phẩm {maSP_str}?"):
            return

        # Cập nhật trong SQL
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE SanPham SET tenSP = ?, soLuongTon = ?, donGia = ?, tacGia = ?, nhaXuatBan = ? WHERE maSP = ?",
                (tenSP or product["tenSP"],
                soLuongTon if soLuongTon is not None else product["soLuongTon"],
                donGia if donGia is not None else product["donGia"],
                tacGia or product["tacGia"],
                nhaXuatBan or product["nhaXuatBan"],
                maSP)
            )
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
            return

        # Cập nhật trong danh sách cục bộ
        product["tenSP"] = tenSP or product["tenSP"]
        product["soLuongTon"] = soLuongTon if soLuongTon is not None else product["soLuongTon"]
        product["donGia"] = donGia if donGia is not None else product["donGia"]
        product["tacGia"] = tacGia or product["tacGia"]
        product["nhaXuatBan"] = nhaXuatBan or product["nhaXuatBan"]

        messagebox.showinfo("Thành công", f"Đã cập nhật sản phẩm {maSP_str}")
        self.load_all_products()
        
        # Xóa nội dung các ô nhập sau khi cập nhật thành công
        self.entry_update_id.delete(0, tk.END)
        self.entry_update_name.delete(0, tk.END)
        self.entry_update_quantity.delete(0, tk.END)
        self.entry_update_price.delete(0, tk.END)
        self.entry_update_author.delete(0, tk.END)
        self.entry_update_publisher.delete(0, tk.END)

    def search_product(self):
        # Tải lại danh sách trước khi tìm
        self.load_products_from_sql()

        product_code = self.entry_search.get().strip()
        results = []
        
        # Kiểm tra nếu trường tìm kiếm trống
        if not product_code:
            messagebox.showinfo("Thông báo", "Vui lòng nhập mã sản phẩm.")
            return
        
        # Chỉ tìm sản phẩm theo mã chính xác
        for prod in self.products:
            # Tìm theo mã sản phẩm chính xác
            if str(prod["maSP"]) == product_code:
                results.append(prod)
        
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Chèn kết quả
        for product in results:
            self.tree.insert("", "end", values=(
                product["maSP"],
                product["tenSP"],
                product["soLuongTon"],
                product["donGia"],
                product["tacGia"],
                product["nhaXuatBan"]
            ))

        if not results:
            messagebox.showinfo("Thông báo", "Không tìm thấy sản phẩm với mã này.")
        else:
            messagebox.showinfo("Thông báo", f"Tìm thấy sản phẩm với mã: {product_code}")
    def delete_product(self):
        maSP = self.entry_delete_id.get().strip()
        
        if not maSP:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã sản phẩm cần xóa!")
            return
        
        # Tải lại danh sách để đảm bảo dữ liệu mới nhất
        self.load_products_from_sql()
        
        # Kiểm tra sản phẩm có tồn tại không
        product_exists = False
        for product in self.products:
            if str(product["maSP"]) == maSP:
                product_exists = True
                break
        
        if not product_exists:
            messagebox.showerror("Lỗi", f"Không tìm thấy sản phẩm có mã '{maSP}'!")
            return
            
        # Xác nhận trước khi xóa
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sản phẩm {maSP}?"):
            return
            
        # Xóa trên SQL
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM SanPham WHERE maSP = ?", (maSP,))
            row_count = cursor.rowcount
            self.conn.commit()
            
            if row_count > 0:
                messagebox.showinfo("Thành công", f"Đã xóa sản phẩm {maSP}")
                # Tải lại danh sách và xóa nội dung ô nhập
                self.load_all_products()
                self.entry_delete_id.delete(0, tk.END)
            else:
                messagebox.showwarning("Cảnh báo", f"Không có sản phẩm nào bị xóa với mã {maSP}")
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
    
    def update_product_status(self):
        """Cập nhật trạng thái của sản phẩm"""
        maSP_str = self.entry_trangthai_id.get().strip()
        trangThai = self.combo_trangthai.get()
        
        if not maSP_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã sản phẩm!")
            return
        
        try:
            # Chuyển đổi mã sản phẩm sang kiểu số nguyên nếu có thể
            maSP = int(maSP_str)
        except ValueError:
            # Nếu không thể chuyển sang số nguyên, giữ nguyên dạng chuỗi
            maSP = maSP_str
        
        # Kiểm tra sản phẩm có tồn tại không
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM SanPham WHERE maSP = ?", (maSP,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            messagebox.showerror("Lỗi", f"Không tìm thấy sản phẩm với mã {maSP_str}")
            return
        
        # Hiển thị hộp thoại xác nhận trước khi cập nhật
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn cập nhật trạng thái sản phẩm {maSP_str} thành '{trangThai}'?"):
            return
        
        # Cập nhật trạng thái trong SQL
        try:
            cursor.execute("UPDATE SanPham SET trangThai = ? WHERE maSP = ?", (trangThai, maSP))
            self.conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật trạng thái sản phẩm {maSP_str} thành '{trangThai}'")
            
            # Xóa nội dung ô nhập và làm mới danh sách
            self.entry_trangthai_id.delete(0, tk.END)
            self.load_product_status()
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))

    def prefill_product_info(self, event=None):
        maSP = self.entry_update_id.get().strip()
        if not maSP:
            return

        self.load_products_from_sql()

        product = next((p for p in self.products if str(p["maSP"]) == maSP), None)
        if product:
            # Xóa dữ liệu hiện tại trong các trường nhập
            self.entry_update_name.delete(0, tk.END)
            self.entry_update_quantity.delete(0, tk.END)
            self.entry_update_price.delete(0, tk.END)
            self.entry_update_author.delete(0, tk.END)
            self.entry_update_publisher.delete(0, tk.END)

            # Điền thông tin sản phẩm hiện có
            self.entry_update_name.insert(0, product["tenSP"])
            self.entry_update_quantity.insert(0, str(product["soLuongTon"]))
            self.entry_update_price.insert(0, str(product["donGia"]))
            self.entry_update_author.insert(0, product["tacGia"])
            self.entry_update_publisher.insert(0, product["nhaXuatBan"])
        else:
            # Nếu không tìm thấy sản phẩm, xóa tất cả trường
            self.entry_update_name.delete(0, tk.END)
            self.entry_update_quantity.delete(0, tk.END)
            self.entry_update_price.delete(0, tk.END)
            self.entry_update_author.delete(0, tk.END)
            self.entry_update_publisher.delete(0, tk.END)
            messagebox.showinfo("Thông báo", f"Không tìm thấy sản phẩm có mã {maSP}")


# =========================================
# Code chạy chính (giao diện tổng thể)
# =========================================
if __name__ == "__main__":
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
    
    # Nút Quản Lí Sản phẩm
    def show_san_pham_ui():
        for widget in main_content.winfo_children():
            widget.destroy()
        sp_frame = SanPhamGUI(main_content)
        sp_frame.pack(fill="both", expand=True)

    def create_menu(parent, label, values):
        frame = tk.Frame(parent, bd=2, relief="ridge")
        if label == "Quản Lí Sách":
            # Tạo nút thay vì menubutton
            single_button = tk.Button(frame, text=label, command=show_san_pham_ui)
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
        "Quản Lí Sách": ["Thêm sản phẩm", "Sửa thông tin sản phẩm", "Tìm kiếm sản phẩm", "Danh Sách Sản phẩm"],
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