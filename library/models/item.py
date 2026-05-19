class Item:
    """Base class for all library items."""

    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

    def display_info(self) -> str:
        return f"{self.title} by {self.author} ({self.year})"

    def __str__(self) -> str:
        return self.display_info()
