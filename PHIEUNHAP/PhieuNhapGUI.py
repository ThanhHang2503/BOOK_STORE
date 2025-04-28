import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from .CTPhieuNhapBUSS import CTPhieuNhapBUSS
from .PhieuNhapBUSS import PhieuNhapBUSS


class PhieuNhapGUI:

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_remove()

        self.phieu_nhap_buss = PhieuNhapBUSS()
        self.phieu_nhap_buss.lay_du_lieu_tu_sql()
        self.ctphieu_nhap_buss = CTPhieuNhapBUSS()
        self.ctphieu_nhap_buss.lay_du_lieu_tu_sql()

        self.frame_title = tk.Frame(self.frame)
        self.frame_title.grid(row=0, column=0, pady=10)

        self.frame_thong_tin = tk.Frame(self.frame)
        self.frame_thong_tin.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.hien_thi_them()

    def xoa_thong_tin_frame(self):
        for widget in self.frame_thong_tin.winfo_children():
            widget.destroy()

    def hien_thi_them(self):
        self.xoa_thong_tin_frame()

        self.label_maPN = tk.Label(self.frame_thong_tin, text="Mã Phiếu Nhập")
        self.label_maPN.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_maPN = tk.Entry(self.frame_thong_tin)
        self.entry_maPN.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.label_ngayNhap = tk.Label(self.frame_thong_tin, text="Ngày Nhập")
        self.label_ngayNhap.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_ngayNhap = tk.Entry(self.frame_thong_tin)
        self.entry_ngayNhap.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.label_nhaCungCap = tk.Label(self.frame_thong_tin, text="Nhà Cung Cấp")
        self.label_nhaCungCap.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.entry_nhaCungCap = tk.Entry(self.frame_thong_tin)
        self.entry_nhaCungCap.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.label_tongTien = tk.Label(self.frame_thong_tin, text="Tổng Tiền")
        self.label_tongTien.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.entry_tongTien = tk.Entry(self.frame_thong_tin)
        self.entry_tongTien.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.btn_them_phieu_nhap = tk.Button(self.frame_thong_tin, text="Thêm Phiếu Nhập", command=self.them_phieu_nhap)
        self.btn_them_phieu_nhap.grid(row=4, column=0, padx=10, pady=10, sticky="w")


    def them_phieu_nhap(self):
        maPN = self.entry_maPN.get()
        ngayNhap = self.entry_ngayNhap.get()
        nhaCungCap = self.entry_nhaCungCap.get()
        tongTien = self.entry_tongTien.get()

        if not maPN or not ngayNhap or not nhaCungCap or not tongTien:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        self.phieu_nhap_buss.them(maPN, ngayNhap, nhaCungCap, tongTien)
        messagebox.showinfo("Thông báo", "Thêm phiếu nhập thành công!")
        self.hien_thi_danh_sach()


    def hien_thi_sua(self):
        self.xoa_thong_tin_frame()
        tk.Label(self.frame_thong_tin, text="Nhập Mã Phiếu Nhập").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_maPN = ttk.Entry(self.frame_thong_tin, width=20)
        self.entry_maPN.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        btn_tim = ttk.Button(self.frame_thong_tin, text="Sửa phiếu nhập", command=self.sua_phieu_nhap)
        btn_tim.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    def sua_phieu_nhap(self):
        ma_pn = self.entry_maPN.get().strip()
        if not ma_pn:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập!")
            return

        phieu_nhap = self.phieu_nhap_buss.tim_kiem(ma_pn)
        if not phieu_nhap:
            messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập!")
            return

        self.xoa_thong_tin_frame()
        ttk.Label(self.frame_thong_tin, text="Sửa Thông Tin Phiếu Nhập", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        maPN, ngayTao, maNV, tongTien = phieu_nhap

        tk.Label(self.frame_thong_tin, text="Mã Phiếu Nhập:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_maPN = ttk.Entry(self.frame_thong_tin, width=25)
        self.entry_maPN.insert(0, maPN)  # Mã phiếu nhập
        self.entry_maPN.config(state="disabled")
        self.entry_maPN.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.frame_thong_tin, text="Ngày Tạo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_ngayTao = ttk.Entry(self.frame_thong_tin, width=25)
        self.entry_ngayTao.insert(0, ngayTao)  # Ngày tạo
        self.entry_ngayTao.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.frame_thong_tin, text="Mã Nhân Viên:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_maNV = ttk.Entry(self.frame_thong_tin, width=25)
        self.entry_maNV.insert(0, maNV)  # Mã nhân viên
        self.entry_maNV.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.frame_thong_tin, text="Tổng Tiền:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_tongTien = ttk.Entry(self.frame_thong_tin, width=25)
        self.entry_tongTien.insert(0, f"{tongTien:,.0f}".replace(",", "."))  # Tổng tiền
        self.entry_tongTien.config(state="disabled")
        self.entry_tongTien.grid(row=4, column=1, padx=10, pady=5)

        btn_xac_nhan = ttk.Button(self.frame_thong_tin, text="Xác nhận sửa", command=self.xac_nhan_sua)
        btn_xac_nhan.grid(row=5, column=1, padx=10, pady=15, sticky="e")

        # Cột chi tiết phiếu nhập
        columns = ("maPN", "maSP", "soLuong", "donGia", "thanhTien")
        self.tree_ct = ttk.Treeview(self.frame_thong_tin, columns=columns, show="headings", height=5)
        for col in columns:
            self.tree_ct.heading(col, text=col)
            self.tree_ct.column(col, width=100)
        self.tree_ct.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        dsct = self.ctphieu_nhap_buss.tim_kiem(maPN)
        for ct in dsct:
            self.tree_ct.insert("", "end", values=(ct.maPN, ct.maSP, ct.soLuong, ct.donGia, ct.thanhTien))

        # Thêm nút "Sửa Chi Tiết Phiếu Nhập"
        btn_sua_chi_tiet = ttk.Button(self.frame_thong_tin, text="Sửa Chi Tiết Phiếu Nhập", command=self.sua_chi_tiet_phiieu_nhap)
        btn_sua_chi_tiet.grid(row=7, column=1, pady=10, sticky="e")

        # Thêm nút "Thêm Chi Tiết Phiếu Nhập"
        btn_them_chi_tiet = ttk.Button(self.frame_thong_tin, text="Thêm Chi Tiết Phiếu Nhập", command=self.them_chi_tiet_phiieu_nhap)
        btn_them_chi_tiet.grid(row=8, column=1, pady=10, sticky="e")

        # Thêm nút "Xóa Chi Tiết Phiếu Nhập"
        btn_xoa_chi_tiet = ttk.Button(self.frame_thong_tin, text="Xóa Chi Tiết Phiếu Nhập", command=self.xoa_chi_tiet_phiieu_nhap)
        btn_xoa_chi_tiet.grid(row=9, column=1, pady=10, sticky="e")


    def sua_chi_tiet_phiieu_nhap(self):
        selected = self.tree_ct.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết phiếu nhập cần sửa!")
            return
        values = self.tree_ct.item(selected[0], 'values')
        maPN, maSP, soLuong, donGia, thanhTien = values

        win = tk.Toplevel()
        win.title("Sửa chi tiết phiếu nhập")

        tk.Label(win, text=f"Mã phiếu nhập: {maPN}").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        tk.Label(win, text=f"Mã sản phẩm: {maSP}").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        tk.Label(win, text="Số lượng:").grid(row=2, column=0, padx=10, pady=5)
        entry_soLuong = ttk.Entry(win)
        entry_soLuong.insert(0, soLuong)
        entry_soLuong.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(win, text="Đơn giá:").grid(row=3, column=0, padx=10, pady=5)
        entry_donGia = ttk.Entry(win)
        entry_donGia.insert(0, donGia)
        entry_donGia.grid(row=3, column=1, padx=10, pady=5)

        btn_capnhat = ttk.Button(
            win,
            text="Cập nhật",
            command=lambda: self.cap_nhat(maPN, maSP, entry_soLuong, entry_donGia, win)
        )
        btn_capnhat.grid(row=4, column=1, pady=10, sticky="e")


    def cap_nhat(self, maPN, maSP, entry_soLuong, entry_donGia, win):
        try:
            soLuong_moi = int(entry_soLuong.get())
            donGia_moi = float(entry_donGia.get())
            thanhTien_moi = soLuong_moi * donGia_moi

            selected = self.tree_ct.selection()
            if selected:
                self.tree_ct.item(selected[0], values=(maPN, maSP, soLuong_moi, donGia_moi, thanhTien_moi))

            win.destroy()
            messagebox.showinfo("Thành công", "Cập nhật chi tiết phiếu nhập thành công.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho số lượng và đơn giá.")


    def them_chi_tiet_phiieu_nhap(self):
        maPN = self.entry_maPN.get().strip()
        if not maPN:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập!")
            return

        win = tk.Toplevel()
        win.title("Thêm Chi Tiết Phiếu Nhập")

        tk.Label(win, text="Mã sản phẩm:").grid(row=0, column=0, padx=10, pady=5)
        entry_maSP = ttk.Entry(win)
        entry_maSP.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(win, text="Số lượng:").grid(row=1, column=0, padx=10, pady=5)
        entry_soLuong = ttk.Entry(win)
        entry_soLuong.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(win, text="Đơn giá:").grid(row=2, column=0, padx=10, pady=5)
        entry_donGia = ttk.Entry(win)
        entry_donGia.grid(row=2, column=1, padx=10, pady=5)

        btn_capnhat = ttk.Button(
            win,
            text="Thêm",
            command=lambda: self.cap_nhat_them_chi_tiet(maPN, entry_maSP.get(), entry_soLuong.get(), entry_donGia.get(), win)
        )
        btn_capnhat.grid(row=3, column=1, pady=10, sticky="e")


    def cap_nhat_them_chi_tiet(self, maPN, maSP, soLuong, donGia, win):
        try:
            soLuong_moi = int(soLuong)
            donGia_moi = float(donGia)
            thanhTien_moi = soLuong_moi * donGia_moi
            self.tree_ct.insert("", "end", values=(maPN, maSP, soLuong_moi, donGia_moi, thanhTien_moi))
            win.destroy()
            messagebox.showinfo("Thành công", "Cập nhật chi tiết phiếu nhập thành công.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho số lượng và đơn giá.")


    def xoa_chi_tiet_phiieu_nhap(self):
        selected = self.tree_ct.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn chi tiết phiếu nhập cần xóa!")
            return
        values = self.tree_ct.item(selected[0], 'values')
        maPN, maSP, _, _, _ = values
        self.tree_ct.delete(selected[0])


    def xac_nhan_sua(self):
        maPN = self.entry_maPN.get().strip()
        maNV = self.entry_maNV.get().strip()
        ngayTao = self.entry_ngayTao.get().strip()
        tongTien = self.entry_tongTien.get().strip()

        if not maPN or not maNV or not ngayTao or not tongTien:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            datetime.strptime(ngayTao.strip(), "%Y-%m-%d")  # Kiểm tra định dạng ngày
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày tạo phải có định dạng YYYY-MM-DD.")
            return

        try:
            tongTien = float(tongTien.replace(".", "").replace(",", "."))
        except ValueError:
            messagebox.showerror("Lỗi", "Tổng tiền phải là một số hợp lệ.")
            return

        ket_qua_sua_phieu_nhap = self.phieu_nhap_buss.sua_phieu_nhap(maPN, ngayTao, maNV, tongTien)

        if ket_qua_sua_phieu_nhap:
            for item in self.tree_ct.get_children():
                values = self.tree_ct.item(item, 'values')
                maPN_ct, maSP, soLuong, donGia, thanhTien = values
                soLuong_moi = int(soLuong)
                donGia_moi = float(donGia)
                thanhTien_moi = soLuong_moi * donGia_moi
                ket_qua_ct = self.ctphieu_nhap_buss.sua(maPN_ct, maSP, soLuong_moi, donGia_moi, thanhTien_moi)

                if not ket_qua_ct:
                    messagebox.showerror("Lỗi", f"Cập nhật chi tiết phiếu nhập cho sản phẩm {maSP} thất bại.")
                    return

            messagebox.showinfo("Thành công", "Cập nhật phiếu nhập và chi tiết phiếu nhập vào cơ sở dữ liệu thành công.")
            self.hien_thi_sua()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật phiếu nhập.")


    def hien_thi_tim(self):
        self.xoa_thong_tin_frame()

        tk.Label(self.frame_thong_tin, text="Nhập Mã Phiếu Nhập").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_maPN = ttk.Entry(self.frame_thong_tin, width=20)
        self.entry_maPN.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        btn_tim = ttk.Button(self.frame_thong_tin, text="Tìm", command=self.tim_kiem)
        btn_tim.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    def tim_kiem(self):
        ma_pn = self.entry_maPN.get().strip()
        if not ma_pn:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã phiếu nhập!")
            return

        self.xoa_thong_tin_frame()

        # Lấy thông tin phiếu nhập từ danh sách
        phieu_nhap = self.phieu_nhap_buss.tim_kiem(ma_pn)

        if not phieu_nhap:
            messagebox.showinfo("Thông báo", "Không tìm thấy phiếu nhập!")
            return

        ttk.Label(self.frame_thong_tin, text="Thông tin phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # Treeview hiển thị phiếu nhập
        columns = ("maPN", "ngayNhap", "nhaCungCap",  "tongTien")
        tree_phieu_nhap = ttk.Treeview(self.frame_thong_tin, columns=columns, show="headings")
        for col, text in zip(columns, ["Mã Phiếu Nhập", "Ngày Nhập","Mã Nhà Cung Cấp",  "Tổng Tiền"]):
            tree_phieu_nhap.heading(col, text=text)
            tree_phieu_nhap.column(col, width=150)

        tree_phieu_nhap.pack(fill="x", padx=10)

        # Giả sử phieu_nhap = (maPN, nhaCungCap, ngayNhap, tongTien)
        maPN, nhaCungCap, ngayNhap, tongTien = phieu_nhap

        # Định dạng tổng tiền: VD: 120.000
        tongTien_str = "{:,.0f}".format(float(tongTien)).replace(",", ".")

        # Chèn dữ liệu vào treeview
        tree_phieu_nhap.insert("", "end", values=(maPN, nhaCungCap, ngayNhap, tongTien_str))

        # Treeview hiển thị chi tiết phiếu nhập
        ttk.Label(self.frame_thong_tin, text="Chi tiết phiếu nhập", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 10))

        columns_ct = ("maPN", "maSP", "soLuongSP", "donGia", "thanhTien")
        tree_ctpn = ttk.Treeview(self.frame_thong_tin, columns=columns_ct, show="headings")
        for col in columns_ct:
            tree_ctpn.heading(col, text=col)
            tree_ctpn.column(col, width=120)
        tree_ctpn.pack(fill="x", padx=10)

        for ct in self.ctphieu_nhap_buss.dsctpn:
            if str(ct.maPN) == ma_pn:
                donGia_str = "{:,.0f}".format(float(ct.donGia)).replace(",", ".")
                thanhTien_str = "{:,.0f}".format(float(ct.thanhTien)).replace(",", ".")
                tree_ctpn.insert("", "end", values=(ct.maPN, ct.maSP, ct.soLuong, donGia_str, thanhTien_str))


    def hien_thi_in_danh_sach(self):
        self.xoa_thong_tin_frame()

        self.frame_trai = tk.Frame(self.frame_thong_tin)
        self.frame_trai.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.frame_phai = tk.Frame(self.frame_thong_tin, bg="#F0F0F0")
        self.frame_phai.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        tk.Label(self.frame_trai, text=f"Danh sách phiếu nhập", font=("Arial", 14, "bold"), bg="#F0F0F0").pack(pady=10)

        self.treeview = ttk.Treeview(
            self.frame_trai,
            columns=("Mã PN", "Nhà Cung Cấp", "Ngày Nhập", "Tổng Tiền"),
            show="headings"
        )
        self.treeview.pack(fill="both", expand=True)

        self.treeview.heading("Mã PN", text="Mã Phiếu Nhập")
        self.treeview.heading("Ngày Nhập", text="Ngày Nhập")
        self.treeview.heading("Nhà Cung Cấp", text="Nhà Cung Cấp")
        self.treeview.heading("Tổng Tiền", text="Tổng Tiền")

        self.treeview.column("Mã PN", width=150)
        self.treeview.column("Ngày Nhập", width=150)
        self.treeview.column("Nhà Cung Cấp", width=200)
        self.treeview.column("Tổng Tiền", width=150)

        self.treeview.bind("<<TreeviewSelect>>", self.hien_thi_chi_tiet_phieu_nhap)

        self.hien_thi_danh_sach()


    def hien_thi_danh_sach(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for phieu in self.phieu_nhap_buss.dsphieunhap:
            self.treeview.insert("", "end", values=(phieu[0], phieu[1], phieu[2], phieu[3]))


    def hien_thi_chi_tiet_phieu_nhap(self, event):
        selected = self.treeview.focus()
        values = self.treeview.item(selected, "values")
        maPN, nhaCungCap, ngayNhap, tongTien = values
        # Xóa các widget cũ trong frame chi tiết
        for widget in self.frame_phai.winfo_children():
            widget.destroy()

        tk.Label(self.frame_phai, text=f"Chi tiết phiếu nhập", font=("Arial", 14, "bold"), bg="#F0F0F0").pack(pady=10)
        tk.Label(self.frame_phai, text=f"Mã Phiếu Nhập: {maPN}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)
        tk.Label(self.frame_phai, text=f"Ngày Nhập: {ngayNhap}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)
        tk.Label(self.frame_phai, text=f"Nhà Cung Cấp: {nhaCungCap}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)
        tk.Label(self.frame_phai, text=f"Tổng Tiền: {tongTien}", bg="#F0F0F0").pack(anchor="w", padx=20, pady=5)

        # Hiển thị danh sách chi tiết phiếu nhập
        tree_ctpn = ttk.Treeview(self.frame_phai, columns=("Mã SP", "Tên SP", "Số Lượng", "Đơn Giá", "Thành Tiền"), show="headings", height=8)
        tree_ctpn.pack(padx=20, pady=10, fill="x")

        tree_ctpn.heading("Mã SP", text="Mã Sản Phẩm")
        tree_ctpn.heading("Tên SP", text="Tên Sản Phẩm")
        tree_ctpn.heading("Số Lượng", text="Số Lượng")
        tree_ctpn.heading("Đơn Giá", text="Đơn Giá")
        tree_ctpn.heading("Thành Tiền", text="Thành Tiền")

        tree_ctpn.column("Mã SP", width=100)
        tree_ctpn.column("Tên SP", width=200)
        tree_ctpn.column("Số Lượng", width=100)
        tree_ctpn.column("Đơn Giá", width=100)
        tree_ctpn.column("Thành Tiền", width=100)
        for ct in self.ctphieu_nhap_buss.dsctpn:
            if str(ct.maPN) == str(maPN):
                tree_ctpn.insert("", "end", values=(ct.maSP, ct.soLuong, ct.donGia, ct.thanhTien))

    def anGiaoDien(self):
        """Ẩn giao diện quản lý hóa đơn"""
        self.frame.grid_forget()

    def hienThi(self, action=None):
        """Hiển thị giao diện tương ứng với action"""
        self.frame.grid(row=0, column=0, sticky="nsew")
        if action=="Tạo phiếu nhập":
            self.hien_thi_them()
        elif action=="Tìm kiếm phiếu nhập":
            self.hien_thi_tim()
        elif action=="Sửa phiếu nhập":
            self.hien_thi_sua()
        elif action=="Hiển thị danh sách":
            self.hien_thi_in_danh_sach()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = PhieuNhapGUI(root)
    root.mainloop()
