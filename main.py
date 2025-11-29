import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import json
import os
from utils import get_page_count, format_currency

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Dark Mode High-Contrast Theme Colors
GLOBAL_BG = "#0F1115"  # Deep dark charcoal/navy
CONTAINER_BG = "#1E2126"  # Slightly lighter for containers
DROPZONE_BG = "#232730"  # Dark blue/slate for drop zone
BORDER_COLOR = "#2D313A"  # Subtle borders
BLUE_PRIMARY = "#3B82F6"  # Vivid blue for primary actions
BLUE_HOVER = "#2563EB"  # Darker blue for hover
SUCCESS_GREEN = "#10B981"  # Bright green for total price
TEXT_PRIMARY = "#FFFFFF"  # White for headings
TEXT_SECONDARY = "#9CA3AF"  # Light gray for secondary text
TEXT_MUTED = "#6B7280"  # Muted gray for labels

# Light mode colors
LIGHT_BG = "#F8F9FA"
LIGHT_CARD = "#FFFFFF"
LIGHT_ACCENT = "#E9ECEF"
LIGHT_BORDER = "#DEE2E6"
LIGHT_DROPZONE_BG = "#F8F9FA"
LIGHT_DROPZONE_BORDER = "#667EEA"
LIGHT_TEXT = "#212529"
LIGHT_TEXT_SECONDARY = "#6C757D"
PRIMARY_COLOR = "#667EEA"  # Gradient blue-purple for light mode
PRIMARY_HOVER = "#5568D3"

