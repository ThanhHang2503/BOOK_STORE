import tkinter as tk
from tkinter import ttk
from PhieuNhapGUI import PhieuNhapGUI

def main():
    root = tk.Tk()
    root.title("Quản Lý Phiếu Nhập")
    root.geometry("1000x600")
    
    # Create the main application
    app = PhieuNhapGUI(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()