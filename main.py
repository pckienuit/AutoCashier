import customtkinter as ctk
from tkinter import filedialog
import json
import os
from utils import get_page_count, format_currency

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class FileRow(ctk.CTkFrame):
    def __init__(self, master, file_path, prices, update_callback, remove_callback):
        super().__init__(master)
        self.file_path = file_path
        self.prices = prices
        self.update_callback = update_callback
        self.remove_callback = remove_callback
        self.filename = os.path.basename(file_path)
        
        # Layout
        self.grid_columnconfigure(0, weight=1) # Filename
        self.grid_columnconfigure(1, weight=0) # Pages
        self.grid_columnconfigure(2, weight=0) # Size
        self.grid_columnconfigure(3, weight=0) # Type
        self.grid_columnconfigure(4, weight=0) # Color
        self.grid_columnconfigure(5, weight=0) # Price
        self.grid_columnconfigure(6, weight=0) # Remove

        # Widgets
        self.lbl_name = ctk.CTkLabel(self, text=self.filename, anchor="w")
        self.lbl_name.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.entry_pages = ctk.CTkEntry(self, width=60)
        self.entry_pages.insert(0, str(get_page_count(file_path)))
        self.entry_pages.grid(row=0, column=1, padx=5, pady=5)
        self.entry_pages.bind("<KeyRelease>", self.on_change)

        self.var_size = ctk.StringVar(value="A4")
        self.opt_size = ctk.CTkOptionMenu(self, values=["A4", "A3"], variable=self.var_size, width=70, command=self.on_change)
        self.opt_size.grid(row=0, column=2, padx=5, pady=5)

        self.var_type = ctk.StringVar(value="soft") # soft/hard
        self.opt_type = ctk.CTkOptionMenu(self, values=["soft", "hard"], variable=self.var_type, width=80, command=self.on_change)
        self.opt_type.grid(row=0, column=3, padx=5, pady=5)

        self.var_color = ctk.StringVar(value="bw") # bw/color
        self.opt_color = ctk.CTkOptionMenu(self, values=["bw", "color"], variable=self.var_color, width=80, command=self.on_change)
        self.opt_color.grid(row=0, column=4, padx=5, pady=5)

        self.lbl_price = ctk.CTkLabel(self, text="0 VND", width=100, anchor="e")
        self.lbl_price.grid(row=0, column=5, padx=5, pady=5)

        self.btn_remove = ctk.CTkButton(self, text="X", width=30, fg_color="red", hover_color="darkred", command=self.remove)
        self.btn_remove.grid(row=0, column=6, padx=5, pady=5)

        self.calculate_price()

    def on_change(self, *args):
        self.calculate_price()
        self.update_callback()

    def calculate_price(self):
        try:
            pages = int(self.entry_pages.get())
        except ValueError:
            pages = 0
        
        size = self.var_size.get()
        p_type = self.var_type.get()
        color = self.var_color.get()

        try:
            unit_price = self.prices[size][p_type][color]
            total = pages * unit_price
            self.lbl_price.configure(text=format_currency(total))
            return total
        except KeyError:
            return 0

    def get_total(self):
        return self.calculate_price()

    def remove(self):
        self.remove_callback(self)
        self.destroy()

    def set_mode(self, size=None, p_type=None, color=None):
        if size: self.var_size.set(size)
        if p_type: self.var_type.set(p_type)
        if color: self.var_color.set(color)
        self.calculate_price()
        self.update_callback()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AutoCashier - Photocopy Calculator")
        self.geometry("900x600")

        self.load_config()
        self.files = []

        # Top Frame: Global Controls
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(self.top_frame, text="Chế độ chung:").pack(side="left", padx=10)
        
        self.global_size = ctk.CTkOptionMenu(self.top_frame, values=["-", "A4", "A3"], width=70, command=lambda v: self.apply_global(size=v))
        self.global_size.pack(side="left", padx=5)
        
        self.global_type = ctk.CTkOptionMenu(self.top_frame, values=["-", "soft", "hard"], width=80, command=lambda v: self.apply_global(p_type=v))
        self.global_type.pack(side="left", padx=5)

        self.global_color = ctk.CTkOptionMenu(self.top_frame, values=["-", "bw", "color"], width=80, command=lambda v: self.apply_global(color=v))
        self.global_color.pack(side="left", padx=5)

        # Scrollable Frame for Files
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Bottom Frame: Controls and Total
        self.bottom_frame = ctk.CTkFrame(self, height=50)
        self.bottom_frame.pack(fill="x", padx=10, pady=10)

        self.btn_add = ctk.CTkButton(self.bottom_frame, text="Thêm File", command=self.add_files)
        self.btn_add.pack(side="left", padx=10, pady=10)

        self.lbl_total = ctk.CTkLabel(self.bottom_frame, text="Tổng tiền: 0 VND", font=("Arial", 20, "bold"))
        self.lbl_total.pack(side="right", padx=20, pady=10)

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                self.prices = data["prices"]
        except Exception as e:
            print(f"Error loading config: {e}")
            self.prices = {} # Should handle better, but for now empty

    def add_files(self):
        file_paths = filedialog.askopenfilenames(title="Chọn file để in")
        for path in file_paths:
            row = FileRow(self.scroll_frame, path, self.prices, self.update_total, self.remove_file)
            row.pack(fill="x", padx=5, pady=2)
            self.files.append(row)
        self.update_total()

    def remove_file(self, row_obj):
        if row_obj in self.files:
            self.files.remove(row_obj)
        self.update_total()

    def apply_global(self, size=None, p_type=None, color=None):
        for row in self.files:
            # Only apply if not "-"
            s = size if size != "-" else None
            t = p_type if p_type != "-" else None
            c = color if color != "-" else None
            row.set_mode(s, t, c)
        self.update_total()

    def update_total(self):
        total = sum(row.get_total() for row in self.files)
        self.lbl_total.configure(text=f"Tổng tiền: {format_currency(total)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