class FileRow(ctk.CTkFrame):
    def __init__(self, master, file_path, prices, update_callback, remove_callback):
        super().__init__(master, corner_radius=12, fg_color="transparent")
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
        self.grid_columnconfigure(5, weight=0) # Sides (1 mặt/2 mặt)
        self.grid_columnconfigure(6, weight=0) # Pages per sheet (ghép)
        self.grid_columnconfigure(7, weight=0) # Price
        self.grid_columnconfigure(8, weight=0) # Remove

        # Widgets with theme-aware styling
        self.lbl_name = ctk.CTkLabel(
            self, 
            text=self.filename, 
            anchor="w",
            font=("Inter", 12, "normal")
        )
        self.lbl_name.grid(row=0, column=0, padx=10, pady=12, sticky="ew")

        self.entry_pages = ctk.CTkEntry(
            self, 
            width=60,
            corner_radius=8,
            border_width=1,
            font=("Inter", 12)
        )
        self.entry_pages.insert(0, str(get_page_count(file_path)))
        self.entry_pages.grid(row=0, column=1, padx=5, pady=12)
        self.entry_pages.bind("<KeyRelease>", self.on_change)

        self.var_size = ctk.StringVar(value="A4")
        self.opt_size = ctk.CTkOptionMenu(
            self, 
            values=["A4", "A3"], 
            variable=self.var_size, 
            width=70, 
            command=self.on_change,
            corner_radius=8,
            font=("Inter", 11)
        )
        self.opt_size.grid(row=0, column=2, padx=5, pady=12)

        self.var_type = ctk.StringVar(value="soft")
        self.opt_type = ctk.CTkOptionMenu(
            self, 
            values=["soft", "hard"], 
            variable=self.var_type, 
            width=80, 
            command=self.on_change,
            corner_radius=8,
            font=("Inter", 11)
        )
        self.opt_type.grid(row=0, column=3, padx=5, pady=12)

        self.var_color = ctk.StringVar(value="bw")
        self.opt_color = ctk.CTkOptionMenu(
            self, 
            values=["bw", "color"], 
            variable=self.var_color, 
            width=80, 
            command=self.on_change,
            corner_radius=8,
            font=("Inter", 11)
        )
        self.opt_color.grid(row=0, column=4, padx=5, pady=12)

        # Sides: 1 mặt / 2 mặt
        self.var_sides = ctk.StringVar(value="1")
        self.opt_sides = ctk.CTkOptionMenu(
            self, 
            values=["1", "2"], 
            variable=self.var_sides, 
            width=60, 
            command=self.on_change,
            corner_radius=8,
            font=("Inter", 11)
        )
        self.opt_sides.grid(row=0, column=5, padx=5, pady=12)

        # Pages per sheet: Số trang ghép trên 1 mặt
        self.var_pages_per_sheet = ctk.StringVar(value="1")
        self.opt_pages_per_sheet = ctk.CTkOptionMenu(
            self, 
            values=["1", "2", "4", "6", "9"], 
            variable=self.var_pages_per_sheet, 
            width=60, 
            command=self.on_change,
            corner_radius=8,
            font=("Inter", 11)
        )
        self.opt_pages_per_sheet.grid(row=0, column=6, padx=5, pady=12)

        self.lbl_price = ctk.CTkLabel(
            self, 
            text="0 VND", 
            width=120, 
            anchor="e",
            font=("Inter", 13, "bold"),
            text_color=SUCCESS_GREEN
        )
        self.lbl_price.grid(row=0, column=7, padx=10, pady=12)

        self.btn_remove = ctk.CTkButton(
            self, 
            text="✕", 
            width=32,
            height=32,
            corner_radius=8,
            fg_color="transparent",
            text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY),
            border_width=1,
            font=("Inter", 14),
            command=self.remove
        )
        self.btn_remove.grid(row=0, column=8, padx=5, pady=12)

        self.calculate_price()

    def on_change(self, *args):
        self.calculate_price()
        self.update_callback()

    def calculate_price(self):
        import math
        try:
            pages = int(self.entry_pages.get())  # Số trang từ file PDF/DOCX
        except ValueError:
            pages = 0
        
        if pages == 0:
            self.lbl_price.configure(text="0 VND")
            return 0
        
        size = self.var_size.get()
        p_type = self.var_type.get()
        color = self.var_color.get()
        sides_str = self.var_sides.get()
        pages_per_sheet = int(self.var_pages_per_sheet.get())

        try:
            sides = int(sides_str)
            
            # LOGIC ĐÚNG: SỐ TRANG → SỐ TỜ GIẤY VẬT LÝ
            
            # Bước 1: Áp dụng ghép trang (pages_per_sheet)
            # Ví dụ: 32 trang, ghép 2 → cần 16 mặt để in
            faces_to_print = math.ceil(pages / pages_per_sheet/2)
            
 
            sheets_physical = math.ceil(faces_to_print / 2)
            
            # Bước 3: Áp dụng chế độ in (1 mặt hay 2 mặt)
            if sides == 1:
                # In 1 mặt: chỉ dùng 1 mặt của tờ giấy
                # → Cần gấp đôi số tờ (vì mặt sau bỏ trống)
                sheets_needed = sheets_physical*2  # Mỗi mặt cần 1 tờ
            else:  # sides == 2
                # In 2 mặt: dùng cả 2 mặt của tờ giấy
                sheets_needed = sheets_physical
            
            # Bước 4: Tính giá (GIÁ TRONG CONFIG = GIÁ/TỜ)
            price_per_sheet = self.prices[size][p_type][color][sides_str]
            
            # Bước 5: Tổng tiền = SỐ TỜ × GIÁ/TỜ
            subtotal = sheets_needed * price_per_sheet
            print(sheets_needed)
            
            # Bước 6: Làm tròn lên hàng nghìn
            total = int(math.ceil(subtotal / 1000) * 1000)
            
            print(f"DEBUG: pages={pages}, ghép={pages_per_sheet}, faces={faces_to_print}, sheets_phys={sheets_physical}, in_{sides}_mặt, tờ_cần={sheets_needed}, giá/tờ={price_per_sheet}, tổng={total}")
            
            self.lbl_price.configure(text=format_currency(total))
            return total
        except (KeyError, ValueError) as e:
            print(f"Error calculating price: {e}")
            print(f"size={size}, p_type={p_type}, color={color}, sides={sides_str}")
            self.lbl_price.configure(text="0 VND")
            return 0

    def get_total(self):
        return self.calculate_price()

    def remove(self):
        self.remove_callback(self)
        self.destroy()

    def set_mode(self, size=None, p_type=None, color=None, sides=None, pages_per_sheet=None):
        if size: self.var_size.set(size)
        if p_type: self.var_type.set(p_type)
        if color: self.var_color.set(color)
        if sides: self.var_sides.set(sides)
        if pages_per_sheet: self.var_pages_per_sheet.set(pages_per_sheet)
        self.calculate_price()
        self.update_callback()


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        self.title("AutoCashier")
        self.geometry("1100x750")
        
        # Configure background - will change based on theme
        self.configure(fg_color=(LIGHT_BG, GLOBAL_BG))

        self.load_config()
        self.files = []

        # Enable drag and drop on main window
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=24, pady=24)

        # === HEADER: Floating container at top ===
        header_frame = ctk.CTkFrame(
            main_container, 
            corner_radius=16,
            fg_color=(LIGHT_CARD, CONTAINER_BG),
            border_width=1,
            border_color=(LIGHT_BORDER, BORDER_COLOR)
        )
        header_frame.pack(fill="x", pady=(0, 20))

        # Header content with flexbox-like layout
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=24, pady=18)

        # LEFT: Logo/Title
        left_section = ctk.CTkFrame(header_content, fg_color="transparent")
        left_section.pack(side="left")

        ctk.CTkLabel(
            left_section,
            text="AutoCashier",
            font=("Inter", 20, "bold"),
            text_color=(LIGHT_TEXT, TEXT_PRIMARY)
        ).pack(side="left", padx=(0, 20))

        # Theme toggle
        self.theme_var = ctk.StringVar(value="Dark")
        self.btn_theme = ctk.CTkButton(
            left_section,
            text="☀️",
            width=40,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 16),
            fg_color="transparent",
            hover_color=(LIGHT_ACCENT, DROPZONE_BG),
            text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY),
            border_width=1,
            border_color=(LIGHT_BORDER, BORDER_COLOR),
            command=self.toggle_theme
        )
        self.btn_theme.pack(side="left")

        # CENTER: Global controls
        center_section = ctk.CTkFrame(header_content, fg_color="transparent")
        center_section.pack(side="left", padx=40)

        ctk.CTkLabel(
            center_section,
            text="Chế độ chung:",
            font=("Inter", 12, "bold"),
            text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY)
        ).pack(side="left", padx=(0, 12))

        # Dropdowns container
        dropdown_frame = ctk.CTkFrame(center_section, fg_color="transparent")
        dropdown_frame.pack(side="left")

        self.global_size = ctk.CTkOptionMenu(
            dropdown_frame,
            values=["-", "A4", "A3"],
            width=75,
            height=36,
            corner_radius=8,
            font=("Inter", 11),
            command=lambda v: self.apply_global(size=v)
        )
        self.global_size.pack(side="left", padx=4)

        self.global_type = ctk.CTkOptionMenu(
            dropdown_frame,
            values=["-", "soft", "hard"],
            width=75,
            height=36,
            corner_radius=8,
            font=("Inter", 11),
            command=lambda v: self.apply_global(p_type=v)
        )
        self.global_type.pack(side="left", padx=4)

        self.global_color = ctk.CTkOptionMenu(
            dropdown_frame,
            values=["-", "bw", "color"],
            width=75,
            height=36,
            corner_radius=8,
            font=("Inter", 11),
            command=lambda v: self.apply_global(color=v)
        )
        self.global_color.pack(side="left", padx=4)

        # Sides (1 mặt / 2 mặt)
        self.global_sides = ctk.CTkOptionMenu(
            dropdown_frame,
            values=["-", "1", "2"],
            width=60,
            height=36,
            corner_radius=8,
            font=("Inter", 11),
            command=lambda v: self.apply_global(sides=v)
        )
        self.global_sides.pack(side="left", padx=4)

        # Pages per sheet
        self.global_pages_per_sheet = ctk.CTkOptionMenu(
            dropdown_frame,
            values=["-", "1", "2", "4", "6", "9"],
            width=60,
            height=36,
            corner_radius=8,
            font=("Inter", 11),
            command=lambda v: self.apply_global(pages_per_sheet=v)
        )
        self.global_pages_per_sheet.pack(side="left", padx=4)

        # RIGHT: Refresh button
        right_section = ctk.CTkFrame(header_content, fg_color="transparent")
        right_section.pack(side="right")

        self.btn_reset_global = ctk.CTkButton(
            right_section,
            text="↺ Refresh",
            width=100,
            height=36,
            corner_radius=8,
            font=("Inter", 12, "bold"),
            fg_color="transparent",
            hover_color=(LIGHT_ACCENT, DROPZONE_BG),
            text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY),
            border_width=1,
            border_color=(LIGHT_BORDER, BORDER_COLOR),
            command=self.reset_global
        )
        self.btn_reset_global.pack()

        # === MAIN CONTENT: Large central container ===
        content_frame = ctk.CTkFrame(
            main_container,
            corner_radius=16,
            fg_color=(LIGHT_CARD, CONTAINER_BG),
            border_width=1,
            border_color=(LIGHT_BORDER, BORDER_COLOR)
        )
        content_frame.pack(fill="both", expand=True, pady=(0, 20))

        self.scroll_frame = ctk.CTkScrollableFrame(
            content_frame,
            corner_radius=12,
            fg_color="transparent",
            border_width=0
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=3, pady=3)

        # === HEADER ROW: Column labels ===
        self.header_row = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent"
        )
        # Pack header_row but it will be hidden initially
        # self.header_row.pack(fill="x", padx=12, pady=(10, 5))  # Don't pack yet
        
        # Create header labels with the same layout as FileRow
        header_container = ctk.CTkFrame(self.header_row, fg_color="transparent")
        header_container.pack(fill="x", padx=12, pady=(10, 5))
        
        # Configure grid
        header_container.grid_columnconfigure(0, weight=1)
        header_container.grid_columnconfigure(1, weight=0)
        header_container.grid_columnconfigure(2, weight=0)
        header_container.grid_columnconfigure(3, weight=0)
        header_container.grid_columnconfigure(4, weight=0)
        header_container.grid_columnconfigure(5, weight=0)
        header_container.grid_columnconfigure(6, weight=0)
        header_container.grid_columnconfigure(7, weight=0)
        header_container.grid_columnconfigure(8, weight=0)
        
        labels = [
            ("Tên file", 0, 1, "w", None),
            ("Trang", 1, 0, "center", 60),
            ("Khổ", 2, 0, "center", 70),
            ("Loại", 3, 0, "center", 80),
            ("Màu", 4, 0, "center", 80),
            ("Mặt", 5, 0, "center", 60),
            ("Ghép", 6, 0, "center", 60),
            ("Giá", 7, 0, "e", 120),
            ("", 8, 0, "center", 32)  # Remove button column
        ]
        
        for text, col, weight, anchor, width in labels:
            if weight == 1:
                # Tên file column - expanding
                lbl = ctk.CTkLabel(
                    header_container,
                    text=text,
                    font=("Inter", 11, "bold"),
                    text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY),
                    anchor=anchor
                )
                lbl.grid(row=0, column=col, padx=10, pady=5, sticky="ew")
            else:
                # Fixed width columns
                lbl = ctk.CTkLabel(
                    header_container,
                    text=text,
                    font=("Inter", 11, "bold"),
                    text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY),
                    anchor=anchor,
                    width=width
                )
                lbl.grid(row=0, column=col, padx=5, pady=5)

        # === DROP ZONE: Background with colored border ===
        self.drop_zone = ctk.CTkFrame(
            self.scroll_frame,
            corner_radius=12,
            fg_color=(LIGHT_DROPZONE_BG, DROPZONE_BG),
            border_width=2,
            border_color=(LIGHT_DROPZONE_BORDER, BLUE_PRIMARY)
        )
        self.drop_zone.pack(fill="both", expand=True, padx=20, pady=20)

        # Dropzone content - centered
        dropzone_content = ctk.CTkFrame(self.drop_zone, fg_color="transparent")
        dropzone_content.place(relx=0.5, rely=0.5, anchor="center")

        # Large folder icon (outline style)
        ctk.CTkLabel(
            dropzone_content,
            text="📂",
            font=("Segoe UI", 72)
        ).pack(pady=(0, 20))

        # Drop label - centered text
        self.drop_label = ctk.CTkLabel(
            dropzone_content,
            text="Kéo thả file vào đây",
            font=("Inter", 22, "bold"),
            text_color=(LIGHT_TEXT, TEXT_PRIMARY)
        )
        self.drop_label.pack(pady=(0, 10))

        # Subtitle
        ctk.CTkLabel(
            dropzone_content,
            text="hoặc bấm nút 'Thêm File' bên dưới",
            font=("Inter", 13),
            text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY)
        ).pack()

        # === FOOTER: Distinct container at bottom ===
        footer_frame = ctk.CTkFrame(
            main_container,
            corner_radius=16,
            fg_color=(LIGHT_CARD, CONTAINER_BG),
            border_width=1,
            border_color=(LIGHT_BORDER, BORDER_COLOR)
        )
        footer_frame.pack(fill="x")

        footer_content = ctk.CTkFrame(footer_frame, fg_color="transparent")
        footer_content.pack(fill="x", padx=24, pady=18)

        # LEFT: Action buttons
        button_container = ctk.CTkFrame(footer_content, fg_color="transparent")
        button_container.pack(side="left")

        # "Add File" button - changes color based on theme
        self.btn_add = ctk.CTkButton(
            button_container,
            text="➕  Thêm File",
            height=44,
            corner_radius=8,
            font=("Inter", 13, "bold"),
            fg_color=(PRIMARY_COLOR, BLUE_PRIMARY),
            hover_color=(PRIMARY_HOVER, BLUE_HOVER),
            text_color=("#FFFFFF", TEXT_PRIMARY),
            border_width=0,
            command=self.add_files
        )
        self.btn_add.pack(side="left", padx=(0, 12))

        # "Delete All" - Outline style
        self.btn_clear = ctk.CTkButton(
            button_container,
            text="🗑️  Xóa tất cả",
            height=44,
            corner_radius=8,
            font=("Inter", 12),
            fg_color="transparent",
            hover_color=(LIGHT_ACCENT, DROPZONE_BG),
            text_color=(LIGHT_TEXT_SECONDARY, TEXT_SECONDARY),
            border_width=1,
            border_color=(LIGHT_BORDER, BORDER_COLOR),
            command=self.clear_all_files
        )
        self.btn_clear.pack(side="left")

        # RIGHT: Price display box
        price_container = ctk.CTkFrame(
            footer_content,
            corner_radius=10,
            fg_color=(LIGHT_ACCENT, DROPZONE_BG),
            border_width=1,
            border_color=(LIGHT_BORDER, BORDER_COLOR)
        )
        price_container.pack(side="right")

        price_inner = ctk.CTkFrame(price_container, fg_color="transparent")
        price_inner.pack(padx=24, pady=12)

        # Label "Tổng tiền"
        ctk.CTkLabel(
            price_inner,
            text="Tổng tiền",
            font=("Inter", 11),
            text_color=(LIGHT_TEXT_SECONDARY, TEXT_MUTED)
        ).pack(anchor="e")

        # "0 VND" - Bright Green
        self.lbl_total = ctk.CTkLabel(
            price_inner,
            text="0 VND",
            font=("Inter", 26, "bold"),
            text_color=SUCCESS_GREEN
        )
        self.lbl_total.pack(anchor="e")

    def load_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.prices = data["prices"]
        except Exception as e:
            print(f"Error loading config: {e}")
            self.prices = {} # Should handle better, but for now empty

    def toggle_theme(self):
        if self.theme_var.get() == "Dark":
            # Switch to Light mode
            ctk.set_appearance_mode("Light")
            self.theme_var.set("Light")
            self.btn_theme.configure(text="🌙")
        else:
            # Switch to Dark mode
            ctk.set_appearance_mode("Dark")
            self.theme_var.set("Dark")
            self.btn_theme.configure(text="☀️")

    def reset_global(self):
        """Reset all global mode selectors to default"""
        self.global_size.set("-")
        self.global_type.set("-")
        self.global_color.set("-")
        self.global_sides.set("-")
        self.global_pages_per_sheet.set("-")

    def clear_all_files(self):
        """Remove all files from the list"""
        for row in self.files[:]:  # Create a copy to iterate
            if row.master:
                row.master.destroy()
        self.files.clear()
        # Hide header row
        if hasattr(self, 'header_row'):
            self.header_row.pack_forget()
        # Show drop zone again
        if hasattr(self, 'drop_zone'):
            self.drop_zone.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_total()

    def on_drop(self, event):
        # Get dropped files
        files = self.tk.splitlist(event.data)
        self.add_files_from_paths(files)

    def add_files_from_paths(self, file_paths):
        # Hide drop zone if files exist
        if file_paths and hasattr(self, 'drop_zone'):
            self.drop_zone.pack_forget()
            # Show header row
            if hasattr(self, 'header_row'):
                self.header_row.pack(fill="x", padx=0, pady=(0, 0), before=self.scroll_frame.winfo_children()[0] if self.files else None)
        
        for path in file_paths:
            # Remove curly braces from Windows paths
            path = path.strip('{}')
            if os.path.isfile(path):
                # Create card with theme-aware colors
                card = ctk.CTkFrame(
                    self.scroll_frame,
                    corner_radius=12,
                    fg_color=(LIGHT_CARD, CONTAINER_BG),
                    border_width=1,
                    border_color=(LIGHT_BORDER, BORDER_COLOR)
                )
                card.pack(fill="x", padx=12, pady=6)
                
                row = FileRow(card, path, self.prices, self.update_total, self.remove_file)
                row.pack(fill="x", padx=10, pady=10)
                self.files.append(row)
        self.update_total()

    def add_files(self):
        file_paths = filedialog.askopenfilenames(title="Chọn file để in")
        self.add_files_from_paths(file_paths)

    def remove_file(self, row_obj):
        if row_obj in self.files:
            self.files.remove(row_obj)
            # Remove the parent card frame
            row_obj.master.destroy()
        # Show drop zone if no files left
        if not self.files:
            # Hide header row
            if hasattr(self, 'header_row'):
                self.header_row.pack_forget()
            # Show drop zone
            if hasattr(self, 'drop_zone'):
                self.drop_zone.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_total()

    def apply_global(self, size=None, p_type=None, color=None, sides=None, pages_per_sheet=None):
        for row in self.files:
            # Only apply if not "-"
            s = size if size and size != "-" else None
            t = p_type if p_type and p_type != "-" else None
            c = color if color and color != "-" else None
            sd = sides if sides and sides != "-" else None
            pps = pages_per_sheet if pages_per_sheet and pages_per_sheet != "-" else None
            row.set_mode(s, t, c, sd, pps)
        self.update_total()

    def update_total(self):
        import math
        total = sum(f.get_total() for f in self.files)
        # Làm tròn lên đến hàng nghìn
        total = int(math.ceil(total / 1000) * 1000)
        self.lbl_total.configure(text=format_currency(total))

if __name__ == "__main__":
    app = App()
    app.mainloop()
