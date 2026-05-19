import re


def is_valid_email(email: str) -> bool:
    """Check email format using regex."""
    return bool(re.match(r"^[\w.\-]+@[\w.\-]+\.\w{2,}$", email))


def is_valid_isbn(isbn: str) -> bool:
    """Accept ISBN-10 or ISBN-13 (digits only, hyphens ignored)."""
    clean = isbn.replace("-", "")
    return bool(re.match(r"^\d{10}(\d{3})?$", clean))
