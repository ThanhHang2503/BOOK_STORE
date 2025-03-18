import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# ------------------------------
# Giả sử bạn đã có class KhachHangGUI (code của bạn đã gửi)
# ------------------------------
class KhachHangGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # ... (code KhachHangGUI như bạn đã gửi)
        tk.Label(self, text="Giao diện Quản Lí Khách Hàng").pack()

# ------------------------------
# Class SanPhamGUI tương tự KhachHangGUI
# ------------------------------
class SanPhamGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # Kết nối đến SQL Server bằng pyodbc
        try:
            connection_string = (
                "DRIVER={SQL Server};"
                "SERVER=LAPTOP-H2KMKBBS\\MSSQLSERVER01;"  # Thay đổi theo server của bạn
                "DATABASE=DOANPYTHON;"                    # Thay đổi theo database của bạn
                "UID=HiHi;"                              # Thay đổi theo user của bạn
                "PWD=111111;"                            # Thay đổi theo mật khẩu của bạn
            )
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Không thể kết nối đến CSDL: {e}")
            return

        # Tạo bảng SanPham nếu chưa tồn tại
        self.create_table()

        # Thanh tiêu đề + nút Đóng
        top_bar = tk.Frame(self, bg="#F0F0F0")
        top_bar.pack(fill='x', pady=5)
        label_title = tk.Label(top_bar, text="Quản Lý Sản Phẩm", font=("Arial", 14, "bold"), bg="#F0F0F0")
        label_title.pack(side="left", padx=10)
        btn_close = tk.Button(top_bar, text="Đóng", command=self.close_frame, bg="red", fg="white")
        btn_close.pack(side="right", padx=10)

        # Notebook chứa các tab thao tác
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Tạo 5 tab: Thêm, Sửa, Tìm kiếm, Danh sách, Xóa
        self.tab_them = ttk.Frame(self.notebook)
        self.tab_sua = ttk.Frame(self.notebook)
        self.tab_tim = ttk.Frame(self.notebook)
        self.tab_danhsach = ttk.Frame(self.notebook)
        self.tab_xoa = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_them, text="Thêm sản phẩm")
        self.notebook.add(self.tab_sua, text="Sửa sản phẩm")
        self.notebook.add(self.tab_tim, text="Tìm kiếm sản phẩm")
        self.notebook.add(self.tab_danhsach, text="Danh sách sản phẩm")
        self.notebook.add(self.tab_xoa, text="Xóa sản phẩm")

        # Xây dựng giao diện cho từng tab
        self.create_tab_them()
        self.create_tab_sua()
        self.create_tab_tim()
        self.create_tab_danhsach()
        self.create_tab_xoa()

    def create_table(self):
        """Tạo bảng SanPham nếu chưa tồn tại."""
        try:
            self.cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SanPham')
                BEGIN
                    CREATE TABLE SanPham (
                        maSP VARCHAR(50) PRIMARY KEY,
                        tenSP NVARCHAR(255),
                        soLuongTon INT,
                        donGia FLOAT,
                        tacGia NVARCHAR(255),
                        nhaXuatBan NVARCHAR(255)
                    )
                END
            """)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"Không thể tạo bảng: {e}")

    def close_frame(self):
        """Đóng khung Quản Lý Sản Phẩm và kết nối CSDL."""
        try:
            self.conn.close()
        except:
            pass
        self.destroy()

    # --------------------------
    # Tab Thêm sản phẩm
    # --------------------------
    def create_tab_them(self):
        frame = self.tab_them
        tk.Label(frame, text="Mã sản phẩm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_maSP = tk.Entry(frame)
        self.entry_maSP.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tên sản phẩm:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_tenSP = tk.Entry(frame)
        self.entry_tenSP.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Số lượng tồn:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_soLuongTon = tk.Entry(frame)
        self.entry_soLuongTon.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Đơn giá:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_donGia = tk.Entry(frame)
        self.entry_donGia.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tác giả:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_tacGia = tk.Entry(frame)
        self.entry_tacGia.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Nhà xuất bản:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_nhaXuatBan = tk.Entry(frame)
        self.entry_nhaXuatBan.grid(row=5, column=1, padx=10, pady=10)
        
        btn_add = tk.Button(frame, text="Thêm sản phẩm", command=self.add_product)
        btn_add.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    def add_product(self):
        maSP = self.entry_maSP.get().strip()
        tenSP = self.entry_tenSP.get().strip()
        soLuongTon = self.entry_soLuongTon.get().strip()
        donGia = self.entry_donGia.get().strip()
        tacGia = self.entry_tacGia.get().strip()
        nhaXuatBan = self.entry_nhaXuatBan.get().strip()

        if not maSP or not tenSP:
            messagebox.showerror("Lỗi", "Mã và tên sản phẩm không được để trống!")
            return

        try:
            self.cursor.execute("SELECT COUNT(*) FROM SanPham WHERE maSP = ?", (maSP,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Lỗi", "Mã sản phẩm đã tồn tại!")
                return

            soLuongTon = int(soLuongTon) if soLuongTon else 0
            donGia = float(donGia) if donGia else 0.0

            self.cursor.execute("""
                INSERT INTO SanPham (maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan))
            self.conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm sản phẩm {maSP}")
            self.load_all_products()
            self.entry_maSP.delete(0, tk.END)
            self.entry_tenSP.delete(0, tk.END)
            self.entry_soLuongTon.delete(0, tk.END)
            self.entry_donGia.delete(0, tk.END)
            self.entry_tacGia.delete(0, tk.END)
            self.entry_nhaXuatBan.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {e}")

    # --------------------------
    # Tab Sửa sản phẩm
    # --------------------------
    def create_tab_sua(self):
        frame = self.tab_sua
        tk.Label(frame, text="Mã sản phẩm cần sửa:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_maSP = tk.Entry(frame)
        self.entry_update_maSP.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tên mới:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_tenSP = tk.Entry(frame)
        self.entry_update_tenSP.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Số lượng tồn mới:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_soLuongTon = tk.Entry(frame)
        self.entry_update_soLuongTon.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Đơn giá mới:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_donGia = tk.Entry(frame)
        self.entry_update_donGia.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Tác giả mới:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_tacGia = tk.Entry(frame)
        self.entry_update_tacGia.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Nhà xuất bản mới:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_update_nhaXuatBan = tk.Entry(frame)
        self.entry_update_nhaXuatBan.grid(row=5, column=1, padx=10, pady=10)
        
        btn_update = tk.Button(frame, text="Sửa sản phẩm", command=self.update_product)
        btn_update.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

    def update_product(self):
        maSP = self.entry_update_maSP.get().strip()
        tenSP = self.entry_update_tenSP.get().strip()
        soLuongTon = self.entry_update_soLuongTon.get().strip()
        donGia = self.entry_update_donGia.get().strip()
        tacGia = self.entry_update_tacGia.get().strip()
        nhaXuatBan = self.entry_update_nhaXuatBan.get().strip()

        try:
            self.cursor.execute("SELECT COUNT(*) FROM SanPham WHERE maSP = ?", (maSP,))
            if self.cursor.fetchone()[0] == 0:
                messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm cần sửa!")
                return

            soLuongTon = int(soLuongTon) if soLuongTon else 0
            donGia = float(donGia) if donGia else 0.0

            self.cursor.execute("""
                UPDATE SanPham 
                SET tenSP = ?, soLuongTon = ?, donGia = ?, tacGia = ?, nhaXuatBan = ?
                WHERE maSP = ?
            """, (tenSP, soLuongTon, donGia, tacGia, nhaXuatBan, maSP))
            self.conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật sản phẩm {maSP}")
            self.load_all_products()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sản phẩm: {e}")

    # --------------------------
    # Tab Tìm kiếm sản phẩm
    # --------------------------
    def create_tab_tim(self):
        frame = self.tab_tim
        tk.Label(frame, text="Nhập từ khóa tìm kiếm:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_search = tk.Entry(frame)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)
        btn_search = tk.Button(frame, text="Tìm kiếm", command=self.search_product)
        btn_search.grid(row=0, column=2, padx=10, pady=10)

        columns = ("maSP", "tenSP", "soLuongTon", "donGia", "tacGia", "nhaXuatBan")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def search_product(self):
        keyword = self.entry_search.get().strip().lower()
        pattern = f"%{keyword}%"
        try:
            query = """
                SELECT maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan
                FROM SanPham 
                WHERE lower(maSP) LIKE ? OR lower(tenSP) LIKE ? OR lower(tacGia) LIKE ? OR lower(nhaXuatBan) LIKE ?
            """
            self.cursor.execute(query, (pattern, pattern, pattern, pattern))
            rows = self.cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)
            for row in rows:
                self.tree.insert("", "end", values=row)
            if not rows:
                messagebox.showinfo("Thông báo", "Không tìm thấy sản phẩm phù hợp.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {e}")

    # --------------------------
    # Tab Danh sách sản phẩm
    # --------------------------
    def create_tab_danhsach(self):
        frame = self.tab_danhsach
        btn_refresh = tk.Button(frame, text="Tải lại danh sách", command=self.load_all_products)
        btn_refresh.pack(pady=10)

        columns = ("maSP", "tenSP", "soLuongTon", "donGia", "tacGia", "nhaXuatBan")
        self.tree_ds = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree_ds.heading(col, text=col)
        self.tree_ds.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_all_products()

    def load_all_products(self):
        for item in self.tree_ds.get_children():
            self.tree_ds.delete(item)
        try:
            self.cursor.execute("SELECT maSP, tenSP, soLuongTon, donGia, tacGia, nhaXuatBan FROM SanPham")
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree_ds.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách: {e}")

    # --------------------------
    # Tab Xóa sản phẩm
    # --------------------------
    def create_tab_xoa(self):
        frame = self.tab_xoa
        tk.Label(frame, text="Mã sản phẩm cần xóa:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_delete_maSP = tk.Entry(frame)
        self.entry_delete_maSP.grid(row=0, column=1, padx=10, pady=10)
        btn_delete = tk.Button(frame, text="Xóa sản phẩm", command=self.delete_product)
        btn_delete.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def delete_product(self):
        maSP = self.entry_delete_maSP.get().strip()
        try:
            self.cursor.execute("SELECT COUNT(*) FROM SanPham WHERE maSP = ?", (maSP,))
            if self.cursor.fetchone()[0] == 0:
                messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm cần xóa!")
                return
            if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sản phẩm {maSP}?"):
                self.cursor.execute("DELETE FROM SanPham WHERE maSP = ?", (maSP,))
                self.conn.commit()
                messagebox.showinfo("Thành công", f"Đã xóa sản phẩm {maSP}")
                self.load_all_products()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {e}")

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass

# ------------------------------
# Giao diện tổng thể của cửa hàng
# ------------------------------
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

    # Khung chính để hiển thị nội dung (ban đầu trống)
    main_content = tk.Frame(root, bg="white")
    main_content.grid(row=2, column=0, sticky="nsew")
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Hàm gọi giao diện của Khách hàng và Sản phẩm

    def show_san_pham_ui():
        for widget in main_content.winfo_children():
            widget.destroy()
        sp_frame = SanPhamGUI(main_content)
        sp_frame.pack(fill="both", expand=True)

    # Hàm tạo menu: Với "Quản Lí Khách hàng" và "Quản Lí Sách" dùng nút đơn, các mục khác dùng Menubutton
    def create_menu(parent, label, values):
        frame = tk.Frame(parent, bd=2, relief="ridge")
        if label == "Quản Lí Sách":
            btn = tk.Button(frame, text=label, command=show_san_pham_ui)
            btn.pack(fill="both", expand=True)
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

