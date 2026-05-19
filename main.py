import random

from library.manager import LibraryManager
from library.models.book import Book
from library.models.member import Member
from library.storage.json_storage import JsonStorage
from library.utils.validators import is_valid_email, is_valid_isbn

BOOKS_FILE = "data/books.json"
MEMBERS_FILE = "data/members.json"
CSV_FILE = "data/books_export.csv"

manager = LibraryManager(JsonStorage(BOOKS_FILE, MEMBERS_FILE))


def print_menu():
    print("\n=== Library Management System ===")
    print("1.  Add book")
    print("2.  View all books")
    print("3.  Search books")
    print("4.  Add member")
    print("5.  View all members")
    print("6.  Borrow book")
    print("7.  Return book")
    print("8.  View available books")
    print("9.  Export books to CSV")
    print("10. View unique genres")
    print("11. View library stats")
    print("0.  Exit")


def add_book():
    print("\n-- Add New Book --")
    title = input("Title: ").strip()
    author = input("Author: ").strip()

    while True:
        try:
            year = int(input("Year: ").strip())
            break
        except ValueError:
            print("Invalid year. Please enter a number.")

    while True:
        isbn = input("ISBN (10 or 13 digits): ").strip()
        if is_valid_isbn(isbn):
            break
        print("Invalid ISBN format. Use 10 or 13 digits.")

    genre = input("Genre: ").strip()
    manager.add_book(Book(title, author, year, isbn, genre))
    print(f"Book '{title}' added.")


def view_books():
    if not manager.books:
        print("\nNo books in the library yet.")
        return
    print("\n-- All Books --")
    for i, book in enumerate(manager.books, 1):
        print(f"{i}. {book.display_info()}")


def search_books():
    query = input("\nSearch by title or author: ").strip()
    results = manager.search_books(query)
    if not results:
        print("No matching books found.")
        return
    for book in results:
        print(f"  {book.display_info()}")


def add_member():
    print("\n-- Add New Member --")
    name = input("Name: ").strip()
    suggested_id = f"M{random.randint(1000, 9999)}"
    member_id = input(f"Member ID (suggested: {suggested_id}): ").strip() or suggested_id

    while True:
        email = input("Email: ").strip()
        if is_valid_email(email):
            break
        print("Invalid email format. Try again.")

    manager.add_member(Member(name, member_id, email))
    print(f"Member '{name}' added.")


def view_members():
    if not manager.members:
        print("\nNo members registered yet.")
        return
    print("\n-- All Members --")
    for i, member in enumerate(manager.members, 1):
        print(f"{i}. {member}")


def borrow_book():
    print("\n-- Borrow Book --")
    member_id = input("Member ID: ").strip()
    isbn = input("Book ISBN: ").strip()
    if manager.borrow_book(member_id, isbn):
        print("Book borrowed successfully.")
    else:
        print("Failed: book not available, or member/book not found.")


def return_book():
    print("\n-- Return Book --")
    member_id = input("Member ID: ").strip()
    isbn = input("Book ISBN: ").strip()
    if manager.return_book(member_id, isbn):
        print("Book returned successfully.")
    else:
        print("Failed: this book is not in the member's borrowed list.")


def view_available():
    print("\n-- Available Books --")
    count = 0
    for book in manager.available_books():  # uses generator
        print(f"  {book.display_info()}")
        count += 1
    if count == 0:
        print("No books are currently available.")


def export_csv():
    manager.export_csv(CSV_FILE)
    print(f"Books exported to {CSV_FILE}")


def view_genres():
    genres = manager.get_genres()
    if not genres:
        print("\nNo genres found.")
        return
    print("\n-- Unique Genres --")
    for genre in sorted(genres):
        print(f"  {genre}")


def view_stats():
    total, available, borrowed = manager.get_stats()  # unpack tuple
    print("\n-- Library Stats --")
    print(f"  Total books:     {total}")
    print(f"  Available:       {available}")
    print(f"  Borrowed:        {borrowed}")
    print(f"  Total members:   {len(manager.members)}")


def main():
    actions = {
        "1": add_book,
        "2": view_books,
        "3": search_books,
        "4": add_member,
        "5": view_members,
        "6": borrow_book,
        "7": return_book,
        "8": view_available,
        "9": export_csv,
        "10": view_genres,
        "11": view_stats,
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
