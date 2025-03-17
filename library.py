import json

FILENAME = "library.json"

def load_library():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    with open(FILENAME, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library):
    title = input("Enter book title: ")
    author = input("Enter author: ")
    year = input("Enter publication year: ")
    genre = input("Enter genre: ")
    read_status = input("Have you read it? (yes/no): ").strip().lower() == "yes"
    
    library.append({
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": read_status
    })
    save_library(library)
    print("Book added successfully!")

def remove_book(library):
    title = input("Enter title of the book to remove: ")
    library = [book for book in library if book["title"].lower() != title.lower()]
    save_library(library)
    print("Book removed successfully!")
    return library

def search_book(library):
    query = input("Enter title or author to search: ").lower()
    results = [book for book in library if query in book["title"].lower() or query in book["author"].lower()]
    if results:
        display_books(results)
    else:
        print("No matching books found.")

def display_books(library):
    if not library:
        print("No books in library.")
    else:
        for book in library:
            print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Genre: {book['genre']}, Read: {'Yes' if book['read'] else 'No'}")

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books else 0
    print(f"Total books: {total_books}, Books read: {read_books} ({read_percentage:.2f}%)")

def menu():
    library = load_library()
    while True:
        print("\nPersonal Library Manager")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_book(library)
        elif choice == "2":
            library = remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    menu()
