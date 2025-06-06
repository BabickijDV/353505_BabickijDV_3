from typing import List, Dict, Any

class BookCatalog:
    """Base class for library book catalog operations"""
    def __init__(self):
        self.books = []  # List of dictionaries with 'title' and 'author' keys

    def add_book(self, title: str, author: str) -> None:
        """Add a book to the catalog"""
        self.books.append({
            'title': title,
            'author': author
        })

    def search_by_author(self, author: str) -> List[Dict[str, str]]:
        """Search books by author name"""
        return [book for book in self.books 
                if author.lower() in book['author'].lower()]

    def sort_by_author(self) -> List[Dict[str, str]]:
        """Sort books by author name"""
        return sorted(self.books, key=lambda x: x['author'])

    def sort_by_title(self) -> List[Dict[str, str]]:
        """Sort books by title"""
        return sorted(self.books, key=lambda x: x['title'])

    def get_all_books(self) -> List[Dict[str, str]]:
        """Get all books in the catalog"""
        return self.books.copy() 