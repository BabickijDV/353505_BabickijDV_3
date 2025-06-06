import csv
from data_handler import BookCatalog

class CSVBookCatalog(BookCatalog):
    """Handler for CSV file operations with book catalog"""
    
    def save_to_csv(self, filename: str) -> None:
        """Save book catalog to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Author'])  # Header
            for book in self.books:
                writer.writerow([book['title'], book['author']])

    def load_from_csv(self, filename: str) -> None:
        """Load book catalog from CSV file"""
        self.books = []  # Clear existing books
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) == 2:
                        self.add_book(title=row[0], author=row[1])
            return True
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return False
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return False 