
from tkinter import messagebox, ttk
import tkinter as tk
from DSPhieuNhap import DSPhieuNhap
from DSCTPhieuNhap import DSCTPhieuNhap
class PhieuNhapGUI:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Quản Lý Phiếu Nhập")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")
        
        # Khởi tạo các đối tượng 
        self.ds_phieu_nhap = DSPhieuNhap()  
        self.ds_phieu_nhap.lay_du_lieu_tu_sql() 
        self.dsctpn= DSCTPhieuNhap()
        self.frame_buttons = tk.Frame(master)#khung chứa menu
        self.frame_buttons.pack(fill="x", padx=10, pady=5)
        self.frame_thong_tin = None #khung tt
        self.tree = None
        self.ds_chi_tiet = []
        #các btn
        self.btn_them = tk.Button(self.frame_buttons, text="Thêm", command=self.them, bg="#FFCAd4")
        self.btn_them.pack(side="left", fill="both", expand=True)
        self.btn_xoa = tk.Button(self.frame_buttons, text="Xóa", command=self.xoa_chi_tiet, bg="#FFCAd4")
        self.btn_xoa.pack(side="left", fill="both", expand=True)
        self.btn_sua = tk.Button(self.frame_buttons, text="Sửa", command=self.sua_phieu_nhap, bg="#FFCAd4")
        self.btn_sua.pack(side="left", fill="both", expand=True)
        self.btn_tim = tk.Button(self.frame_buttons, text="Tìm kiếm", command=self.tim_chi_tiet, bg="#FFCAd4")
        self.btn_tim.pack(side="left", fill="both", expand=True)
        self.btn_in = tk.Button(self.frame_buttons, text="In danh sách", command=self.in_danh_sach, bg="#FFCAd4")
        self.btn_in.pack(side="left", fill="both", expand=True)
         
         
    def reset_frame(self):
        if self.frame_thong_tin:
            self.frame_thong_tin.pack_forget()
            self.frame_thong_tin.destroy()
        self.frame_thong_tin = tk.Frame(self.master)
        self.frame_thong_tin.pack(pady=10, fill="both", expand=True)

    
    
    def them(self):
        
        self.reset_frame()

        self.label_maPN = tk.Label(self.frame_thong_tin, text="Mã Phiếu Nhập:")
        self.label_maPN.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_maPN = tk.Entry(self.frame_thong_tin)
        self.entry_maPN.grid(row=0, column=1, padx=10, pady=5)

        self.label_maNV = tk.Label(self.frame_thong_tin, text="Mã Nhân Viên:")
        self.label_maNV.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_maNV = tk.Entry(self.frame_thong_tin)
        self.entry_maNV.grid(row=1, column=1, padx=10, pady=5)

        self.label_ngayTao = tk.Label(self.frame_thong_tin, text="Ngày Tạo:")
        self.label_ngayTao.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_ngayTao = tk.Entry(self.frame_thong_tin)
        self.entry_ngayTao.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.frame_thong_tin, text="Thêm Chi Tiết Phiếu Nhập", command=self.them_CTphieuNhap).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(self.frame_thong_tin, text="Lưu Phiếu Nhập", command=self.luu_phieu_nhap, bg="#90EE90").grid(row=4, column=0, columnspan=2, pady=10)

        self.frame_chi_tiet = tk.Frame(self.frame_thong_tin)
        self.frame_chi_tiet.grid(row=5, column=0, columnspan=2, pady=10)
        self.tree = ttk.Treeview(self.frame_chi_tiet, columns=("maSP", "soLuong", "donGia", "thanhTien"), show="headings")
        self.tree.heading("maSP", text="Mã SP")
        self.tree.heading("soLuong", text="Số Lượng")
        self.tree.heading("donGia", text="Đơn Giá")
        self.tree.heading("thanhTien", text="Thành Tiền")
        self.tree.column("maSP", width=100)
        self.tree.column("soLuong", width=100)
        self.tree.column("donGia", width=100)
        self.tree.column("thanhTien", width=100)
        # Ẩn Treeview lúc đầu
        self.frame_chi_tiet.grid_remove()

    def them_CTphieuNhap(self):
        self.ctpn_them = tk.Toplevel(self.master)
        self.ctpn_them.title("Thêm Chi Tiết Phiếu Nhập")
        self.ctpn_them.geometry("500x400")

        tk.Label(self.ctpn_them, text="Mã Sản Phẩm:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_maSP = tk.Entry(self.ctpn_them)
        self.entry_maSP.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.ctpn_them, text="Số Lượng:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_soLuong = tk.Entry(self.ctpn_them)
        self.entry_soLuong.grid(row=1, column=1, padx=10, pady=5)
        self.entry_soLuong.bind("<KeyRelease>", self.tinh_thanh_tien)

        tk.Label(self.ctpn_them, text="Đơn Giá:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_donGia = tk.Entry(self.ctpn_them)
        self.entry_donGia.grid(row=2, column=1, padx=10, pady=5)
        self.entry_donGia.bind("<KeyRelease>", self.tinh_thanh_tien)

        tk.Label(self.ctpn_them, text="Thành Tiền:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_thanhTien = tk.Entry(self.ctpn_them, state="readonly")
        self.entry_thanhTien.grid(row=3, column=1, padx=10, pady=5)

        # Nút Thêm vào danh sách
        self.btn_luu = tk.Button(self.ctpn_them, text="Thêm", command=self.them_vao_table, bg="#90EE90")
        self.btn_luu.grid(row=4, column=0, pady=10)

        # Tạo bảng hiển thị sản phẩm đã thêm
        self.tree = ttk.Treeview(self.ctpn_them, columns=("maSP", "soLuong", "donGia", "thanhTien"), show="headings")
        self.tree.heading("maSP", text="Mã SP")
        self.tree.heading("soLuong", text="Số Lượng")
        self.tree.heading("donGia", text="Đơn Giá")
        self.tree.heading("thanhTien", text="Thành Tiền")
        self.tree.column("maSP", width=100)
        self.tree.column("soLuong", width=100)
        self.tree.column("donGia", width=100)
        self.tree.column("thanhTien", width=100)
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def them_vao_table(self):
        maSP = self.entry_maSP.get()
        soLuong = self.entry_soLuong.get()
        donGia = self.entry_donGia.get()

        if not maSP or not soLuong or not donGia:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            soLuong = int(soLuong)
            donGia = int(donGia)
            thanhTien = soLuong * donGia
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng và đơn giá phải là số!")
            return
          
        self.ds_chi_tiet.append((maSP, soLuong, donGia, thanhTien))
        self.ctpn_them.destroy()
        self.hien_thi_chi_tiet()
    def hien_thi_chi_tiet(self):
        self.frame_chi_tiet.grid()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for chi_tiet in self.ds_chi_tiet:
            self.tree.insert("", "end", values=chi_tiet)

    def reset_ctpn_them(self):
        #Xóa dữ liệu trên form nhưng vẫn giữ dữ liệu trong danh sách
        self.entry_maSP.delete(0, tk.END)
        self.entry_soLuong.delete(0, tk.END)
        self.entry_donGia.delete(0, tk.END)
        self.entry_thanhTien.config(state="normal")
        self.entry_thanhTien.delete(0, tk.END)
        self.entry_thanhTien.config(state="readonly")

    def luu_chi_tiet(self):
        #Lưu danh sách chi tiết vào SQL"""
        maPN = self.entry_maPN.get()
        if not self.ds_chi_tiet:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để lưu!")
            return
        for chi_tiet in self.ds_chi_tiet:
            maSP, soLuong, donGia, thanhTien = chi_tiet
            self.DSCTPhieuNhap.luu_chi_tiet_vao_sql(maPN, maSP, soLuong, donGia, thanhTien)

        messagebox.showinfo("Thành công", "Lưu tất cả chi tiết phiếu nhập thành công!")
        self.ctpn_them.destroy() 

        
    def luu_phieu_nhap(self):
        maPN = self.entry_maPN.get()
        maNV = self.entry_maNV.get()
        ngayTao = self.entry_ngayTao.get()

        if not maPN or not maNV or not ngayTao:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin phiếu nhập!")
            return

        if self.DSPhieuNhap.kiem_tra_trung_ma_phieu_nhap(maPN):
            messagebox.showwarning("Cảnh báo", "Mã phiếu nhập đã tồn tại, vui lòng nhập mã khác!")
            return

        if self.DSPhieuNhap.luu_thong_tin_vao_sql(maPN, maNV, ngayTao, 0):  
            messagebox.showinfo("Thành công", "Lưu phiếu nhập thành công!")
            self.reset_frame()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu phiếu nhập!")

    def luu_chi_tiet(self):
        maPN = self.entry_maPN.get()
        maSP = self.entry_maSP.get()
        soLuong = self.entry_soLuong.get()
        donGia = self.entry_donGia.get()

        if not maPN or not maSP or not soLuong or not donGia:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin chi tiết phiếu nhập!")
            return

        soLuong = int(soLuong)
        donGia = int(donGia)
        thanhTien = soLuong * donGia

        if self.DSCTPhieuNhap.kiem_tra_phieu_nhap_chua_maSP(maPN, maSP):
            messagebox.showwarning("Cảnh báo", "Sản phẩm đã có trong phiếu nhập này!")
            return

        if self.DSCTPhieuNhap.luu_chi_tiet_vao_sql(maPN, maSP, soLuong, donGia, thanhTien):
            messagebox.showinfo("Thành công", "Lưu chi tiết phiếu nhập thành công!")
            self.cap_nhat_tong_tien(maPN)  # Cập nhật tổng tiền phiếu nhập sau khi thêm chi tiết
        else:
            messagebox.showerror("Lỗi", "Không thể lưu chi tiết phiếu nhập!")

    def tinh_thanh_tien(self, event=None):
        try:
            so_luong = int(self.entry_soLuong.get()) if self.entry_soLuong.get() else 0
            don_gia = int(self.entry_donGia.get()) if self.entry_donGia.get() else 0
            thanh_tien = so_luong * don_gia

            self.entry_thanhTien.config(state="normal")
            self.entry_thanhTien.delete(0, tk.END)
            self.entry_thanhTien.insert(0, str(thanh_tien))
            self.entry_thanhTien.config(state="readonly")
        except ValueError:
            messagebox.showerror("lỗi!", "thành tiền lỗi")

    def sua_phieu_nhap(self):
        # Nếu có frame cũ, ẩn nó đi
        if self.frame_thong_tin:
            self.frame_thong_tin.pack_forget()
            
        # Tạo các label và entry cho việc sửa thông tin phiếu nhập
        self.label_sua_maNV = tk.Label(self.frame_sua, text="Sửa Mã Nhân Viên:")
        self.label_sua_maNV.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_sua_maNV = tk.Entry(self.frame_sua)
        self.entry_sua_maNV.grid(row=0, column=1, padx=10, pady=5)

        self.label_sua_ngayTao = tk.Label(self.frame_sua, text="Sửa Ngày Tạo:")
        self.label_sua_ngayTao.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_sua_ngayTao = tk.Entry(self.frame_sua)
        self.entry_sua_ngayTao.grid(row=1, column=1, padx=10, pady=5)

        self.label_sua_ctpn = tk.Label(self.frame_sua, text="Sửa Chi Tiết Phiếu Nhập:")
        self.label_sua_ctpn.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.btn_sua_ctpn = tk.Button(self.frame_sua, text="Sửa Chi Tiết", command=self.sua_ctpn, bg="#FFCAd4")
        self.btn_sua_ctpn.grid(row=2, column=1, padx=10, pady=5)

    def sua_ctpn(self):
        pass

    def xoa_chi_tiet(self):
        # Logic xóa chi tiết phiếu nhập
        pass
    
    def tim_chi_tiet(self):
        self.reset_frame()
        # Tạo frame nhập dữ liệu tìm kiếm
        frame_tim_kiem = ttk.Frame(self.frame_thong_tin)
        frame_tim_kiem.pack(fill="x", pady=10)

        ttk.Label(frame_tim_kiem, text="Nhập Mã Phiếu Nhập:").pack(side="left", padx=5)

        self.entry_ma_pn = ttk.Entry(frame_tim_kiem, width=20)
        self.entry_ma_pn.pack(side="left", padx=5)

        btn_tim = ttk.Button(frame_tim_kiem, text="Tìm", command=self.tim)
        btn_tim.pack(side="left", padx=5)

    def tim(self):
        ma_pn = self.entry_ma_pn.get().strip()
        if not ma_pn:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập!")
            return

        # Xóa kết quả cũ nếu có
        for widget in self.frame_thong_tin.winfo_children():
            if isinstance(widget, ttk.Treeview) or isinstance(widget, ttk.Label):
                widget.destroy()  
                
        # Lấy thông tin phiếu nhập
        phieu_nhap = self.ds_phieu_nhap.tim_kiem_phieu_nhap(ma_pn)
       

        if not phieu_nhap:
            messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập!")
            return

        ttk.Label(self.frame_thong_tin, text="Thông tin phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # Tạo Treeview hiển thị thông tin phiếu nhập
        columns = ("maPN", "maNV", "ngayTao", "tongTien")
        tree_phieu_nhap = ttk.Treeview(self.frame_thong_tin, columns=columns, show="headings")
        tree_phieu_nhap.heading("maPN", text="Mã Phiếu Nhập")
        tree_phieu_nhap.heading("maNV", text="Mã Nhân Viên")
        tree_phieu_nhap.heading("ngayTao", text="Ngày Tạo")
        tree_phieu_nhap.heading("tongTien", text="Tổng Tiền")

        for col in columns:
            tree_phieu_nhap.column(col, width=120)

        tree_phieu_nhap.pack(fill="both", expand=True)
        tree_phieu_nhap.insert("", "end", values=(phieu_nhap["ma_phieu_nhap"], phieu_nhap["ma_nhan_vien"], phieu_nhap["ngay_nhap"], phieu_nhap["tong_tien"]))
        ttk.Label(self.frame_thong_tin, text="Chi tiết phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 10))

        # Tạo Treeview hiển thị danh sách chi tiết phiếu nhập
        columns_ct = ("maPN", "maSP", "soLuongSP", "donGia", "thanhTien")
        tree_chi_tiet = ttk.Treeview(self.frame_thong_tin, columns=columns_ct, show="headings")

        tree_chi_tiet.heading("maPN", text="Mã Phiếu Nhập")
        tree_chi_tiet.heading("maSP", text="Mã Sản Phẩm")
        tree_chi_tiet.heading("soLuongSP", text="Số Lượng")
        tree_chi_tiet.heading("donGia", text="Đơn Giá")
        tree_chi_tiet.heading("thanhTien", text="Thành Tiền")

        for col in columns_ct:
            tree_chi_tiet.column(col, width=120)

        tree_chi_tiet.pack(fill="both", expand=True)

        danh_sach_ct = self.dsctpn.lay_du_lieu_tu_sql()
        try:
            ma_pn = int(ma_pn)
        except ValueError:
            messagebox.showerror("Lỗi", "Mã phiếu nhập không hợp lệ!")
            return
        for ct in danh_sach_ct:
            if ct[0] == ma_pn:
                tree_chi_tiet.insert("", "end", values=(ct[0], ct[1], ct[2], float(ct[3]), float(ct[4])))

        self.frame_thong_tin.update_idletasks()  
        
        
        
        
    def in_danh_sach(self):
        self.reset_frame()

        # Thêm tiêu đề "Thông tin phiếu nhập"
        ttk.Label(self.frame_thong_tin, text="Thông tin phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        columns = ("maPN", "maNV", "ngayTao", "tongTien")
        self.tree_phieu_nhap = ttk.Treeview(self.frame_thong_tin, columns=columns, show="headings")
        self.tree_phieu_nhap.heading("maPN", text="Mã Phiếu Nhập")
        self.tree_phieu_nhap.column("maPN", width=100)
        self.tree_phieu_nhap.heading("maNV", text="Mã Nhân Viên")
        self.tree_phieu_nhap.column("maNV", width=100)
        self.tree_phieu_nhap.heading("ngayTao", text="Ngày Tạo")
        self.tree_phieu_nhap.column("ngayTao", width=200)
        self.tree_phieu_nhap.heading("tongTien", text="Tổng Tiền")
        self.tree_phieu_nhap.column("tongTien", width=100)
        self.tree_phieu_nhap.pack(fill="both", expand=True)  # Hiển thị Treeview

        # Thêm sự kiện khi chọn một phiếu nhập
        self.tree_phieu_nhap.bind("<<TreeviewSelect>>", self.hien_thi_chi_tiet_phieu_nhap)

        danh_sach = self.ds_phieu_nhap.lay_du_lieu_tu_sql()
        if danh_sach:
            for phieu in danh_sach:
                self.tree_phieu_nhap.insert("", "end", values=(phieu[0], phieu[1], phieu[2], phieu[3]))
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

        # Thêm tiêu đề "Chi tiết phiếu nhập"
        ttk.Label(self.frame_thong_tin, text="Chi tiết phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 10))

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
    giao_dien = PhieuNhapGUI(root)
    root.mainloop()
