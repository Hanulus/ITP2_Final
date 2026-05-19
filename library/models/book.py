from library.models.item import Item


class Book(Item):
    """Physical book in the library."""

    def __init__(self, title: str, author: str, year: int, isbn: str, genre: str):
        super().__init__(title, author, year)
        self.isbn = isbn
        self.genre = genre
        self.is_available = True  # True means the book is on the shelf

    def display_info(self) -> str:
        status = "available" if self.is_available else "borrowed"
        return f"[{status}] {self.title} by {self.author} ({self.year}) | ISBN: {self.isbn} | Genre: {self.genre}"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "genre": self.genre,
            "is_available": self.is_available,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        book = Book(
            data["title"],
            data["author"],
            data["year"],
            data["isbn"],
            data["genre"],
        )
        book.is_available = data.get("is_available", True)
        return book
