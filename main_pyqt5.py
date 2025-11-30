#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoCashier - PyQt5 Version for Windows 7 Compatibility
"""
import sys
import os
import json
import time
import math
from pathlib import Path
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QFrame,
    QComboBox, QLineEdit, QFileDialog, QHeaderView, QSpinBox,
    QMessageBox, QDialog, QScrollArea, QStyle
)
from PyQt5.QtCore import Qt, QTimer, QMimeData, QUrl, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QDragEnterEvent, QDropEvent, QIcon

from utils import get_page_count, format_currency


# ========== THEME COLORS ==========
class Theme:
    """Dark and Light theme colors"""
    
    # Dark Theme
    DARK_BG = "#0F1115"
    DARK_CONTAINER = "#1E2126"
    DARK_DROPZONE = "#232730"
    DARK_BORDER = "#2D313A"
    DARK_BLUE_PRIMARY = "#3B82F6"
    DARK_BLUE_HOVER = "#2563EB"
    DARK_SUCCESS = "#10B981"
    DARK_TEXT_PRIMARY = "#FFFFFF"
    DARK_TEXT_SECONDARY = "#9CA3AF"
    DARK_TEXT_MUTED = "#6B7280"
    
    # Light Theme
    LIGHT_BG = "#F8F9FA"
    LIGHT_CARD = "#FFFFFF"
    LIGHT_ACCENT = "#E9ECEF"
    LIGHT_BORDER = "#DEE2E6"
    LIGHT_PRIMARY = "#667EEA"
    LIGHT_PRIMARY_HOVER = "#5568D3"
    LIGHT_TEXT = "#212529"
    LIGHT_TEXT_SECONDARY = "#6C757D"
    LIGHT_SUCCESS = "#10B981"


class StyleSheet:
    """Qt StyleSheets for Dark and Light modes"""
    
    @staticmethod
    def dark_mode():
        return f"""
        QMainWindow, QWidget {{
            background-color: {Theme.DARK_BG};
            color: {Theme.DARK_TEXT_PRIMARY};
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 12px;
        }}
        
        QFrame#container {{
            background-color: {Theme.DARK_CONTAINER};
            border: 1px solid {Theme.DARK_BORDER};
            border-radius: 12px;
        }}
        
        QFrame#dropzone {{
            background-color: {Theme.DARK_DROPZONE};
            border: 2px dashed {Theme.DARK_BLUE_PRIMARY};
            border-radius: 12px;
        }}
        
        QPushButton {{
            background-color: {Theme.DARK_BLUE_PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {Theme.DARK_BLUE_HOVER};
        }}
        
        QPushButton#secondary {{
            background-color: transparent;
            color: {Theme.DARK_TEXT_SECONDARY};
            border: 1px solid {Theme.DARK_BORDER};
        }}
        
        QPushButton#secondary:hover {{
            background-color: {Theme.DARK_DROPZONE};
        }}
        
        QComboBox {{
            background-color: {Theme.DARK_CONTAINER};
            color: {Theme.DARK_TEXT_PRIMARY};
            border: 1px solid {Theme.DARK_BORDER};
            border-radius: 8px;
            padding: 6px 12px;
        }}
        
        QComboBox:hover {{
            border-color: {Theme.DARK_BLUE_PRIMARY};
        }}
        
        QComboBox::drop-down {{
            border: none;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {Theme.DARK_CONTAINER};
            color: {Theme.DARK_TEXT_PRIMARY};
            selection-background-color: {Theme.DARK_BLUE_PRIMARY};
            border: 1px solid {Theme.DARK_BORDER};
        }}
        
        QTableWidget {{
            background-color: {Theme.DARK_CONTAINER};
            color: {Theme.DARK_TEXT_PRIMARY};
            border: 1px solid {Theme.DARK_BORDER};
            border-radius: 8px;
            gridline-color: {Theme.DARK_BORDER};
        }}
        
        QTableWidget::item {{
            padding: 8px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {Theme.DARK_BLUE_PRIMARY};
        }}
        
        QHeaderView::section {{
            background-color: {Theme.DARK_CONTAINER};
            color: {Theme.DARK_TEXT_SECONDARY};
            border: none;
            border-bottom: 1px solid {Theme.DARK_BORDER};
            padding: 8px;
            font-weight: bold;
        }}
        
        QSpinBox, QLineEdit {{
            background-color: {Theme.DARK_CONTAINER};
            color: {Theme.DARK_TEXT_PRIMARY};
            border: 1px solid {Theme.DARK_BORDER};
            border-radius: 6px;
            padding: 6px;
        }}
        
        QLabel#title {{
            color: {Theme.DARK_TEXT_PRIMARY};
            font-size: 20px;
            font-weight: bold;
        }}
        
        QLabel#total {{
            color: {Theme.DARK_SUCCESS};
            font-size: 26px;
            font-weight: bold;
        }}
        
        QLabel#subtitle {{
            color: {Theme.DARK_TEXT_SECONDARY};
            font-size: 11px;
        }}
        """
    
    @staticmethod
    def light_mode():
        return f"""
        QMainWindow, QWidget {{
            background-color: {Theme.LIGHT_BG};
            color: {Theme.LIGHT_TEXT};
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 12px;
        }}
        
        QFrame#container {{
            background-color: {Theme.LIGHT_CARD};
            border: 1px solid {Theme.LIGHT_BORDER};
            border-radius: 12px;
        }}
        
        QFrame#dropzone {{
            background-color: {Theme.LIGHT_BG};
            border: 2px dashed {Theme.LIGHT_PRIMARY};
            border-radius: 12px;
        }}
        
        QPushButton {{
            background-color: {Theme.LIGHT_PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {Theme.LIGHT_PRIMARY_HOVER};
        }}
        
        QPushButton#secondary {{
            background-color: transparent;
            color: {Theme.LIGHT_TEXT_SECONDARY};
            border: 1px solid {Theme.LIGHT_BORDER};
        }}
        
        QPushButton#secondary:hover {{
            background-color: {Theme.LIGHT_ACCENT};
        }}
        
        QComboBox {{
            background-color: {Theme.LIGHT_CARD};
            color: {Theme.LIGHT_TEXT};
            border: 1px solid {Theme.LIGHT_BORDER};
            border-radius: 8px;
            padding: 6px 12px;
        }}
        
        QComboBox:hover {{
            border-color: {Theme.LIGHT_PRIMARY};
        }}
        
        QComboBox::drop-down {{
            border: none;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {Theme.LIGHT_CARD};
            color: {Theme.LIGHT_TEXT};
            selection-background-color: {Theme.LIGHT_PRIMARY};
            border: 1px solid {Theme.LIGHT_BORDER};
        }}
        
        QTableWidget {{
            background-color: {Theme.LIGHT_CARD};
            color: {Theme.LIGHT_TEXT};
            border: 1px solid {Theme.LIGHT_BORDER};
            border-radius: 8px;
            gridline-color: {Theme.LIGHT_BORDER};
        }}
        
        QTableWidget::item {{
            padding: 8px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {Theme.LIGHT_PRIMARY};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {Theme.LIGHT_ACCENT};
            color: {Theme.LIGHT_TEXT_SECONDARY};
            border: none;
            border-bottom: 1px solid {Theme.LIGHT_BORDER};
            padding: 8px;
            font-weight: bold;
        }}
        
        QSpinBox, QLineEdit {{
            background-color: {Theme.LIGHT_CARD};
            color: {Theme.LIGHT_TEXT};
            border: 1px solid {Theme.LIGHT_BORDER};
            border-radius: 6px;
            padding: 6px;
        }}
        
        QLabel#title {{
            color: {Theme.LIGHT_TEXT};
            font-size: 20px;
            font-weight: bold;
        }}
        
        QLabel#total {{
            color: {Theme.LIGHT_SUCCESS};
            font-size: 26px;
            font-weight: bold;
        }}
        
        QLabel#subtitle {{
            color: {Theme.LIGHT_TEXT_SECONDARY};
            font-size: 11px;
        }}
        """


class MiniWidget(QWidget):
    """Mini always-on-top widget showing summary"""
    
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        
        # Window setup
        self.setWindowTitle("AutoCashier Mini")
        self.setFixedSize(220, 160)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # Position at top-right
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 240, 20)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Title bar with restore button
        title_bar = QHBoxLayout()
        title_bar.addWidget(QLabel("📊"))
        
        self.btn_restore = QPushButton("▲")
        self.btn_restore.setFixedSize(28, 28)
        self.btn_restore.clicked.connect(self.restore_main_window)
        title_bar.addStretch()
        title_bar.addWidget(self.btn_restore)
        
        layout.addLayout(title_bar)
        
        # Total price
        self.lbl_total = QLabel("0 VND")
        self.lbl_total.setObjectName("total")
        self.lbl_total.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_total)
        
        # Stats
        stats_layout = QHBoxLayout()
        self.lbl_files = QLabel("0")
        self.lbl_files.setObjectName("subtitle")
        self.lbl_files.setAlignment(Qt.AlignCenter)
        
        self.lbl_pages = QLabel("0p")
        self.lbl_pages.setObjectName("subtitle")
        self.lbl_pages.setAlignment(Qt.AlignCenter)
        
        self.lbl_sheets = QLabel("0s")
        self.lbl_sheets.setObjectName("subtitle")
        self.lbl_sheets.setAlignment(Qt.AlignCenter)
        
        stats_layout.addWidget(self.lbl_files)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.lbl_pages)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.lbl_sheets)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(500)
    
    def update_stats(self):
        """Update stats from parent"""
        stats = self.parent_app.get_stats()
        self.lbl_files.setText(str(stats['files']))
        self.lbl_pages.setText(f"{stats['pages']}p")
        self.lbl_sheets.setText(f"{stats['sheets']}s")
        self.lbl_total.setText(format_currency(stats['total']))
    
    def restore_main_window(self):
        """Restore main window and close mini widget"""
        self.parent_app.show()
        self.parent_app.activateWindow()
        self.close()
    
    def closeEvent(self, event):
        """Handle window close"""
        self.timer.stop()
        event.accept()


class AutoCashierApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Data
        self.files = []  # List of file data dicts
        self.prices = {}
        self.defaults = {}
        self.watch_folders = {}
        self.last_file_time = None
        self.customer_timeout = 60
        self.dark_mode = True
        self.mini_widget = None
        
        # Load config
        self.load_config()
        
        # Setup UI
        self.init_ui()
        
        # Apply theme
        self.apply_theme()
        
        # Watch folder timer
        self.watch_timer = QTimer()
        self.watch_timer.timeout.connect(self.check_new_files)
        
        # Initialize watch folders
        self.init_watch_folders()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AutoCashier - PyQt5")
        self.setGeometry(100, 100, 1100, 750)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # ===== HEADER =====
        header_frame = QFrame()
        header_frame.setObjectName("container")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(24, 18, 24, 18)
        
        # Title and controls
        title_label = QLabel("AutoCashier")
        title_label.setObjectName("title")
        header_layout.addWidget(title_label)
        
        # Minimize button
        self.btn_minimize = QPushButton("▼")
        self.btn_minimize.setObjectName("secondary")
        self.btn_minimize.setFixedSize(36, 36)
        self.btn_minimize.clicked.connect(self.minimize_to_widget)
        header_layout.addWidget(self.btn_minimize)
        
        # Theme toggle
        self.btn_theme = QPushButton("☀️")
        self.btn_theme.setObjectName("secondary")
        self.btn_theme.setFixedSize(40, 40)
        self.btn_theme.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.btn_theme)
        
        header_layout.addSpacing(20)
        
        # Global controls
        header_layout.addWidget(QLabel("Chế độ chung:"))
        
        self.global_size = QComboBox()
        self.global_size.addItems(["-", "A4", "A3"])
        self.global_size.setFixedWidth(75)
        self.global_size.currentTextChanged.connect(lambda v: self.apply_global(size=v))
        header_layout.addWidget(self.global_size)
        
        self.global_type = QComboBox()
        self.global_type.addItems(["-", "soft", "hard"])
        self.global_type.setFixedWidth(75)
        self.global_type.currentTextChanged.connect(lambda v: self.apply_global(p_type=v))
        header_layout.addWidget(self.global_type)
        
        self.global_color = QComboBox()
        self.global_color.addItems(["-", "bw", "color"])
        self.global_color.setFixedWidth(75)
        self.global_color.currentTextChanged.connect(lambda v: self.apply_global(color=v))
        header_layout.addWidget(self.global_color)
        
        self.global_sides = QComboBox()
        self.global_sides.addItems(["-", "1", "2"])
        self.global_sides.setFixedWidth(60)
        self.global_sides.currentTextChanged.connect(lambda v: self.apply_global(sides=v))
        header_layout.addWidget(self.global_sides)
        
        self.global_pages_per_sheet = QComboBox()
        self.global_pages_per_sheet.addItems(["-", "1", "2", "4", "6", "9"])
        self.global_pages_per_sheet.setFixedWidth(60)
        self.global_pages_per_sheet.currentTextChanged.connect(lambda v: self.apply_global(pages_per_sheet=v))
        header_layout.addWidget(self.global_pages_per_sheet)
        
        header_layout.addStretch()
        
        # Watch folder button
        self.btn_watch = QPushButton("📁 Watch Folder")
        self.btn_watch.clicked.connect(self.toggle_watch_folder)
        header_layout.addWidget(self.btn_watch)
        
        # Refresh button
        btn_refresh = QPushButton("↺ Refresh")
        btn_refresh.setObjectName("secondary")
        btn_refresh.clicked.connect(self.reset_global)
        header_layout.addWidget(btn_refresh)
        
        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)
        
        # ===== CONTENT AREA =====
        content_frame = QFrame()
        content_frame.setObjectName("container")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Tên file", "Trang", "Khổ", "Loại", "Màu", "Mặt", "Ghép", "Giá", ""
        ])
        
        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Filename stretches
        for i in range(1, 9):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Enable drag and drop
        self.table.setAcceptDrops(True)
        self.table.setDragEnabled(True)
        self.table.setDragDropMode(QTableWidget.DropOnly)
        
        content_layout.addWidget(self.table)
        
        # Drop zone (shown when no files)
        self.drop_zone = QFrame()
        self.drop_zone.setObjectName("dropzone")
        self.drop_zone.setMinimumHeight(300)
        drop_layout = QVBoxLayout()
        drop_layout.setAlignment(Qt.AlignCenter)
        
        drop_icon = QLabel("📂")
        drop_icon.setFont(QFont("Segoe UI", 48))
        drop_icon.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_icon)
        
        drop_label = QLabel("Kéo thả file vào đây")
        drop_label.setObjectName("title")
        drop_label.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_label)
        
        drop_subtitle = QLabel("hoặc bấm nút 'Thêm File' bên dưới")
        drop_subtitle.setObjectName("subtitle")
        drop_subtitle.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_subtitle)
        
        self.drop_zone.setLayout(drop_layout)
        content_layout.addWidget(self.drop_zone)
        
        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)
        
        # ===== FOOTER =====
        footer_frame = QFrame()
        footer_frame.setObjectName("container")
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(24, 18, 24, 18)
        
        # Add file button
        btn_add = QPushButton("➕  Thêm File")
        btn_add.setFixedHeight(44)
        btn_add.clicked.connect(self.add_files)
        footer_layout.addWidget(btn_add)
        
        # Clear all button
        btn_clear = QPushButton("🗑️  Xóa tất cả")
        btn_clear.setObjectName("secondary")
        btn_clear.setFixedHeight(44)
        btn_clear.clicked.connect(self.clear_all_files)
        footer_layout.addWidget(btn_clear)
        
        footer_layout.addStretch()
        
        # Total price
        price_container = QFrame()
        price_container.setObjectName("container")
        price_layout = QVBoxLayout()
        price_layout.setContentsMargins(24, 12, 24, 12)
        
        price_label = QLabel("Tổng tiền")
        price_label.setObjectName("subtitle")
        price_label.setAlignment(Qt.AlignRight)
        price_layout.addWidget(price_label)
        
        self.lbl_total = QLabel("0 VND")
        self.lbl_total.setObjectName("total")
        self.lbl_total.setAlignment(Qt.AlignRight)
        price_layout.addWidget(self.lbl_total)
        
        price_container.setLayout(price_layout)
        footer_layout.addWidget(price_container)
        
        footer_frame.setLayout(footer_layout)
        main_layout.addWidget(footer_frame)
        
        central_widget.setLayout(main_layout)
        
        # Enable drag and drop on main window
        self.setAcceptDrops(True)
    
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.prices = data.get("prices", {})
                self.defaults = data.get("defaults", {})
                self.config_watch_folders = data.get("watch_folders", [])
                self.customer_timeout = data.get("customer_timeout_seconds", 60)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.prices = {}
            self.defaults = {}
            self.config_watch_folders = []
    
    def init_watch_folders(self):
        """Initialize watch folders from config"""
        for folder in self.config_watch_folders:
            if os.path.isdir(folder):
                self.add_watch_folder(folder)
                print(f"Auto-watching folder: {folder}")
        
        if self.watch_folders:
            self.watch_timer.start(2000)
    
    def apply_theme(self):
        """Apply current theme stylesheet"""
        if self.dark_mode:
            self.setStyleSheet(StyleSheet.dark_mode())
            self.btn_theme.setText("☀️")
        else:
            self.setStyleSheet(StyleSheet.light_mode())
            self.btn_theme.setText("🌙")
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def minimize_to_widget(self):
        """Minimize to mini widget"""
        if self.mini_widget is None or not self.mini_widget.isVisible():
            self.mini_widget = MiniWidget(self)
            self.mini_widget.setStyleSheet(self.styleSheet())
            self.mini_widget.show()
        self.hide()
    
    def reset_global(self):
        """Reset global controls"""
        self.global_size.setCurrentText("-")
        self.global_type.setCurrentText("-")
        self.global_color.setCurrentText("-")
        self.global_sides.setCurrentText("-")
        self.global_pages_per_sheet.setCurrentText("-")
    
    def add_files(self):
        """Open file dialog to add files"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Chọn file để in",
            "",
            "All Files (*.pdf *.docx *.pptx *.xlsx *.xls *.jpg *.jpeg *.png *.bmp *.gif *.tiff);;PDF Files (*.pdf);;Word Files (*.docx);;PowerPoint Files (*.pptx);;Excel Files (*.xlsx *.xls);;Images (*.jpg *.jpeg *.png *.bmp *.gif *.tiff)"
        )
        if file_paths:
            self.add_files_from_paths(file_paths)
    
    def add_files_from_paths(self, file_paths):
        """Add files from list of paths"""
        for path in file_paths:
            if os.path.isfile(path):
                self.add_file(path)
        
        self.update_ui()
        self.update_total()
    
    def add_file(self, file_path):
        """Add a single file to the table"""
        # Get default values based on extension
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if ext == 'pdf':
            file_defaults = self.defaults.get('pdf', self.defaults.get('default', {}))
        elif ext == 'docx':
            file_defaults = self.defaults.get('docx', self.defaults.get('default', {}))
        elif ext in ['pptx', 'ppt']:
            file_defaults = self.defaults.get('pptx', self.defaults.get('default', {}))
        elif ext in ['xlsx', 'xls']:
            file_defaults = self.defaults.get('xlsx', self.defaults.get('default', {}))
        elif ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'tif']:
            file_defaults = self.defaults.get('image', self.defaults.get('default', {}))
        else:
            file_defaults = self.defaults.get('default', {})
        
        # Create file data
        file_data = {
            'path': file_path,
            'filename': os.path.basename(file_path),
            'pages': get_page_count(file_path),
            'size': file_defaults.get('size', 'A4'),
            'type': file_defaults.get('type', 'soft'),
            'color': file_defaults.get('color', 'bw'),
            'sides': file_defaults.get('sides', '1'),
            'pages_per_sheet': file_defaults.get('pages_per_sheet', '1')
        }
        
        self.files.append(file_data)
        self.add_table_row(file_data)
    
    def add_table_row(self, file_data):
        """Add a row to the table for a file"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Filename
        self.table.setItem(row, 0, QTableWidgetItem(file_data['filename']))
        
        # Pages (editable)
        pages_widget = QSpinBox()
        pages_widget.setRange(1, 9999)
        pages_widget.setValue(file_data['pages'])
        pages_widget.valueChanged.connect(lambda v, r=row: self.on_pages_changed(r, v))
        self.table.setCellWidget(row, 1, pages_widget)
        
        # Size dropdown
        size_combo = QComboBox()
        size_combo.addItems(["A4", "A3"])
        size_combo.setCurrentText(file_data['size'])
        size_combo.currentTextChanged.connect(lambda v, r=row: self.on_combo_changed(r, 'size', v))
        self.table.setCellWidget(row, 2, size_combo)
        
        # Type dropdown
        type_combo = QComboBox()
        type_combo.addItems(["soft", "hard"])
        type_combo.setCurrentText(file_data['type'])
        type_combo.currentTextChanged.connect(lambda v, r=row: self.on_combo_changed(r, 'type', v))
        self.table.setCellWidget(row, 3, type_combo)
        
        # Color dropdown
        color_combo = QComboBox()
        color_combo.addItems(["bw", "color"])
        color_combo.setCurrentText(file_data['color'])
        color_combo.currentTextChanged.connect(lambda v, r=row: self.on_combo_changed(r, 'color', v))
        self.table.setCellWidget(row, 4, color_combo)
        
        # Sides dropdown
        sides_combo = QComboBox()
        sides_combo.addItems(["1", "2"])
        sides_combo.setCurrentText(file_data['sides'])
        sides_combo.currentTextChanged.connect(lambda v, r=row: self.on_combo_changed(r, 'sides', v))
        self.table.setCellWidget(row, 5, sides_combo)
        
        # Pages per sheet dropdown
        pps_combo = QComboBox()
        pps_combo.addItems(["1", "2", "4", "6", "9"])
        pps_combo.setCurrentText(file_data['pages_per_sheet'])
        pps_combo.currentTextChanged.connect(lambda v, r=row: self.on_combo_changed(r, 'pages_per_sheet', v))
        self.table.setCellWidget(row, 6, pps_combo)
        
        # Price
        price = self.calculate_price(file_data)
        self.table.setItem(row, 7, QTableWidgetItem(format_currency(price)))
        
        # Remove button
        btn_remove = QPushButton("✕")
        btn_remove.setObjectName("secondary")
        btn_remove.setFixedSize(32, 32)
        btn_remove.clicked.connect(lambda checked, r=row: self.remove_file(r))
        self.table.setCellWidget(row, 8, btn_remove)
    
    def on_pages_changed(self, row, value):
        """Handle pages value change"""
        if row < len(self.files):
            self.files[row]['pages'] = value
            self.update_row_price(row)
            self.update_total()
    
    def on_combo_changed(self, row, field, value):
        """Handle combo box change"""
        if row < len(self.files):
            self.files[row][field] = value
            self.update_row_price(row)
            self.update_total()
    
    def update_row_price(self, row):
        """Update price for a specific row"""
        if row < len(self.files):
            price = self.calculate_price(self.files[row])
            self.table.item(row, 7).setText(format_currency(price))
    
    def calculate_price(self, file_data):
        """Calculate price for a file"""
        try:
            pages = file_data['pages']
            if pages == 0:
                return 0
            
            size = file_data['size']
            p_type = file_data['type']
            color = file_data['color']
            sides = int(file_data['sides'])
            pages_per_sheet = int(file_data['pages_per_sheet'])
            
            # Calculate sheets needed
            faces_to_print = math.ceil(pages / pages_per_sheet / 2)
            sheets_physical = math.ceil(faces_to_print / 2)
            
            if sides == 1:
                sheets_needed = faces_to_print
            else:
                sheets_needed = sheets_physical
            
            # Get price per sheet
            price_per_sheet = self.prices[size][p_type][color][file_data['sides']]
            
            # Calculate total
            subtotal = sheets_needed * price_per_sheet
            total = int(math.ceil(subtotal / 1000) * 1000)
            
            return total
        except Exception as e:
            print(f"Error calculating price: {e}")
            return 0
    
    def remove_file(self, row):
        """Remove a file from the table"""
        if row < len(self.files):
            self.files.pop(row)
            self.table.removeRow(row)
            self.update_ui()
            self.update_total()
            
            # Update remove button connections for rows after deleted row
            for i in range(row, self.table.rowCount()):
                btn = self.table.cellWidget(i, 8)
                if btn:
                    btn.clicked.disconnect()
                    btn.clicked.connect(lambda checked, r=i: self.remove_file(r))
    
    def clear_all_files(self):
        """Clear all files from table"""
        self.files.clear()
        self.table.setRowCount(0)
        self.update_ui()
        self.update_total()
    
    def apply_global(self, size=None, p_type=None, color=None, sides=None, pages_per_sheet=None):
        """Apply global settings to all files"""
        for i, file_data in enumerate(self.files):
            if size and size != "-":
                file_data['size'] = size
                combo = self.table.cellWidget(i, 2)
                if combo:
                    combo.setCurrentText(size)
            
            if p_type and p_type != "-":
                file_data['type'] = p_type
                combo = self.table.cellWidget(i, 3)
                if combo:
                    combo.setCurrentText(p_type)
            
            if color and color != "-":
                file_data['color'] = color
                combo = self.table.cellWidget(i, 4)
                if combo:
                    combo.setCurrentText(color)
            
            if sides and sides != "-":
                file_data['sides'] = sides
                combo = self.table.cellWidget(i, 5)
                if combo:
                    combo.setCurrentText(sides)
            
            if pages_per_sheet and pages_per_sheet != "-":
                file_data['pages_per_sheet'] = pages_per_sheet
                combo = self.table.cellWidget(i, 6)
                if combo:
                    combo.setCurrentText(pages_per_sheet)
            
            self.update_row_price(i)
        
        self.update_total()
    
    def update_total(self):
        """Update total price display"""
        total = sum(self.calculate_price(f) for f in self.files)
        total = int(math.ceil(total / 1000) * 1000)
        self.lbl_total.setText(format_currency(total))
    
    def update_ui(self):
        """Update UI based on file count"""
        if len(self.files) > 0:
            self.table.setVisible(True)
            self.drop_zone.setVisible(False)
        else:
            self.table.setVisible(False)
            self.drop_zone.setVisible(True)
    
    def get_stats(self):
        """Get statistics for mini widget"""
        total_pages = sum(f['pages'] for f in self.files)
        total_sheets = 0
        
        for f in self.files:
            pages = f['pages']
            pages_per_sheet = int(f['pages_per_sheet'])
            sides = int(f['sides'])
            
            faces = math.ceil(pages / pages_per_sheet)
            if sides == 1:
                sheets = faces
            else:
                sheets = math.ceil(faces / 2)
            total_sheets += sheets
        
        total_price = sum(self.calculate_price(f) for f in self.files)
        total_price = int(math.ceil(total_price / 1000) * 1000)
        
        return {
            'files': len(self.files),
            'pages': total_pages,
            'sheets': total_sheets,
            'total': total_price
        }
    
    def add_watch_folder(self, folder):
        """Add a folder to watch list"""
        if folder not in self.watch_folders and os.path.isdir(folder):
            self.watch_folders[folder] = set(os.listdir(folder))
            self.update_watch_button_text()
            return True
        return False
    
    def toggle_watch_folder(self):
        """Add a new folder to watch"""
        folder = QFileDialog.getExistingDirectory(self, "Chọn folder để theo dõi")
        if folder:
            if folder in self.watch_folders:
                QMessageBox.information(self, "Thông báo", f"Đang theo dõi folder này rồi!")
            else:
                if self.add_watch_folder(folder):
                    print(f"Started watching: {folder}")
                    if len(self.watch_folders) == 1:
                        self.watch_timer.start(2000)
    
    def update_watch_button_text(self):
        """Update watch button text"""
        count = len(self.watch_folders)
        if count == 0:
            self.btn_watch.setText("📁 Watch Folder")
        else:
            self.btn_watch.setText(f"👁 Watching ({count})")
    
    def check_new_files(self):
        """Check watched folders for new files"""
        if not self.watch_folders:
            return
        
        try:
            current_time = time.time()
            
            for folder, watched_files in list(self.watch_folders.items()):
                if not os.path.isdir(folder):
                    print(f"Folder no longer exists: {folder}")
                    del self.watch_folders[folder]
                    self.update_watch_button_text()
                    continue
                
                try:
                    current_files = set(os.listdir(folder))
                    new_files = current_files - watched_files
                    
                    if new_files:
                        # Check for new customer
                        if self.last_file_time and (current_time - self.last_file_time) > self.customer_timeout:
                            print(f"New customer detected (>{self.customer_timeout}s gap)")
                            self.clear_all_files()
                        
                        # Add new files
                        for filename in sorted(new_files):
                            filepath = os.path.join(folder, filename)
                            if os.path.isfile(filepath):
                                ext = os.path.splitext(filename)[1].lower()
                                if ext in ['.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
                                    print(f"New file detected: {filename}")
                                    self.add_file(filepath)
                                    watched_files.add(filename)
                                    self.last_file_time = current_time
                        
                        self.update_ui()
                        self.update_total()
                    
                    self.watch_folders[folder] = watched_files
                
                except Exception as e:
                    print(f"Error checking folder {folder}: {e}")
        
        except Exception as e:
            print(f"Error in check_new_files: {e}")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)
        
        if files:
            self.add_files_from_paths(files)
            event.acceptProposedAction()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("AutoCashier")
    app.setOrganizationName("AutoCashier")
    
    # Create and show main window
    window = AutoCashierApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
