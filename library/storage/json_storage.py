import json
import os

from library.models.book import Book
from library.models.member import Member


class JsonStorage:
    """Handles saving and loading data from JSON files."""

    def __init__(self, books_file: str, members_file: str):
        self.books_file = books_file
        self.members_file = members_file
        os.makedirs(os.path.dirname(books_file), exist_ok=True)

    def save_books(self, books: list[Book]) -> None:
        with open(self.books_file, "w") as f:
            json.dump([b.to_dict() for b in books], f, indent=2)

    def load_books(self) -> list[Book]:
        if not os.path.exists(self.books_file):
            return []
        with open(self.books_file, "r") as f:
            return [Book.from_dict(d) for d in json.load(f)]

    def save_members(self, members: list[Member]) -> None:
        with open(self.members_file, "w") as f:
            json.dump([m.to_dict() for m in members], f, indent=2)

    def load_members(self) -> list[Member]:
        if not os.path.exists(self.members_file):
            return []
        with open(self.members_file, "r") as f:
            return [Member.from_dict(d) for d in json.load(f)]
