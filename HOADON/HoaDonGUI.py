import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from DSHoaDon import DSHoaDon
from HoaDon import HoaDon


class HoaDonGUI:
    def __init__(self, parent):
        self.dsHoaDon = DSHoaDon()
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Khởi tạo các frame con cho từng chức năng
        self.them_frame = ttk.Frame(self.frame)
        self.sua_frame = ttk.Frame(self.frame)
        self.timKiem_frame = ttk.Frame(self.frame)
        self.hienThiDS_frame = ttk.Frame(self.frame)
        self.trangThai_frame = ttk.Frame(self.frame)

        self.taoGiaoDien()

        # Mặc định hiển thị danh sách hóa đơn
        self.hienThiDS()

        # cờ trạng thái thao tác
        self.thanhCong = False

    def hienThiDS(self):
        """Hiển thị danh sách hóa đơn trong TreeView"""
        try:
            dsHoaDon = self.dsHoaDon.danhSachHD()

            # Xóa dữ liệu cũ trong TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Thêm dữ liệu mới vào TreeView
            for hd in dsHoaDon:
                self.tree.insert("", "end", values=(hd.maHD, hd.maNV, hd.maKH, hd.tongTien, hd.ngayTaoHD))

            # Đảm bảo frame hiển thị đúng
            self.frame_danh_sach.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
            self.frame_danh_sach.tkraise()  # Đưa frame danh sách lên trên cùng

        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi hiển thị danh sách: {str(e)}", fg="red")

    def hienThi(self, action):
        """Ẩn widget trong frame trước khi hiển thị"""
        for widget in self.frame.winfo_children():
            widget.grid_forget()

        self.frame.grid(row=0, column=0, sticky="nsew")

        if action == "Hiển thị hóa đơn":
            # Chỉ hiển thị danh sách, ẩn form nhập liệu và nút
            self.frame_danh_sach.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.hienThiDS()  # Gọi lại để load dữ liệu

        else:
            # Hiển thị form nhập liệu và nút cho các chức năng khác
            self.frame_nhap.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.frame_button.grid(row=1, column=0, pady=10, sticky="nsew")

            self.lamMoiForm()  # Reset form khi chuyển giữa các chế độ

            if action == "Tạo hóa đơn":
                self.label_thong_bao.config(text="Nhập thông tin hóa đơn mới", fg="blue")
                self.entry_maHD.config(state="normal")
                self.btn_luu.config(state="normal")

            elif action == "Sửa hóa đơn":
                self.label_thong_bao.config(text="Chọn hóa đơn từ danh sách để sửa", fg="blue")
                self.entry_maNV.config(state="normal")
                self.btn_luu.config(state="disabled")
                self.hienThiDS()

                if not hasattr(self, "frame_suaHD"):
                    self.frame_suaHD = tk.Frame(self.parent)
                    self.frame_suaHD.grid(row=2, column=0, pady=10, sticky="ew")
                    # Nút Xác nhận sửa
                    self.btn_xac_nhan = tk.Button(self.frame_suaHD, text="Xác nhận sửa",
                                                  command=self.suaHoaDon, bg="green", fg="white")
                    self.btn_xac_nhan.grid(row=0, column=0, padx=5, pady=5)
                    # Nút Hủy sửa
                    self.btn_huy_sua = tk.Button(self.frame_suaHD, text="Hủy sửa",
                                                 command=self.lamMoiForm, bg="red", fg="white")
                    self.btn_huy_sua.grid(row=0, column=1, padx=5, pady=5)

                # Hiển thị frame nút sửa
                self.frame_suaHD.grid(row=2, column=0, pady=10, sticky="ew")
                # Hiển thị danh sách hóa đơn sau form nhập liệu và frame sửa
                self.frame_danh_sach.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

            elif action == "Tìm kiếm hóa đơn":
                self.label_thong_bao.config(text="Nhập thông tin hóa đơn cần tìm", fg="blue")
                self.entry_maHD.config(state="normal")
                self.btn_luu.config(state="disabled")

            else:
                self.label_thong_bao.config(text="", fg="black")

    def diChuyen(self, event):
        current_entry = event.widget  # Lấy ô nhập liệu hiện tại
        if current_entry.get().strip() == "":  # Nếu ô đang trống
            return "break"  # Không làm gì cả

        next_widget = current_entry.tk_focusNext()  # Tìm ô tiếp theo
        if isinstance(next_widget, tk.Entry):  # Nếu ô tiếp theo là Entry thì chuyển
            next_widget.focus()
        return "break"  # Ngăn hành động mặc định

    def anGiaoDien(self):
        """Ẩn giao diện quản lý hóa đơn"""
        self.frame.grid_forget()

    def taoGiaoDien(self):
        """Tạo giao diện chung cho quản lý hóa đơn"""
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)

        # Frame nhập thông tin
        self.frame_nhap = ttk.LabelFrame(self.frame, text="Thông tin hóa đơn")

        self.label_thong_bao = tk.Label(self.frame_nhap, text="", fg="red")
        self.label_thong_bao.grid(row=0, column=0, columnspan=4, pady=5)

        ttk.Label(self.frame_nhap, text="Mã hóa đơn:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_maHD = ttk.Entry(self.frame_nhap)
        self.entry_maHD.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Mã nhân viên:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_maNV = ttk.Entry(self.frame_nhap)
        self.entry_maNV.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Mã khách hàng:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_maKH = ttk.Entry(self.frame_nhap)
        self.entry_maKH.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Tổng tiền:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_tongTien = ttk.Entry(self.frame_nhap)
        self.entry_tongTien.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_nhap, text="Ngày tạo:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_ngayTao = ttk.Entry(self.frame_nhap, state="readonly")
        self.entry_ngayTao.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        # Frame chứa các nút chức năng
        self.frame_button = tk.Frame(self.frame)

        self.btn_lam_moi = tk.Button(self.frame_button, text="Quay lại", command=self.lamMoiForm, bg="#9E9E9E",
                                     fg="white")
        self.btn_lam_moi.pack(side=tk.LEFT, padx=5)

        self.btn_luu = tk.Button(self.frame_button, text="OK", command=self.luuHoaDon, bg="#4CAF50", fg="white")
        self.btn_luu.pack(side=tk.LEFT, padx=5)

        # Frame hiển thị danh sách
        self.frame_danh_sach = ttk.LabelFrame(self.frame, text="Danh sách hóa đơn")

        # Tạo Treeview để hiển thị danh sách
        self.tree = ttk.Treeview(self.frame_danh_sach, columns=("maHD", "maNV", "maKH", "tongTien", "ngayTaoHD"),
                                 show="headings", height=15)
        self.tree.heading("maHD", text="Mã hóa đơn")
        self.tree.heading("maNV", text="Mã nhân viên")
        self.tree.heading("maKH", text="Mã khách hàng")
        self.tree.heading("ngayTaoHD", text="Ngày tạo")
        self.tree.heading("tongTien", text="Tổng tiền")

        # Thiết lập độ rộng cột
        self.tree.column("maHD", width=100)
        self.tree.column("maNV", width=100)
        self.tree.column("maKH", width=100)
        self.tree.column("ngayTaoHD", width=150)
        self.tree.column("tongTien", width=150)

        # Thêm thanh cuộn
        scrollbar_y = ttk.Scrollbar(self.frame_danh_sach, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_danh_sach, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sắp xếp các thành phần
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Bắt sự kiện khi chọn một hóa đơn trong danh sách
        self.tree.bind("<<TreeviewSelect>>", self.chonHD)

        # Gán sự kiện khi nhấn Enter để di chuyển đến ô tiếp theo
        entries = [self.entry_maHD, self.entry_maNV, self.entry_maKH, self.entry_tongTien, self.entry_ngayTao]
        for entry in entries:
            entry.bind("<Return>", self.diChuyen)

    def chonHD(self, event):
        """Xử lý sự kiện khi chọn một hóa đơn trong danh sách"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")

            # Tìm hóa đơn tương ứng
            hd = self.dsHoaDon.timKiem(values[0])
            if not hd:
                print("Không tìm thấy hóa đơn với mã:", values[0])
                return

            # Hiển thị thông tin lên form
            self.entry_maHD.delete(0, tk.END)
            self.entry_maHD.insert(0, hd.maHD)
            self.entry_maNV.delete(0, tk.END)
            self.entry_maNV.insert(0, hd.maNV)
            self.entry_maKH.delete(0, tk.END)
            self.entry_maKH.insert(0, hd.maKH)
            self.entry_ngayTao.config(state="normal")
            self.entry_ngayTao.delete(0, tk.END)
            self.entry_ngayTao.insert(0, hd.ngayTaoHD)
            self.entry_ngayTao.config(state="readonly")
            self.entry_tongTien.delete(0, tk.END)
            self.entry_tongTien.insert(0, hd.tongTien)

    def luuHoaDon(self):
        """Lưu thông tin hóa đơn mới"""
        try:
            maHD = self.entry_maHD.get().strip()
            maNV = self.entry_maNV.get().strip()
            maKH = self.entry_maKH.get().strip()
            tongTien = self.entry_tongTien.get().strip()

            if not all([maHD, maNV, maKH, tongTien]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            try:
                tongTien = float(tongTien)
            except ValueError:
                self.label_thong_bao.config(text="Tổng tiền phải là số!", fg="red")
                return

            # Tạo hóa đơn mới
            hd = HoaDon(
                maHD=maHD,
                maNV=maNV,
                maKH=maKH,
                tongTien=tongTien,
                ngayTaoHD=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            if self.dsHoaDon.them(hd):
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Thêm hóa đơn thành công!", fg="green")
            else:
                self.label_thong_bao.config(text=f'Lỗi! Mã hóa đơn {maHD} đã tồn tại.', fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi: {str(e)}", fg="red")

    def suaHoaDon(self):
        """Sửa thông tin hóa đơn"""
        try:
            maHD = self.entry_maHD.get().strip()
            if not maHD:
                self.label_thong_bao.config(text="Vui lòng chọn hóa đơn cần sửa!", fg="red")
                return

            maNV = self.entry_maNV.get().strip()
            maKH = self.entry_maKH.get().strip()
            tongTien = self.entry_tongTien.get().strip()

            if not all([maNV, maKH, tongTien]):
                self.label_thong_bao.config(text="Vui lòng nhập đầy đủ thông tin!", fg="red")
                return

            try:
                tongTien = float(tongTien)
            except ValueError:
                self.label_thong_bao.config(text="Tổng tiền phải là số!", fg="red")
                return

            # Xác nhận trước khi sửa
            confirm = messagebox.askyesno("Xác nhận sửa", f"Bạn có chắc muốn sửa thông tin hóa đơn có mã {maHD}?")
            if not confirm:
                return

            # Cập nhật hóa đơn
            if self.dsHoaDon.sua(maHD, maNV, maKH, tongTien):
                self.hienThiDS()
                self.lamMoiForm()
                self.label_thong_bao.config(text="Sửa thông tin hóa đơn thành công!", fg="green")
            else:
                self.label_thong_bao.config(text=f"Không tìm thấy hóa đơn có mã {maHD}!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi sửa hóa đơn: {str(e)}", fg="red")

    def xoaHoaDon(self):
        """Xóa hóa đơn"""
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                self.label_thong_bao.config(text="Vui lòng chọn hóa đơn cần xóa!", fg="red")
                return

            item = selected_items[0]
            maHD = self.tree.item(item, "values")[0]

            # Hiển thị hộp thoại xác nhận
            confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa hóa đơn có mã {maHD}?")
            if confirm:
                if self.dsHoaDon.xoa(maHD):
                    self.hienThiDS()
                    self.lamMoiForm()
                    self.label_thong_bao.config(text="Xóa hóa đơn thành công!", fg="green")
                else:
                    self.label_thong_bao.config(text=f"Không tìm thấy hóa đơn có mã {maHD}!", fg="red")
        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi xóa hóa đơn: {str(e)}", fg="red")

    def timKiemHoaDon(self):
        """Tìm kiếm hóa đơn"""
        try:
            maHD = self.entry_maHD.get().strip()
            maKH = self.entry_maKH.get().strip()

            if not maHD and not maKH:
                self.label_thong_bao.config(text="Vui lòng nhập mã hóa đơn hoặc mã khách hàng để tìm kiếm!", fg="red")
                return

            # Xóa dữ liệu cũ trong tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Tìm kiếm theo mã hóa đơn
            if maHD:
                hd = self.dsHoaDon.timKiem(maHD)
                if hd:
                    self.tree.insert("", "end", values=(hd.maHD, hd.maNV, hd.maKH, hd.tongTien, hd.ngayTaoHD))
                    self.label_thong_bao.config(text="Đã tìm thấy hóa đơn", fg="green")
                else:
                    self.label_thong_bao.config(text="Không tìm thấy hóa đơn nào!", fg="red")

            # Tìm kiếm theo mã khách hàng
            elif maKH:
                found = False
                for hd in self.dsHoaDon.danhSachHD():
                    if hd.maKH == maKH:
                        self.tree.insert("", "end", values=(hd.maHD, hd.maNV, hd.maKH, hd.tongTien, hd.ngayTaoHD))
                        found = True

                if found:
                    self.label_thong_bao.config(text="Đã tìm thấy hóa đơn", fg="green")
                else:
                    self.label_thong_bao.config(text="Không tìm thấy hóa đơn nào!", fg="red")

        except Exception as e:
            self.label_thong_bao.config(text=f"Lỗi khi tìm kiếm: {str(e)}", fg="red")

    def lamMoiForm(self):
        """Làm mới form nhập liệu"""
        self.entry_maHD.delete(0, tk.END)
        self.entry_maNV.delete(0, tk.END)
        self.entry_maKH.delete(0, tk.END)

        self.entry_ngayTao.config(state="normal")
        self.entry_ngayTao.delete(0, tk.END)
        self.entry_ngayTao.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.entry_ngayTao.config(state="readonly")

        self.entry_tongTien.delete(0, tk.END)
        self.entry_tongTien.insert(0, "0")

        self.label_thong_bao.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý hóa đơn")
    root.geometry("800x600")
    app = HoaDonGUI(root)
    root.mainloop()
