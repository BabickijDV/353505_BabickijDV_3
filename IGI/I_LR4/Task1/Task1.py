import csv
import pickle
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from csv_handler import CSVBookCatalog
from pickle_handler import PickleBookCatalog

class BookCatalog(ABC):
    """Abstract base class for book catalog operations"""
    
    @abstractmethod
    def add_book(self, title, author):
        pass
    
    @abstractmethod
    def search_by_author(self, author):
        pass
    
    @abstractmethod
    def save_to_file(self, filename):
        pass
    
    @abstractmethod
    def load_from_file(self, filename):
        pass

class EnhancedBookCatalog(CSVBookCatalog):
    """Enhanced book catalog with additional features"""
    
    def __init__(self):
        super().__init__()
        self._sort_order = "author"  # Protected attribute
        
    @property
    def sort_order(self):
        """Get the current sort order"""
        return self._sort_order
    
    @sort_order.setter
    def sort_order(self, value):
        """Set the sort order (author or title)"""
        if value.lower() in ["author", "title"]:
            self._sort_order = value.lower()
        else:
            print("Invalid sort order. Use 'author' or 'title'.")
    
    def get_sorted_books(self):
        """Get books sorted by current sort order"""
        return sorted(self.books, key=lambda x: x[self._sort_order])
    
    def __str__(self):
        """String representation of the catalog"""
        return f"BookCatalog with {len(self.books)} books (sorted by {self._sort_order})"
    
    def __len__(self):
        """Number of books in catalog"""
        return len(self.books)

class DataHandler:
    """Base class for data handling operations"""
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def sort_by_key(self) -> Dict[str, Any]:
        """Sort dictionary by keys"""
        return dict(sorted(self.data.items()))

    def sort_by_value(self) -> Dict[str, Any]:
        """Sort dictionary by values"""
        return dict(sorted(self.data.items(), key=lambda x: x[1]))

    def search_by_key(self, key: str) -> Any:
        """Search dictionary by key"""
        return self.data.get(key, None)

    def search_by_value(self, value: Any) -> List[str]:
        """Search dictionary by value and return all matching keys"""
        return [k for k, v in self.data.items() if v == value]

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu"""
    print("\n=== Каталог книг библиотеки ===")
    print("1. Добавить книгу")
    print("2. Поиск книг по автору")
    print("3. Показать все книги")
    print("4. Сохранить в CSV")
    print("5. Загрузить из CSV")
    print("6. Сохранить в Pickle")
    print("7. Загрузить из Pickle")
    print("8. Выход")

def get_book_info():
    """Get book information from user"""
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    return title, author

def main():
    # Инициализируем оба каталога
    csv_catalog = CSVBookCatalog()
    pickle_catalog = PickleBookCatalog()
    
    # Используем csv_catalog как основной
    catalog = csv_catalog
    
    while True:
        clear_screen()
        display_menu()
        
        try:
            choice = int(input("\nВыберите действие (1-8): "))
        except ValueError:
            print("Пожалуйста, введите число от 1 до 8")
            input("Нажмите Enter для продолжения...")
            continue

        if choice == 1:
            # Добавить книгу
            title, author = get_book_info()
            catalog.add_book(title, author)
            print(f"\nКнига '{title}' автора {author} добавлена в каталог.")

        elif choice == 2:
            # Поиск по автору
            author = input("\nВведите имя автора для поиска: ")
            books = catalog.search_by_author(author)
            if books:
                print(f"\nНайдены книги автора {author}:")
                for book in books:
                    print(f"- '{book['title']}'")
            else:
                print(f"Книги автора {author} не найдены.")

        elif choice == 3:
            # Показать все книги
            books = catalog.get_all_books()
            if books:
                print("\nВсе книги в каталоге:")
                for book in books:
                    print(f"- '{book['title']}' (Автор: {book['author']})")
            else:
                print("Каталог пуст.")

        elif choice == 4:
            # Сохранить в CSV
            catalog.save_to_csv('library.csv')
            print("Каталог сохранен в файл library.csv")

        elif choice == 5:
            # Загрузить из CSV
            if catalog.load_from_csv('library.csv'):
                print("Каталог загружен из файла library.csv")

        elif choice == 6:
            # Сохранить в Pickle
            pickle_catalog.books = catalog.get_all_books()  # Синхронизируем данные
            pickle_catalog.save_to_pickle('library.pickle')
            print("Каталог сохранен в файл library.pickle")

        elif choice == 7:
            # Загрузить из Pickle
            if pickle_catalog.load_from_pickle('library.pickle'):
                catalog.books = pickle_catalog.get_all_books()  # Синхронизируем данные
                print("Каталог загружен из файла library.pickle")

        elif choice == 8:
            # Выход
            print("\nДо свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 8.")

        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()