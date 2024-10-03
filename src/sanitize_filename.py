import re

def sanitize_filename(filename: str) -> str:
    """Sanitize filename"""
    illegal_chars = r'[<>:"/\\|?*]'
    return re.sub(illegal_chars, "_", filename)
