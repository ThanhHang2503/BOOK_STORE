import tkinter as tk
from tkinter import ttk

from HOADON.HoaDonGUI import HoaDonGUI
from NHANVIEN.NhanVienGUI import NhanVienGUI
from PHIEUNHAP.PhieuNhapGUI import PhieuNhapGUI
from ThongKe.ThongKeGUI import ThongKeGUI

root = tk.Tk()
root.title("***********QUẢN LÍ CỬA HÀNG*********")

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Đặt kích thước và vị trí của cửa sổ
root.geometry(f"{screen_width}x{screen_height}")

# Tạo title
f_tl = tk.Frame(root, height=80, width=screen_width, bg="#FFCAd4")
f_tl.grid(row=0, column=0, sticky="ew")
f_tl.grid_propagate(False)
f_tl.grid_columnconfigure(0, weight=1)
tl = tk.Label(f_tl, text="MENU", font=("Arial", 24, "bold"), fg="black", bg="#FFCAd4")
tl.grid(pady=20)

# Tạo menu
top_menu = tk.Frame(root, height=100, width=screen_width, background="#D3D3D3")
top_menu.grid(row=1, column=0, sticky="ew")

# Create a main frame to hold the content
main_frame = ttk.Frame(root)
main_frame.grid(row=2, column=0, sticky="nsew")
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

options = {
    "Quản Lí Nhân viên": ["Thêm nhân viên", "Sửa thông tin nhân viên", "Tìm kiếm nhân viên", "Hiển thị danh sách"],
    "Quản Lí Hóa đơn": ["Tạo hóa đơn", "Sửa hóa đơn", "Tìm kiếm hóa đơn", "Hiển thị hóa đơn"],
    "Quản Lí Khách hàng": ["Thêm khách hàng", "Sửa thông tin khách hàng", "Tìm kiếm khách hàng"],
    "Quản Lí Sách": ["Thêm sản phẩm", "Sửa thông tin sản phẩm", "Tìm kiếm sản phẩm", "Trạng Thái"],
    "Thống Kê Doanh thu": [],
    "Quản Lí Phiếu nhập": ["Tạo phiếu nhập", "Tìm kiếm phiếu nhập", "Sửa phiếu nhập", "Hiển thị danh sách"]
}

nhan_vien_gui = NhanVienGUI(main_frame)
hoa_don_gui = HoaDonGUI(main_frame)
phieu_nhap_gui = PhieuNhapGUI(main_frame)
thong_ke_gui = ThongKeGUI(main_frame)

nhan_vien_gui.anGiaoDien()
hoa_don_gui.anGiaoDien()
phieu_nhap_gui.anGiaoDien()
thong_ke_gui.anGiaoDien()

empty_frame = tk.Frame(main_frame)

def quanLy(gui_object, action=None):
    # Ẩn tất cả giao diện cũ
    for widget in main_frame.winfo_children():
        widget.grid_forget()

    # Cấu hình main_frame để căn giữa nội dung
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    if gui_object:
        if gui_object == phieu_nhap_gui and action is None:
            # Nếu chọn "Quản Lí Phiếu nhập" lần đầu chưa có action -> chỉ hiện danh sách
            gui_object.hien_thi_in_danh_sach()
            gui_object.frame.grid(row=0, column=0, sticky="nsew", padx=100, pady=100)
        else:
            gui_object.hienThi(action)
            gui_object.frame.grid(row=0, column=0, sticky="nsew", padx=100, pady=100)
    else:
        empty_frame = tk.Frame(main_frame)
        empty_frame.grid(row=0, column=0, sticky="nsew", padx=100, pady=100)

def taoMenu(parent, label, values):
    frame = tk.Frame(parent, bd=2, relief="ridge")

    if label == "Thống Kê Doanh thu":
        button = tk.Button(frame, text=label, command=lambda: quanLy(thong_ke_gui))
        button.pack(fill="both", expand=True)
    else:
       
        menubutton = ttk.Menubutton(frame, text=label, direction="below")
        menu = tk.Menu(menubutton, tearoff=0)
        menubutton.config(menu=menu)

        for item in values:
            if label == "Quản Lí Nhân viên":
                menu.add_command(label=item, command=lambda i=item: quanLy(nhan_vien_gui, i))
            elif label == "Quản Lí Hóa đơn":
                menu.add_command(label=item, command=lambda i=item: quanLy(hoa_don_gui, i))
            elif label == "Quản Lí Phiếu nhập":
                menu.add_command(label=item, command=lambda i=item: quanLy(phieu_nhap_gui, i))
            else:
                menu.add_command(label=item, command=lambda i=item: quanLy(None, i))

        menubutton.pack(fill="both", expand=True)

    return frame


i = 0
for label, values in options.items():
    top_menu.grid_columnconfigure(i, weight=1)
    menu_btn = taoMenu(top_menu, label, values)
    menu_btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
    i += 1

root.mainloop()
