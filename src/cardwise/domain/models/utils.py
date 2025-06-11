def normalize_string(s: str) -> str:
    """
    Normalize a string by removing leading and trailing whitespace and converting to lowercase.
    """
    s_ = "".join([c.lower() for c in s if c.isalnum() or c == " "])
    # remove spaces
    s_ = s_.strip().replace(" ", "_")
    return s_
