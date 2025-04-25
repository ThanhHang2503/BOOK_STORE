import tkinter as tk
import math

# Cấu hình màu sắc
BG_COLOR = "#f8f9fa"
HEADER_COLOR = "#fce4ec"
FG_COLOR = "#212121"
ENTRY_BG = "#ffffff"
BUTTON_COLOR = "#f48fb1"
ACCENT_COLOR = "#f06292"
BAR_BASE_COLOR = "#f8bbd0"
BAR_HIGHLIGHT = "#f48fb1"

RADIUS = 220
BAR_COUNT = 60
BAR_LENGTH = 15
BAR_WIDTH = 4

root = tk.Tk()
root.title("*************QUẢN LÍ CỬA HÀNG*************")
root.configure(bg=BG_COLOR)
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda event: root.destroy())

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg=BG_COLOR, highlightthickness=0)
canvas.pack(fill="both", expand=True)

center_x = screen_width // 2
center_y = screen_height // 2

header_height = 80
canvas.create_rectangle(0, 0, screen_width, header_height, fill=HEADER_COLOR, outline="")
canvas.create_text(center_x, header_height / 2, text="ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 24, "bold"), fill=FG_COLOR)

bars = []
light_index = 0

# Tạo vạch dài xung quanh form
def draw_light_bars():
    global bars
    for i in range(BAR_COUNT):
        angle_deg = i * (360 / BAR_COUNT)
        angle_rad = math.radians(angle_deg)
        x0 = center_x + (RADIUS - BAR_LENGTH) * math.cos(angle_rad)
        y0 = center_y + (RADIUS - BAR_LENGTH) * math.sin(angle_rad)
        x1 = center_x + (RADIUS + BAR_LENGTH) * math.cos(angle_rad)
        y1 = center_y + (RADIUS + BAR_LENGTH) * math.sin(angle_rad)

        line = canvas.create_line(x0, y0, x1, y1, fill="#fce4ec", width=BAR_WIDTH, capstyle="round")
        bars.append(line)


# Tạo hiệu ứng ánh sáng chạy vòng - bắt đầu nhạt và đậm dần khi di chuyển
def animate_bars():
    global light_index
    for i in range(BAR_COUNT):
        distance = min(abs(i - light_index), BAR_COUNT - abs(i - light_index))
        # hieu chinh mau sac
        if distance < 5:
            r = 240
            g = 98
            b = 146
            color = f"#{r:02x}{g:02x}{b:02x}"
        elif distance < 10:
            r = 244
            g = 143
            b = 177
            color = f"#{r:02x}{g:02x}{b:02x}"
        elif distance < 15:

            r = 248
            g = 187
            b = 208
            color = f"#{r:02x}{g:02x}{b:02x}"

        else:
            r = 252
            g = 228
            b = 236
            color = f"#{r:02x}{g:02x}{b:02x}"

        canvas.itemconfig(bars[i], fill=color)

    light_index = (light_index + 1) % BAR_COUNT
    root.after(50, animate_bars)


# Vẽ các thanh sáng
draw_light_bars()

# Tạo form trong một frame trong suốt
form_frame = tk.Frame(root, bg=BG_COLOR)
form_frame.place(x=center_x, y=center_y, anchor="center")

title = tk.Label(form_frame, text="Đăng nhập", font=("Arial", 24, "bold"), fg=FG_COLOR, bg=BG_COLOR)
title.pack(pady=(0, 20))

def tao(parent, placeholder, show=None):
    frame = tk.Frame(parent, bg=BG_COLOR)
    frame.pack(pady=10)

    entry_width = 300
    entry_height = 40

    # Create rounded border with canvas
    canvas_border = tk.Canvas(frame, width=entry_width, height=entry_height,
        bg=BG_COLOR, highlightthickness=0)
    canvas_border.pack()

    # Draw rounded rectangle for border
    radius = 10  # Corner radius
    canvas_border.bogoc(0, 0, entry_width, entry_height, radius,
        fill=ENTRY_BG, outline="#e0e0e0", width=1)

    # Create entry widget
    entry = tk.Entry(frame, font=("Arial", 12), fg=FG_COLOR, bg=ENTRY_BG,
        insertbackground=FG_COLOR, relief="flat", width=28)
    entry.place(x=10, y=10, width=entry_width - 20, height=entry_height - 20)

    if show:
        entry.config(show=show)

    # Placeholder text
    entry.insert(0, placeholder)
    entry.config(fg="#9e9e9e")

    def on_focus_in(event):
        if entry.get()==placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=FG_COLOR)
            if show:
                entry.config(show=show)

    def on_focus_out(event):
        if entry.get()=="":
            entry.insert(0, placeholder)
            entry.config(fg="#9e9e9e")
            if show:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return entry


tk.Canvas.bogoc = lambda self, x1, y1, x2, y2, radius, **kwargs: self.create_polygon(
    x1 + radius, y1,
    x2 - radius, y1,
    x2, y1,
    x2, y1 + radius,
    x2, y2 - radius,
    x2, y2,
    x2 - radius, y2,
    x1 + radius, y2,
    x1, y2,
    x1, y2 - radius,
    x1, y1 + radius,
    x1, y1,
    smooth=True, **kwargs)

email_entry = tao(form_frame, "Tên đăng nhập")
password_entry = tao(form_frame, "Mật khẩu", show="*")

forgot = tk.Label(form_frame, text="Quên mật khẩu?", fg=ACCENT_COLOR, bg=BG_COLOR, font=("Arial", 9))
forgot.pack(pady=10)


# Create login button with rounded corners
def nutbogoc(parent, text, command=None):
    button_frame = tk.Frame(parent, bg=BG_COLOR)
    button_frame.pack(pady=10)

    button_width = 300
    button_height = 40

    # Create canvas for button background
    canvas = tk.Canvas(button_frame, width=button_width, height=button_height,
        bg=BG_COLOR, highlightthickness=0)
    canvas.pack()

    # Draw rounded rectangle
    canvas.bogoc(0, 0, button_width, button_height, 20, fill=BUTTON_COLOR, outline="")

    # Add text
    canvas.create_text(button_width / 2, button_height / 2, text=text, fill="white",
        font=("Arial", 12, "bold"))

    # Add click functionality
    def on_click(event):
        if command:
            command()

    canvas.bind("<Button-1>", on_click)
    canvas.config(cursor="hand2")

    return canvas


login_btn = nutbogoc(form_frame, "Đăng nhập")

# Thêm nút thoát
exit_btn = tk.Button(root, text="X", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR,
    relief="flat", cursor="hand2", command=root.destroy, borderwidth=0)
exit_btn.place(x=screen_width - 40, y=10)

# Bắt đầu hiệu ứng
animate_bars()

root.mainloop()