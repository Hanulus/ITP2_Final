import csv
import os

from library.models.book import Book
from library.models.member import Member
from library.storage.json_storage import JsonStorage
from library.utils.decorators import log_action


class LibraryManager:
    """Central class that associates books and members, and coordinates all operations."""

    def __init__(self, storage: JsonStorage):
        self._storage = storage
        self.books: list[Book] = storage.load_books()
        self.members: list[Member] = storage.load_members()

    @log_action
    def add_book(self, book: Book) -> None:
        self.books.append(book)
        self._storage.save_books(self.books)

    @log_action
    def add_member(self, member: Member) -> None:
        self.members.append(member)
        self._storage.save_members(self.members)

    @log_action
    def borrow_book(self, member_id: str, isbn: str) -> bool:
        member = self._find_member(member_id)
        book = self._find_book(isbn)
        if not member or not book or not book.is_available:
            return False
        book.is_available = False
        member.borrowed_books.append(isbn)
        self._storage.save_books(self.books)
        self._storage.save_members(self.members)
        return True

    @log_action
    def return_book(self, member_id: str, isbn: str) -> bool:
        member = self._find_member(member_id)
        book = self._find_book(isbn)
        if not member or not book or isbn not in member.borrowed_books:
            return False
        book.is_available = True
        member.borrowed_books.remove(isbn)
        self._storage.save_books(self.books)
        self._storage.save_members(self.members)
        return True

    def search_books(self, query: str) -> list[Book]:
        """Filter books by title or author using lambda + filter."""
        q = query.lower()
        return list(filter(
            lambda b: q in b.title.lower() or q in b.author.lower(),
            self.books
        ))

    def available_books(self):
        """Generator — yields books that are currently on the shelf."""
        for book in self.books:
            if book.is_available:
                yield book

    def get_genres(self) -> set:
        """Return a set of unique genres across all books."""
        return set(map(lambda b: b.genre, self.books))

    def get_stats(self) -> tuple:
        """Return library stats as a tuple: (total, available, borrowed)."""
        total = len(self.books)
        available = sum(1 for b in self.books if b.is_available)
        return (total, available, total - available)

    def export_csv(self, filepath: str) -> None:
        """Export all books to a CSV file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        fields = ["title", "author", "year", "isbn", "genre", "is_available"]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(map(lambda b: b.to_dict(), self.books))

    def _find_book(self, isbn: str):
        return next((b for b in self.books if b.isbn == isbn), None)

    def _find_member(self, member_id: str):
        return next((m for m in self.members if m.member_id == member_id), None)
