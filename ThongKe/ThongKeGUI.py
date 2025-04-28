import tkinter as tk
from datetime import date, datetime, time
from tkinter import messagebox, ttk

from dill.pointers import parent

from .ThongKeBUSS import ThongKeBUSS
from .ThongKeDAO import ThongKeDAO


class ThongKeGUI:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_remove()

        # Khởi tạo DAO và BUSS
        self.thongke_dao = ThongKeDAO()
        self.thongke_buss = ThongKeBUSS()
        
        # Gán DAO cho BUSS
        self.thongke_buss.dao = self.thongke_dao
        
        # Lấy dữ liệu từ SQL
        self.thongke_buss.lay_du_lieu_tu_sql()
        
        # Tạo giao diện
        self.create_widgets()
        
    def create_date_picker(self, parent):
        """Tạo widget chọn ngày tháng"""
        # Tạo frame chứa các widget chọn ngày
        date_frame = tk.Frame(parent, bg="#f0f0f0")
        
        # Lấy ngày hiện tại
        current_date = datetime.now()
        
        # Ngày
        day_var = tk.StringVar(value=str(current_date.day))
        day_spinbox = ttk.Spinbox(date_frame, from_=1, to=31, width=3, 
                                  textvariable=day_var, wrap=True)
        day_spinbox.pack(side=tk.LEFT)
        
        tk.Label(date_frame, text="/", bg="#f0f0f0").pack(side=tk.LEFT)
        
        # Tháng
        month_var = tk.StringVar(value=str(current_date.month))
        month_spinbox = ttk.Spinbox(date_frame, from_=1, to=12, width=3, 
                                    textvariable=month_var, wrap=True)
        month_spinbox.pack(side=tk.LEFT)
        
        tk.Label(date_frame, text="/", bg="#f0f0f0").pack(side=tk.LEFT)
        
        # Năm
        year_var = tk.StringVar(value=str(current_date.year))
        year_spinbox = ttk.Spinbox(date_frame, from_=2000, to=2100, width=5, 
                                   textvariable=year_var, wrap=True)
        year_spinbox.pack(side=tk.LEFT)
        
        # Trả về frame và các biến để truy cập sau này
        return date_frame, day_var, month_var, year_var
    
    def get_date_from_picker(self, day_var, month_var, year_var):
        """Lấy ngày từ các biến của date picker"""
        try:
            day = int(day_var.get())
            month = int(month_var.get())
            year = int(year_var.get())
            
            # Kiểm tra ngày hợp lệ
            if month in [4, 6, 9, 11] and day > 30:
                day = 30
            elif month == 2:
                # Kiểm tra năm nhuận
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    if day > 29:
                        day = 29
                elif day > 28:
                    day = 28
            
            return date(year, month, day)
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Ngày không hợp lệ: {str(e)}")
            return date.today()
    
    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self.parent, bg="#f0f0f0")
        #de chay giao dien trong menu
        main_frame = self.frame
        # main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tiêu đề
        title_label = tk.Label(main_frame, text="THỐNG KÊ HÓA ĐƠN", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)
        
        # Frame chứa các điều khiển
        control_frame = tk.LabelFrame(main_frame, text="Tùy chọn thống kê", font=("Arial", 10, "bold"), bg="#f0f0f0")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame cho thống kê theo ngày
        day_frame = tk.Frame(control_frame, bg="#f0f0f0")
        day_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(day_frame, text="Thống kê theo ngày:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        # Tạo date picker cho ngày
        self.day_picker_frame, self.day_day_var, self.day_month_var, self.day_year_var = self.create_date_picker(day_frame)
        self.day_picker_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Button(day_frame, text="Thống kê", command=self.thong_ke_theo_ngay, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Frame cho thống kê theo tháng
        month_frame = tk.Frame(control_frame, bg="#f0f0f0")
        month_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(month_frame, text="Thống kê theo tháng:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.month_var = tk.StringVar()
        month_cb = ttk.Combobox(month_frame, textvariable=self.month_var, width=5, values=[str(i) for i in range(1, 13)])
        month_cb.pack(side=tk.LEFT, padx=5)
        month_cb.current(datetime.now().month - 1)
        
        tk.Label(month_frame, text="Năm:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.year_month_var = tk.StringVar()
        year_month_cb = ttk.Combobox(month_frame, textvariable=self.year_month_var, width=6, values=[str(i) for i in range(2020, 2031)])
        year_month_cb.pack(side=tk.LEFT, padx=5)
        year_month_cb.current(datetime.now().year - 2020)
        
        tk.Button(month_frame, text="Thống kê", command=self.thong_ke_theo_thang, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Frame cho thống kê theo năm
        year_frame = tk.Frame(control_frame, bg="#f0f0f0")
        year_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(year_frame, text="Thống kê theo năm:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.year_var = tk.StringVar()
        year_cb = ttk.Combobox(year_frame, textvariable=self.year_var, width=6, values=[str(i) for i in range(2020, 2031)])
        year_cb.pack(side=tk.LEFT, padx=5)
        year_cb.current(datetime.now().year - 2020)
        
        tk.Button(year_frame, text="Thống kê", command=self.thong_ke_theo_nam, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Frame cho thống kê theo khoảng thời gian
        range_frame = tk.Frame(control_frame, bg="#f0f0f0")
        range_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(range_frame, text="Từ ngày:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        # Tạo date picker cho từ ngày
        self.from_picker_frame, self.from_day_var, self.from_month_var, self.from_year_var = self.create_date_picker(range_frame)
        self.from_picker_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Label(range_frame, text="Đến ngày:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        # Tạo date picker cho đến ngày
        self.to_picker_frame, self.to_day_var, self.to_month_var, self.to_year_var = self.create_date_picker(range_frame)
        self.to_picker_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Button(range_frame, text="Thống kê", command=self.thong_ke_tu_ngay_den_ngay, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Frame hiển thị kết quả
        result_frame = tk.LabelFrame(main_frame, text="Kết quả thống kê", font=("Arial", 10, "bold"), bg="#f0f0f0")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tạo Treeview để hiển thị dữ liệu
        columns = ("Mã HD", "Ngày tạo", "Mã NV", "Tổng tiền")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=15)
        
        # Định dạng các cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí Treeview và thanh cuộn
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame hiển thị tổng doanh thu
        summary_frame = tk.Frame(main_frame, bg="#f0f0f0")
        summary_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(summary_frame, text="Tổng doanh thu:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.total_revenue_label = tk.Label(summary_frame, text="0 VNĐ", font=("Arial", 12), bg="#f0f0f0", fg="#FF0000")
        self.total_revenue_label.pack(side=tk.LEFT, padx=5)
        
        # Frame chứa các nút điều khiển
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Button(button_frame, text="Làm mới", command=self.refresh_data, bg="#2196F3", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xuất báo cáo", command=self.export_report, bg="#FF9800", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Thoát", command=self.exit_app, bg="#F44336", fg="white", width=15).pack(side=tk.RIGHT, padx=5)
        
        # Hiển thị tất cả dữ liệu khi khởi động
        self.display_all_data()
    
    def display_all_data(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lấy dữ liệu từ SQL
        self.thongke_buss.lay_du_lieu_tu_sql()
        
        # Hiển thị tất cả dữ liệu
        total_revenue = 0
        for hd in self.thongke_buss.dshoadon:
            maHD, ngayTaoHD, maNV, tongTien = hd
            
            # Định dạng ngày tháng
            if isinstance(ngayTaoHD, datetime):
                ngay_tao_str = ngayTaoHD.strftime("%d/%m/%Y")
            else:
                ngay_tao_str = ngayTaoHD.strftime("%d/%m/%Y") if hasattr(ngayTaoHD, 'strftime') else str(ngayTaoHD)
            
            # Định dạng tiền tệ
            tong_tien_str = f"{tongTien:,.0f}"
            
            self.tree.insert("", tk.END, values=(maHD, ngay_tao_str, maNV, tong_tien_str))
            total_revenue += tongTien
        
        # Cập nhật tổng doanh thu
        self.total_revenue_label.config(text=f"{total_revenue:,.0f} VNĐ")
    
    def thong_ke_theo_ngay(self):
        try:
            selected_date = self.get_date_from_picker(self.day_day_var, self.day_month_var, self.day_year_var)
            ket_qua, doanh_thu = self.thongke_buss.ThongKeTheoNgay(selected_date)
            self.display_results(ket_qua, doanh_thu)
            messagebox.showinfo("Thông báo", f"Đã thống kê theo ngày {selected_date.strftime('%d/%m/%Y')}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thống kê theo ngày: {str(e)}")
    
    def thong_ke_theo_thang(self):
        try:
            month = int(self.month_var.get())
            year = int(self.year_month_var.get())
            ket_qua, doanh_thu = self.thongke_buss.ThongKeTheoThang(month, year)
            self.display_results(ket_qua, doanh_thu)
            messagebox.showinfo("Thông báo", f"Đã thống kê theo tháng {month}/{year}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thống kê theo tháng: {str(e)}")
    
    def thong_ke_theo_nam(self):
        try:
            year = int(self.year_var.get())
            ket_qua, doanh_thu = self.thongke_buss.ThongKeTheoNam(year)
            self.display_results(ket_qua, doanh_thu)
            messagebox.showinfo("Thông báo", f"Đã thống kê theo năm {year}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thống kê theo năm: {str(e)}")
    
    def thong_ke_tu_ngay_den_ngay(self):
        try:
            from_date = self.get_date_from_picker(self.from_day_var, self.from_month_var, self.from_year_var)
            to_date = self.get_date_from_picker(self.to_day_var, self.to_month_var, self.to_year_var)
            
            # Chuyển đổi sang datetime để có thể so sánh chính xác
            from_datetime = datetime.combine(from_date, time.min)
            to_datetime = datetime.combine(to_date, time.max)
            
            if from_date > to_date:
                messagebox.showerror("Lỗi", "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc!")
                return
            
            ket_qua, doanh_thu = self.thongke_buss.ThongKeTuNgayDenNgay(from_datetime, to_datetime)
            self.display_results(ket_qua, doanh_thu)
            messagebox.showinfo("Thông báo", f"Đã thống kê từ ngày {from_date.strftime('%d/%m/%Y')} đến ngày {to_date.strftime('%d/%m/%Y')}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thống kê theo khoảng thời gian: {str(e)}")
    
    def display_results(self, ket_qua, doanh_thu):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Hiển thị kết quả
        for hd in ket_qua:
            maHD, ngayTaoHD, maNV, tongTien = hd
            
            # Định dạng ngày tháng
            if isinstance(ngayTaoHD, datetime):
                ngay_tao_str = ngayTaoHD.strftime("%d/%m/%Y")
            else:
                ngay_tao_str = ngayTaoHD.strftime("%d/%m/%Y") if hasattr(ngayTaoHD, 'strftime') else str(ngayTaoHD)
            
            # Định dạng tiền tệ
            tong_tien_str = f"{tongTien:,.0f}"
            
            self.tree.insert("", tk.END, values=(maHD, ngay_tao_str, maNV, tong_tien_str))
        
        # Cập nhật tổng doanh thu
        self.total_revenue_label.config(text=f"{doanh_thu:,.0f} VNĐ")
    
    def refresh_data(self):
        # Làm mới dữ liệu từ cơ sở dữ liệu
        self.thongke_buss.lay_du_lieu_tu_sql()
        self.display_all_data()
        messagebox.showinfo("Thông báo", "Đã làm mới dữ liệu!")
    
    def export_report(self):
        # Chức năng xuất báo cáo (có thể mở rộng sau)
        messagebox.showinfo("Thông báo", "Chức năng xuất báo cáo sẽ được phát triển sau!")
    
    def exit_app(self):
        # Đóng kết nối cơ sở dữ liệu trước khi thoát
        self.thongke_dao.close()
        self.root.destroy()
        
    def anGiaoDien(self):
        """Ẩn giao diện quản lý hóa đơn"""
        self.frame.grid_forget()

    def hienThi(self):
        self.frame.grid()


# Hàm chạy ứng dụng
if __name__=="__main__":
    root = tk.Tk()
    root.title("Thống kê doanh thu")
    app = ThongKeGUI(root)
    root.mainloop()