import os
from pypdf import PdfReader
from docx import Document

def get_page_count(file_path):
    """
    Returns the number of pages in a file.
    Supports .pdf and .docx.
    Returns 1 for other file types or if counting fails (default assumption).
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.pdf':
            reader = PdfReader(file_path)
            return len(reader.pages)
        elif ext == '.docx':
            # python-docx không có thuộc tính đếm trang trực tiếp vì phụ thuộc vào rendering.
            # Trả về 1 trang mặc định, người dùng có thể sửa sau.
            return 1
        else:
            return 1
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 1

def format_currency(amount):
    return f"{amount:,.0f} VND".replace(",", ".")
