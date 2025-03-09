def read_html(file_path):
    """Read an HTML file and return its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
