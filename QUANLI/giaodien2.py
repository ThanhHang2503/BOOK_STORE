import tkinter as tk
from tkinter import ttk
from NHANVIEN.NhanVien import NhanVien
from NHANVIEN.DSNhanVien import DSNhanVien

# Khởi tạo danh sách nhân viên
ds_nv = DSNhanVien()

root = tk.Tk()
root.title("***********QUẢN LÍ CỬA HÀNG*********")

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Tạo title
f_tl = tk.Frame(root, height=80, width=screen_width, bg="#FFCAd4")
f_tl.grid(row=0, column=0, sticky="ew")
f_tl.grid_propagate(False)
tl = tk.Label(f_tl, text="MENU", font=("Arial", 24, "bold"), fg="black", bg="#FFCAd4")
tl.grid(pady=20)

# Tạo menu
top_menu = tk.Frame(root, height=100, width=screen_width, background="#D3D3D3")
top_menu.grid(row=1, column=0, sticky="ew")

# Tạo khu vực hiển thị nội dung
content_frame = tk.Frame(root, background="white")
content_frame.grid(row=2, column=0, sticky="nsew")
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Hàm thêm nhân viên vào danh sách
def add_employee():
    ma_nv = entry_id.get().strip()
    ho_ten = entry_name.get().strip()
    chuc_vu = entry_role.get().strip()
    ngay_sinh = entry_dob.get().strip()
    luong = float(entry_salary.get().strip()) if entry_salary.get().strip() else 0.0
    gioi_tinh = entry_gender.get().strip()
    so_nam_kinh_nghiem = int(entry_exp.get().strip()) if entry_exp.get().strip() else 0

    if not ma_nv or not ho_ten:
        tk.messagebox.showwarning("Lỗi", "Mã nhân viên và Họ tên không được để trống!")
        return

    nv = NhanVien(ma_nv, ho_ten, chuc_vu, ngay_sinh, luong, gioi_tinh, so_nam_kinh_nghiem)
    ds_nv.them_nhan_vien(nv)

    tk.messagebox.showinfo("Thành công", f"Nhân viên {ho_ten} đã được thêm!")
    clear_fields()

# Hàm xóa dữ liệu nhập
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_role.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_salary.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_exp.delete(0, tk.END)

# Hiển thị giao diện thêm nhân viên
def show_add_employee():
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Thêm Nhân Viên", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    tk.Label(content_frame, text="Mã Nhân Viên:").pack()
    global entry_id
    entry_id = tk.Entry(content_frame)
    entry_id.pack()

    tk.Label(content_frame, text="Họ và Tên:").pack()
    global entry_name
    entry_name = tk.Entry(content_frame)
    entry_name.pack()

    tk.Label(content_frame, text="Chức vụ:").pack()
    global entry_role
    entry_role = tk.Entry(content_frame)
    entry_role.pack()

    tk.Label(content_frame, text="Ngày Sinh (dd/mm/yyyy):").pack()
    global entry_dob
    entry_dob = tk.Entry(content_frame)
    entry_dob.pack()

    tk.Label(content_frame, text="Lương:").pack()
    global entry_salary
    entry_salary = tk.Entry(content_frame)
    entry_salary.pack()

    tk.Label(content_frame, text="Giới Tính:").pack()
    global entry_gender
    entry_gender = tk.Entry(content_frame)
    entry_gender.pack()

    tk.Label(content_frame, text="Số Năm Kinh Nghiệm:").pack()
    global entry_exp
    entry_exp = tk.Entry(content_frame)
    entry_exp.pack()

    tk.Button(content_frame, text="Lưu", command=add_employee).pack(pady=10)

# Danh sách menu
options = {
    "Quản Lí Nhân viên": {"Thêm nhân viên": show_add_employee},
}

# Hàm tạo menu
def create_menu(parent, label, values):
    frame = tk.Frame(parent, bd=2, relief="ridge")
    menubutton = ttk.Menubutton(frame, text=label, direction="below")
    menu = tk.Menu(menubutton, tearoff=0)
    menubutton.config(menu=menu)
    
    for item, command in values.items():
        menu.add_command(label=item, command=command)
    
    menubutton.pack(fill="both", expand=True)
    return frame 

# Thêm menu vào giao diện
i = 0
for label, values in options.items():
    top_menu.grid_columnconfigure(i, weight=1)
    menu_btn = create_menu(top_menu, label, values)
    menu_btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
    i += 1

root.mainloop()
