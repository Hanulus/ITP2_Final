class Member:
    """Represents a library member."""

    def __init__(self, name: str, member_id: str, email: str):
        self.name = name
        self.member_id = member_id
        self.email = email
        self.borrowed_books: list = []  # list of ISBNs currently borrowed

    def __str__(self) -> str:
        return f"Member [{self.member_id}]: {self.name} | {self.email}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "member_id": self.member_id,
            "email": self.email,
            "borrowed_books": self.borrowed_books,
        }

    @staticmethod
    def from_dict(data: dict) -> "Member":
        m = Member(data["name"], data["member_id"], data["email"])
        m.borrowed_books = data.get("borrowed_books", [])
        return m
