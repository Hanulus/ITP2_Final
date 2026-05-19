import unittest

from library.models.book import Book
from library.models.member import Member
from library.utils.validators import is_valid_email, is_valid_isbn


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Clean Code", "Robert Martin", 2008, "9780132350884", "Programming")

    def test_book_is_available_by_default(self):
        self.assertTrue(self.book.is_available)

    def test_display_info_contains_title(self):
        self.assertIn("Clean Code", self.book.display_info())

    def test_display_info_shows_available_status(self):
        self.assertIn("available", self.book.display_info())

    def test_display_info_shows_borrowed_status(self):
        self.book.is_available = False
        self.assertIn("borrowed", self.book.display_info())

    def test_to_dict_has_all_keys(self):
        d = self.book.to_dict()
        for key in ["title", "author", "year", "isbn", "genre", "is_available"]:
            self.assertIn(key, d)

    def test_from_dict_restores_book(self):
        restored = Book.from_dict(self.book.to_dict())
        self.assertEqual(restored.title, self.book.title)
        self.assertEqual(restored.isbn, self.book.isbn)
        self.assertEqual(restored.is_available, self.book.is_available)


class TestMember(unittest.TestCase):
    def setUp(self):
        self.member = Member("Alice", "M001", "alice@example.com")

    def test_no_borrowed_books_initially(self):
        self.assertEqual(self.member.borrowed_books, [])

    def test_member_str_contains_id(self):
        self.assertIn("M001", str(self.member))

    def test_member_str_contains_name(self):
        self.assertIn("Alice", str(self.member))

    def test_to_dict_and_from_dict(self):
        restored = Member.from_dict(self.member.to_dict())
        self.assertEqual(restored.member_id, self.member.member_id)
        self.assertEqual(restored.email, self.member.email)


class TestValidators(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(is_valid_email("alice@example.com"))

    def test_invalid_email_no_at(self):
        self.assertFalse(is_valid_email("notanemail"))

    def test_invalid_email_no_domain(self):
        self.assertFalse(is_valid_email("user@"))

    def test_valid_isbn13(self):
        self.assertTrue(is_valid_isbn("9780132350884"))

    def test_valid_isbn10(self):
        self.assertTrue(is_valid_isbn("0132350882"))

    def test_invalid_isbn_too_short(self):
        self.assertFalse(is_valid_isbn("12345"))

    def test_isbn_with_hyphens(self):
        # hyphens should be stripped before validation
        self.assertTrue(is_valid_isbn("978-0132350884"))


if __name__ == "__main__":
    unittest.main()
