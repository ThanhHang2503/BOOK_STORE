import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("***********QUẢN LÍ CỬA HÀNG*********")

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Đặt kích thước và vị trí của cửa sổ
root.geometry(f"{screen_width}x{screen_height }")
# Tạo title
f_tl = tk.Frame(root, height=80, width=screen_width, bg="#FFCAd4")
f_tl.grid(row=0, column=0, sticky="ew")
f_tl.grid_propagate(False)  # Giữ nguyên kích thước frame
f_tl.grid_columnconfigure(0, weight=1)  # Cho phép mở rộng theo chiều ngang
tl = tk.Label(f_tl, text="MENU", font=("Arial", 24, "bold"), fg="black", bg="#FFCAd4")
tl.grid( pady=20)  #can giua


# Tạo menu
top_menu = tk.Frame(root, height=100, width=screen_width, background="#D3D3D3")
top_menu.grid(row=1, column=0, sticky="ew")

options = {
    "Quản Lí Nhân viên": {"Thêm nhân viên"
                          ,"Sửa thông tin nhân viên"
                          , "Tìm kiếm nhân viên",
                          "Trạng thái"},
    "Quản Lí Hóa đơn":{"Tạo hóa đơn", "Tìm kiếm hóa đơn", "Sửa hóa đơn"},
    "Quản Lí Khách hàng": {"Thêm khách hàng", "Sửa thông tin khách hàng", "Tìm kiếm khách hàng"},
    "Quản Lí Sách": {"Thêm sản phẩm", "Sửa thông tin sản phẩm", "Tìm kiếm sản phẩm", "Trạng Thái"},
    "Thống Kê Doanh thu": {"Báo cáo ngày", "Báo cáo quý", "Báo cáo năm"},
    "Quản Lí Phiếu nhập":{ "Tạo phiếu nhập", "Tìm kiếm phiếu nhập", "Sửa phiếu nhập"}
}
def create_menu(parent, label, values):
    frame = tk.Frame(parent, bd=2, relief="ridge") 
    menubutton = ttk.Menubutton(frame, text=label, direction="below")
    menu = tk.Menu(menubutton, tearoff=0)
    menubutton.config(menu=menu)
    for item in values:
        menu.add_command(label=item, command=lambda i=item: print(f"Chọn: {i}"))
    menubutton.pack(fill="both", expand=True)  
    return frame 

# Thêm các menu vào giao diện
i = 0
for label, values in options.items():
    top_menu.grid_columnconfigure(i, weight=1)
    menu_btn = create_menu(top_menu, label, values)
    menu_btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
    i += 1

    
root.mainloop()
