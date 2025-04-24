import time
from abc import ABC, abstractmethod

# Abstract Base Class for Library Items
class LibraryItem(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

# Represents A Book's Genre
class Genre:
    def __init__(self, name):
        self.name = name.strip().lower()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Genre({self.name!r})"

# Represents A Book's Tag
class Tag:
    def __init__(self, name):
        self.name = name.strip().lower()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Tag({self.name!r})"

# Represents a Book
class Book(LibraryItem):
    def __init__(self, title="", description="", current_chapter=1, genres=None, tags=None, reviews=None):
        self._title = title
        self._description = description
        self._current_chapter = current_chapter
        self.genres = genres if genres else []
        self.tags = tags if tags else []
        self.reviews = reviews if reviews else []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def current_chapter(self):
        return self._current_chapter

    @current_chapter.setter
    def current_chapter(self, value):
        if isinstance(value, int) and value > 0:
            self._current_chapter = value
        else:
            raise ValueError("Current chapter must be a positive integer.")

    def add_review(self, review):
        if review.strip():
            self.reviews.append(review.strip())

    def __str__(self):
        genre_list = ', '.join(str(genre) for genre in self.genres)
        tag_list = ', '.join(str(tag) for tag in self.tags)
        reviews = "\n  - " + "\n  - ".join(self.reviews) if self.reviews else "None"
        return (
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Current Chapter: {self.current_chapter}\n"
            f"Genres: {genre_list}\n"
            f"Tags: {tag_list}\n"
            f"Reviews:{reviews}\n"
        )

    def __repr__(self):
        return f"Book(title={self.title!r}, description={self.description!r}, current_chapter={self.current_chapter})"

# Manages The Collection Of Books
class Library:
    def __init__(self, filename="library.txt"):
        self.books = []
        self.filename = filename

    def add_book(self, title, description, current_chapter=1, genre_names=None, tag_names=None):
        if any(book.title == title for book in self.books):
            print(f"Book '{title}' already exists.")
            return
        genres = [Genre(name) for name in genre_names] if genre_names else []
        tags = [Tag(name) for name in tag_names] if tag_names else []
        book = Book(title, description, current_chapter, genres, tags)
        self.books.append(book)
        print(f"Book '{title}' added.")
        self.write()

    def edit_book(self, index, title=None, description=None, current_chapter=None, genre_names=None, tag_names=None):
        if 0 <= index < len(self.books):
            book = self.books[index]
            if title: book.title = title
            if description: book.description = description
            if current_chapter is not None: book.current_chapter = current_chapter
            if genre_names is not None: book.genres = [Genre(name.strip()) for name in genre_names]
            if tag_names is not None: book.tags = [Tag(name.strip()) for name in tag_names]
            print(f"Book '{book.title}' updated.")
            self.write()
        else:
            print("Invalid book index.")

    def add_review_to_book(self, index, review):
        if 0 <= index < len(self.books):
            self.books[index].add_review(review)
            print(f"Review added to '{self.books[index].title}'.")
            self.write()
        else:
            print("Invalid book index.")

    def write(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            for book in self.books:
                file.write(f"Title: {book.title}\n")
                file.write(f"Description: {book.description}\n")
                file.write(f"Current Chapter: {book.current_chapter}\n")
                file.write(f"Genres: {', '.join(g.name.capitalize() for g in book.genres)}\n")
                file.write(f"Tags: {', '.join(t.name.capitalize() for t in book.tags)}\n")
                for review in book.reviews:
                    file.write(f"Review: {review}\n")
                file.write("\n")

    def display(self):
        if not self.books:
            print("Library is empty.")
        for i, book in enumerate(self.books):
            print(f"Book {i}:\n{book}")
            time.sleep(0.5)

    def load_books(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            title, description, current_chapter = "", "", 1
            genres, tags, reviews = [], [], []

            for line in lines:
                line = line.strip()
                if line.startswith("Title:"):
                    title = line[len("Title:"):].strip()
                elif line.startswith("Description:"):
                    description = line[len("Description:"):].strip()
                elif line.startswith("Current Chapter:"):
                    current_chapter = int(line[len("Current Chapter:"):].strip())
                elif line.startswith("Genres:"):
                    genre_names = line[len("Genres:"):].split(",")
                    genres = [Genre(name.strip()) for name in genre_names if name.strip()]
                elif line.startswith("Tags:"):
                    tag_names = line[len("Tags:"):].split(",")
                    tags = [Tag(name.strip()) for name in tag_names if name.strip()]
                elif line.startswith("Review:"):
                    reviews.append(line[len("Review:"):].strip())
                elif line == "":
                    if title and description:
                        book = Book(title, description, current_chapter, genres, tags, reviews)
                        self.books.append(book)
                        title, description, current_chapter = "", "", 1
                        genres, tags, reviews = [], [], []

        except FileNotFoundError:
            print("Library file not found.")

class LibrarySearch:
    def __init__(self, library):
        self.library = library

    def search(self):
        search_type = input("Search by (1) title or (2) genre? ").strip()
        if search_type == "1":
            keyword = input("Enter title keyword: ").strip().lower()
            results = [b for b in self.library.books if keyword in b.title.lower()]
        elif search_type == "2":
            genre_input = input("Enter genre(s), comma separated: ").strip().lower()
            search_genres = [g.strip() for g in genre_input.split(",")]
            results = [b for b in self.library.books if any(g.name in search_genres for g in b.genres)]
        else:
            print("Invalid option.")
            return

        for i, book in enumerate(results):
            print(f"\nResult {i}:\n{book}")
            time.sleep(0.5)

class LibraryManager:
    def __init__(self, library):
        self.library = library

    def remove_book_by_title(self, title):
        for i, book in enumerate(self.library.books):
            if book.title.lower() == title.lower():
                confirm = input(f"Confirm delete '{book.title}' (type title): ").strip()
                if confirm == book.title:
                    self.library.books.pop(i)
                    print(f"'{book.title}' removed.")
                    self.library.write()
                else:
                    print("Confirmation failed.")
                return
        print("Book not found.")

# Main Menu Loop
def loop():
    filename = input("Library filename: ").strip()
    lib = Library(filename)
    manager = LibraryManager(lib)
    searcher = LibrarySearch(lib)

    print("Loading books...")
    lib.load_books()
    time.sleep(1)
    lib.display()

    while True:
        print("\nMenu:")
        print("1. Add Book")
        print("2. Edit Book")
        print("3. Add Review")
        print("4. Remove Book")
        print("5. Search")
        print("6. Display Books")
        print("7. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            description = input("Description: ").strip()
            try:
                chapter = int(input("Chapter: ").strip())
            except ValueError:
                chapter = 1
            genres = input("Genres (comma separated): ").split(",")
            tags = input("Tags (comma separated): ").split(",")
            lib.add_book(title, description, chapter, genres, tags)

        elif choice == "2":
            try:
                index = int(input("Book index: ").strip())
            except ValueError:
                continue
            desc = input("New description (blank = skip): ") or None
            chapter_input = input("New chapter (blank = skip): ")
            chapter = int(chapter_input) if chapter_input.isdigit() else None
            tag_input = input("New tags (blank = skip): ")
            tags = tag_input.split(",") if tag_input else None
            lib.edit_book(index, description=desc, current_chapter=chapter, tag_names=tags)

        elif choice == "3":
            try:
                index = int(input("Book number to review: ").strip())
            except ValueError:
                continue
            review = input("Enter your review from 1 - 5: ").strip()
            lib.add_review_to_book(index, review)

        elif choice == "4":
            title = input("Title to delete: ").strip()
            manager.remove_book_by_title(title)

        elif choice == "5":
            searcher.search()

        elif choice == "6":
            lib.display()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    loop()

