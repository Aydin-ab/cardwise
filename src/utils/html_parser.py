def read_html(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
