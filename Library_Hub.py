import time

#The Guts Of A Book Using Getters And Setters
class Book:
    def __init__(self, title="", description="", current_chapter=1, genres=None, tags=None):
        self._title = title
        self._description = description
        self._current_chapter = current_chapter
        self.genres = genres if genres else []
        self.tags = tags if tags else []

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

    def __str__(self):
        genre_list = ', '.join(str(genre) for genre in self.genres)
        tag_list = ', '.join(str(tag) for tag in self.tags)
        return (
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Current Chapter: {self.current_chapter}\n"
            f"Genres: {genre_list}\n"
            f"Tags: {tag_list}\n"
        )

    def __repr__(self):
        return f"Book(title={self.title!r}, description={self.description!r}, current_chapter={self.current_chapter})"

#Reprisents A Books Genre
class Genre:
    def __init__(self, name):
        self.name = name.strip().lower()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Genre({self.name!r})"

#Reprisents A Books Tags
class Tag:
    def __init__(self, name):
        self.name = name.strip().lower()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Tag({self.name!r})"

#Manages The Collection Of Books IE Adding, Editing
class Library:
    def __init__(self, filename="library.txt"):
        self.books = []
        self.filename = filename

    def add_book(self, title, description, current_chapter=1, genre_names=None, tag_names=None):
        if any(book.title == title for book in self.books):
            print(f"Book '{title}' already exists in the library.")
            return
        genres = [Genre(name) for name in genre_names] if genre_names else []
        tags = [Tag(name) for name in tag_names] if tag_names else []
        book = Book(title, description, current_chapter, genres, tags)
        self.books.append(book)
        print(f"Book '{title}' has been added.")
        self.write()

    def edit_book(self, index, title=None, description=None, current_chapter=None, genre_names=None, tag_names=None):
        if 0 <= index < len(self.books):
            book = self.books[index]
            if title:
                book.title = title
            if description:
                book.description = description
            if current_chapter is not None:
                book.current_chapter = current_chapter
            if genre_names is not None:
                book.genres = [Genre(name.strip()) for name in genre_names]
            if tag_names is not None:
                book.tags = [Tag(name.strip()) for name in tag_names]
            print(f"Book '{book.title}' has been updated successfully.")
            self.write()
        else:
            print(f"Invalid index: {index}. No book to edit.")

    def write(self, filename=None):
        with open(filename or self.filename, "w", encoding="utf-8") as file:
            for book in self.books:
                file.write(f"Title: {book.title}\n")
                file.write(f"Description: {book.description}\n")
                file.write(f"Current Chapter: {book.current_chapter}\n")
                file.write(f"Genres: {', '.join(g.name.capitalize() for g in book.genres)}\n")
                file.write(f"Tags: {', '.join(t.name.capitalize() for t in book.tags)}\n")
                file.write("\n")

    def display(self):
        if not self.books:
            print("No books in the library.")
            return

        print("\nBooks in Library:\n")
        for i, book in enumerate(self.books, 0):
            print(f"Book {i}:\n{book}")
            time.sleep(0.75)

    def load_books(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            title, description, current_chapter, genres, tags = "", "", 1, [], []
            for line in lines:
                line = line.strip()
                if line.startswith("Title:"):
                    title = line[len("Title:"):].strip()
                elif line.startswith("Description:"):
                    description = line[len("Description:"):].strip()
                elif line.startswith("Current Chapter:"):
                    try:
                        current_chapter = int(line[len("Current Chapter:"):].strip())
                    except ValueError:
                        current_chapter = 1
                elif line.startswith("Genres:"):
                    genre_names = line[len("Genres:"):].split(",")
                    genres = [Genre(name.strip()) for name in genre_names if name.strip()]
                elif line.startswith("Tags:"):
                    tag_names = line[len("Tags:"):].split(",")
                    tags = [Tag(name.strip()) for name in tag_names if name.strip()]
                elif line == "":
                    if title and description:
                        book = Book(title, description, current_chapter, genres, tags)
                        self.books.append(book)
                        title, description, current_chapter, genres, tags = "", "", 1, [], []

            if title and description:
                book = Book(title, description, current_chapter, genres, tags)
                self.books.append(book)

        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")

#Used To Search For A Specific Book Or Genres
class LibrarySearch:
    def __init__(self, library):
        self.library = library

    def search(self):
        search_type = input("Search by (1) title or (2) genre? Enter 1 or 2: ").strip()
        if search_type == "1":
            keyword = input("Enter a book title: ").strip().lower()
            matches = [book for book in self.library.books if keyword in book.title.lower()]
        elif search_type == "2":
            genre_input = input("Enter genres (comma separated): ").strip().lower()
            genres_to_search = [genre.strip() for genre in genre_input.split(",")]
            matches = [
                book for book in self.library.books
                if any(genre.name in genres_to_search for genre in book.genres)
            ]
        else:
            print("Invalid input.")
            return

        if matches:
            print(f"\nFound {len(matches)} matching book(s):\n")
            for i, book in enumerate(matches, 1):
                print(f"Result {i}:\n{book}")
                time.sleep(0.5)
        else:
            print("No matches found.")

#Used To Deleat Books In A Library
class LibraryManager:
    def __init__(self, library):
        self.library = library

    def remove_book_by_title(self, title):
        for i, book in enumerate(self.library.books):
            if book.title.lower() == title.lower():
                confirmation = input(f"To confirm deletion please retype the title '{book.title}': ").strip()
                if confirmation == book.title:
                    removed_book = self.library.books.pop(i)
                    print(f"'{removed_book.title}' has been deleted from the library.")
                    self.library.write()
                else:
                    print("Title mismatch. Deletion canceled.")
                return
        print(f"No book found with the title '{title}'.")

#Main Interface
def loop():
    filename = input("Enter library filename: ").strip()
    lib = Library(filename)
    manager = LibraryManager(lib)
    print("\nLoading books from", filename)
    lib.load_books()
    time.sleep(1)
    lib.display()
    searcher = LibrarySearch(lib)

    while True:
        print("\nMenu:")
        print("1. Add Book")
        print("2. Edit Book")
        print("3. Remove Book")
        print("4. Search Library")
        print("5. Display Library Contents")
        print("6. Quit")

        choice = input("Choose an option: \n").strip()

        if choice == "1":
            title = input("Title: ").strip()
            description = input("Description: ").strip()
            try:
                current_chapter = int(input("Current Chapter: ").strip())
            except ValueError:
                print("Invalid chapter number. Defaulting to 1.")
                current_chapter = 1
            genres = input("Genres (comma separated): ").strip().split(",")
            tags = input("Tags (comma separated): ").strip().split(",")
            lib.add_book(title, description, current_chapter, genres, tags)
            time.sleep(2)

        elif choice == "2":
            try:
                index = int(input("Enter Book Number: ").strip())
            except ValueError:
                print("There Is No Book With That Number.")
                continue
            description = input("Change Description? (leave blank to skip): ").strip() or None
            chapter_input = input("Chapter Update (leave blank to skip): ").strip()
            current_chapter = int(chapter_input) if chapter_input.isdigit() else None
            tag_input = input("Update Tags? (comma separated, blank to skip): ").strip()
            tags = tag_input.split(",") if tag_input else None
            lib.edit_book(index, description=description, current_chapter=current_chapter, tag_names=tags)
            time.sleep(2)

        elif choice == "3":
            title = input("Enter the title of the book you want to delete: ").strip()
            if title:
                manager.remove_book_by_title(title)
            else:
                print("No title entered.")
            time.sleep(1.5)

        elif choice == "4":
            searcher.search()

        elif choice == "5":
            lib.display()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    loop()
