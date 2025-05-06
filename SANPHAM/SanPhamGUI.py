import tkinter as tk
from tkinter import messagebox, ttk

import pyodbc


class SanPhamGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.products = []  # Danh sách sản phẩm được tải từ SQL
        self.conn = self.ket_noi_sql()  # Thiết lập kết nối SQL
        self.create_widgets()

    def ket_noi_sql(self):
        """ Kết nối với SQL Server """
        try:
            # Sử dụng chuỗi kết nối đầy đủ
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=DESKTOP-NRE55H1;"
                "DATABASE=DOANPYTHON;"
                "Trusted_Connection=yes;"
            )
            print("✅ Kết nối SQL thành công!")
            return conn
        except Exception as e:
            print(f"❌ Lỗi kết nối SQL: {str(e)}")
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
        # Tạo Notebook với các tab chức năng
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Các tab: Thêm, Sửa, Tìm kiếm, Danh sách
        self.tab_them = ttk.Frame(self.notebook)
        self.tab_sua = ttk.Frame(self.notebook)
        self.tab_danhsach = ttk.Frame(self.notebook)
        self.tab_tim = ttk.Frame(self.notebook)

        # Thêm tab vào notebook
        self.notebook.add(self.tab_them, text="Thêm sản phẩm")
        self.notebook.add(self.tab_sua, text="Sửa thông tin sản phẩm")
        self.notebook.add(self.tab_danhsach, text="Danh sách sản phẩm")
        self.notebook.add(self.tab_tim, text="Tìm kiếm sản phẩm")

        # Gọi các hàm tạo giao diện chi tiết cho từng tab
        self.create_tab_them()
        self.create_tab_sua()
        self.create_tab_danhsach()
        self.create_tab_tim()

    def create_tab_them(self):
        frame = self.tab_them
        
        # Tạo form nhập liệu
        form_frame = ttk.LabelFrame(frame, text="Thông tin sản phẩm mới")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tạo các trường nhập liệu
        tk.Label(form_frame, text="Mã sản phẩm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_id = tk.Entry(form_frame)
        self.entry_id.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Tên sản phẩm:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_name = tk.Entry(form_frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Đơn giá:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_price = tk.Entry(form_frame)
        self.entry_price.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Số lượng tồn:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_quantity = tk.Entry(form_frame)
        self.entry_quantity.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Tác giả:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_author = tk.Entry(form_frame)
        self.entry_author.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Nhà xuất bản:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_publisher = tk.Entry(form_frame)
        self.entry_publisher.grid(row=5, column=1, padx=10, pady=10)

        # Nút thêm sản phẩm
        btn_add = tk.Button(form_frame, text="Thêm sản phẩm", command=self.add_product)
        btn_add.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    def create_tab_sua(self):
        frame = self.tab_sua
        
        # Frame chứa form sửa thông tin
        edit_frame = ttk.LabelFrame(frame, text="Thông tin sản phẩm")
        edit_frame.pack(fill="x", padx=10, pady=10)
        
        # Tạo các trường nhập liệu - Cột 1
        left_frame = ttk.Frame(edit_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(left_frame, text="Mã sản phẩm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_update_id = tk.Entry(left_frame, state="normal")
        self.entry_update_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Tên mới:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_update_name = tk.Entry(left_frame)
        self.entry_update_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Đơn giá mới:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_update_price = tk.Entry(left_frame)
        self.entry_update_price.grid(row=2, column=1, padx=5, pady=5)

        # Tạo các trường nhập liệu - Cột 2
        right_frame = ttk.Frame(edit_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(right_frame, text="Số lượng tồn mới:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_update_quantity = tk.Entry(right_frame)
        self.entry_update_quantity.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="Tác giả mới:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_update_author = tk.Entry(right_frame)
        self.entry_update_author.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="Nhà xuất bản mới:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_update_publisher = tk.Entry(right_frame)
        self.entry_update_publisher.grid(row=2, column=1, padx=5, pady=5)

        # Frame chứa các nút
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Nút hủy
        btn_cancel = tk.Button(button_frame, text="Hủy", command=self.clear_edit_fields)
        btn_cancel.pack(side="left", padx=5)
        
        # Nút xác nhận
        btn_confirm = tk.Button(button_frame, text="Xác nhận sửa", command=self.update_product)
        btn_confirm.pack(side="left", padx=5)
        
        # Frame chứa danh sách sản phẩm
        list_frame = ttk.LabelFrame(frame, text="Danh sách sản phẩm")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tạo Treeview để hiển thị danh sách sản phẩm
        columns = ("Mã SP", "Tên SP", "Số Lượng", "Đơn Giá", "Tác Giả", "Nhà Xuất Bản")
        self.tree_sua = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree_sua.heading(col, text=col)
            self.tree_sua.column(col, width=100)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree_sua.yview)
        self.tree_sua.configure(yscrollcommand=scrollbar.set)
        
        self.tree_sua.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Gắn sự kiện chọn sản phẩm từ danh sách
        self.tree_sua.bind('<<TreeviewSelect>>', self.on_select_product)
        
        # Tải danh sách sản phẩm
        self.load_products_to_edit_list()

    def load_products_to_edit_list(self):
        # Xóa dữ liệu cũ
        for item in self.tree_sua.get_children():
            self.tree_sua.delete(item)
            
        # Tải dữ liệu mới
        self.load_products_from_sql()
        
        # Debug: In ra số lượng sản phẩm đã tải
        print(f"Loaded {len(self.products)} products for editing")
        
        # Thêm dữ liệu vào Treeview
        for product in self.products:
            values = (
                product["maSP"],
                product["tenSP"],
                product["soLuongTon"],
                product["donGia"],
                product["tacGia"],
                product["nhaXuatBan"]
            )
            # Debug: In ra giá trị của từng sản phẩm

            self.tree_sua.insert("", "end", values=values)

    def on_select_product(self, event):
        try:
            # Debug: In ra sự kiện
            print("Selection event triggered")
            
            # Lấy sản phẩm được chọn
            selected_item = self.tree_sua.selection()
            print(f"Selected items: {selected_item}")
            
            if not selected_item:
                print("No item selected")
                return
                
            # Lấy dữ liệu của sản phẩm được chọn
            item = selected_item[0]  # Lấy item đầu tiên được chọn
            values = self.tree_sua.item(item)['values']
            
            # Debug: In ra giá trị để kiểm tra
            print("Selected values:", values)
            
            # Xóa nội dung cũ trong các trường nhập
            self.entry_update_id.delete(0, tk.END)
            self.entry_update_name.delete(0, tk.END)
            self.entry_update_quantity.delete(0, tk.END)
            self.entry_update_price.delete(0, tk.END)
            self.entry_update_author.delete(0, tk.END)
            self.entry_update_publisher.delete(0, tk.END)
            
            # Điền thông tin sản phẩm vào các trường nhập
            if values and len(values) >= 6:  # Kiểm tra xem có đủ 6 giá trị không
                # Chuyển đổi tất cả giá trị sang string
                maSP = str(values[0])
                tenSP = str(values[1])
                soLuongTon = str(values[2])
                donGia = str(values[3])
                tacGia = str(values[4])
                nhaXuatBan = str(values[5])
                
                # Debug: In ra giá trị đã chuyển đổi
                print("Converted values:")
                print(f"maSP: {maSP} (type: {type(maSP)})")
                print(f"tenSP: {tenSP} (type: {type(tenSP)})")
                print(f"soLuongTon: {soLuongTon} (type: {type(soLuongTon)})")
                print(f"donGia: {donGia} (type: {type(donGia)})")
                print(f"tacGia: {tacGia} (type: {type(tacGia)})")
                print(f"nhaXuatBan: {nhaXuatBan} (type: {type(nhaXuatBan)})")
                
                # Điền vào các trường
                self.entry_update_id.config(state="normal")  # Tạm thời cho phép chỉnh sửa
                self.entry_update_id.delete(0, tk.END)
                self.entry_update_id.insert(0, maSP)
                self.entry_update_id.config(state="readonly")  # Khóa lại sau khi điền
                
                self.entry_update_name.insert(0, tenSP)
                self.entry_update_quantity.insert(0, soLuongTon)
                self.entry_update_price.insert(0, donGia)
                self.entry_update_author.insert(0, tacGia)
                self.entry_update_publisher.insert(0, nhaXuatBan)
                
                # Debug: In ra giá trị đã điền
                print("Filled values:")
                print("ID:", self.entry_update_id.get())
                print("Name:", self.entry_update_name.get())
                print("Quantity:", self.entry_update_quantity.get())
                print("Price:", self.entry_update_price.get())
                print("Author:", self.entry_update_author.get())
                print("Publisher:", self.entry_update_publisher.get())
            else:
                print("Error: Invalid values format")
                
        except Exception as e:
            print("Error in on_select_product:", str(e))
            messagebox.showerror("Lỗi", f"Có lỗi khi chọn sản phẩm: {str(e)}")

    def update_product(self):
        try:
            # Lấy dữ liệu từ các trường nhập
            maSP = self.entry_update_id.get().strip()
            tenSP = self.entry_update_name.get().strip()
            soLuongTon_str = self.entry_update_quantity.get().strip()
            donGia_str = self.entry_update_price.get().strip()
            tacGia = self.entry_update_author.get().strip()
            nhaXuatBan = self.entry_update_publisher.get().strip()

            # Kiểm tra dữ liệu đầu vào
            if not maSP:
                messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm cần sửa!")
                return

            if not tenSP:
                messagebox.showerror("Lỗi", "Tên sản phẩm không được để trống!")
                return

            # Chuyển đổi số lượng và đơn giá
            try:
                soLuongTon = int(soLuongTon_str)
                donGia = float(donGia_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng tồn và đơn giá phải là số!")
                return

            # Tải lại danh sách để đảm bảo dữ liệu mới nhất
            self.load_products_from_sql()

            # Tìm sản phẩm trong danh sách
            product = next((p for p in self.products if str(p["maSP"]) == str(maSP)), None)
            if not product:
                messagebox.showerror("Lỗi", f"Không tìm thấy sản phẩm với mã {maSP}")
                return

            # Xác nhận trước khi cập nhật
            if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn cập nhật thông tin sản phẩm {maSP}?"):
                return

            # Cập nhật trong SQL
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE SanPham SET tenSP = ?, soLuongTon = ?, donGia = ?, tacGia = ?, nhaXuatBan = ? WHERE maSP = ?",
                (tenSP, soLuongTon, donGia, tacGia, nhaXuatBan, maSP)
            )
            self.conn.commit()

            # Cập nhật trong danh sách cục bộ
            product["tenSP"] = tenSP
            product["soLuongTon"] = soLuongTon
            product["donGia"] = donGia
            product["tacGia"] = tacGia
            product["nhaXuatBan"] = nhaXuatBan

            # Cập nhật giao diện
            self.load_products_to_edit_list()
            self.load_all_products()
            self.clear_edit_fields()

            messagebox.showinfo("Thành công", f"Đã cập nhật sản phẩm {maSP}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            return

    def create_tab_danhsach(self):
        frame = self.tab_danhsach
        
        # Tạo Treeview để hiển thị danh sách sản phẩm
        columns = ("Mã SP", "Tên SP", "Số Lượng", "Đơn Giá", "Tác Giả", "Nhà Xuất Bản")
        self.tree_ds = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Đặt tiêu đề cho các cột
        for col in columns:
            self.tree_ds.heading(col, text=col)
            self.tree_ds.column(col, width=100)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree_ds.yview)
        self.tree_ds.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí các widget
        self.tree_ds.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Thêm nút Xuất Excel vào cuối danh sách
        btn_xuat_excel = tk.Button(frame, text="Xuất Excel", command=self.xuatExcel, bg="#2196F3", fg="white")
        btn_xuat_excel.pack(side="bottom", anchor="e", padx=10, pady=5)
        
        # Tải danh sách sản phẩm
        self.load_all_products()

    def load_all_products(self):
        # Tải dữ liệu từ SQL
        self.load_products_from_sql()
        
        # Xóa dữ liệu cũ trong treeview
        for item in self.tree_ds.get_children():
            self.tree_ds.delete(item)
        
        # Thêm dữ liệu mới vào treeview
        for product in self.products:
            self.tree_ds.insert("", "end", values=(
                product["maSP"],
                product["tenSP"],
                product["soLuongTon"],
                product["donGia"],
                product["tacGia"],
                product["nhaXuatBan"]
            ))

    def create_tab_tim(self):
        frame = self.tab_tim
        
        # Frame chứa ô tìm kiếm
        search_frame = ttk.LabelFrame(frame, text="Tìm kiếm sản phẩm")
        search_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(search_frame, text="Nhập mã sản phẩm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_search = tk.Entry(search_frame)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)

        btn_search = tk.Button(search_frame, text="Tìm kiếm", command=self.search_product)
        btn_search.grid(row=0, column=2, padx=10, pady=10)

        # Frame chứa kết quả tìm kiếm
        result_frame = ttk.LabelFrame(frame, text="Kết quả tìm kiếm")
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Mã SP", "Tên SP", "Số Lượng", "Đơn Giá", "Tác Giả", "Nhà Xuất Bản")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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
        if any(prod["maSP"]==maSP for prod in self.products):
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

        new_product = {"maSP": maSP, "tenSP": tenSP, "soLuongTon": soLuongTon, "donGia": donGia, "tacGia": tacGia,
                       "nhaXuatBan": nhaXuatBan}
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
            if str(prod["maSP"])==product_code:
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

    def anGiaoDien(self):
        """Ẩn giao diện quản lý sản phẩm"""
        self.pack_forget()

    def hienThi(self, action):
        """Hiển thị giao diện theo hành động được chọn"""
        # Ẩn tất cả các tab
        for tab in self.notebook.tabs():
            self.notebook.hide(tab)
        
        # Hiển thị tab tương ứng với hành động
        if action == "Thêm sản phẩm":
            self.notebook.select(self.tab_them)
        elif action == "Sửa thông tin sản phẩm":
            self.notebook.select(self.tab_sua)
            self.load_products_to_edit_list()
        elif action == "Tìm kiếm sản phẩm":
            self.notebook.select(self.tab_tim)
            self.load_products_from_sql()
        elif action == "Danh sách sản phẩm":
            self.notebook.select(self.tab_danhsach)
            self.load_products_from_sql()
            self.load_all_products()
        
        # Hiển thị giao diện
        self.pack(fill="both", expand=True)

    def clear_edit_fields(self):
        """Xóa nội dung các trường nhập liệu"""
        self.entry_update_id.delete(0, tk.END)
        self.entry_update_name.delete(0, tk.END)
        self.entry_update_quantity.delete(0, tk.END)
        self.entry_update_price.delete(0, tk.END)
        self.entry_update_author.delete(0, tk.END)
        self.entry_update_publisher.delete(0, tk.END)

    def xuatExcel(self):
        """Xuất danh sách sản phẩm ra file Excel"""
        try:
            import openpyxl
            from openpyxl.styles import Alignment, Font, PatternFill
            from openpyxl.utils import get_column_letter

            # Lấy danh sách sản phẩm
            self.load_products_from_sql()
            ds = self.products
            if not ds:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu sản phẩm để xuất!")
                return

            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Lưu file Excel"
            )
            if not file_path:
                return

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Danh sách sản phẩm"

            headers = ["Mã SP", "Tên SP", "Số lượng tồn", "Đơn giá", "Tác giả", "Nhà xuất bản"]
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")

            for row, sp in enumerate(ds, 2):
                ws.cell(row=row, column=1, value=sp["maSP"])
                ws.cell(row=row, column=2, value=sp["tenSP"])
                ws.cell(row=row, column=3, value=sp["soLuongTon"])
                ws.cell(row=row, column=4, value=sp["donGia"])
                ws.cell(row=row, column=5, value=sp["tacGia"])
                ws.cell(row=row, column=6, value=sp["nhaXuatBan"])

            for col in range(1, len(headers) + 1):
                ws.column_dimensions[get_column_letter(col)].width = 18

            wb.save(file_path)
            messagebox.showinfo("Thành công", f"Đã xuất danh sách sản phẩm thành công!\nFile được lưu tại: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi xuất file Excel:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý sách")
    root.geometry("800x600")
    app = SanPhamGUI(root)
    root.mainloop()