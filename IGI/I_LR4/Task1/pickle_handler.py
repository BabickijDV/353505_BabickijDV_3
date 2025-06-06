import pickle
from data_handler import BookCatalog

class PickleBookCatalog(BookCatalog):
    """Handler for Pickle file operations with book catalog"""
    
    def save_to_pickle(self, filename: str) -> bool:
        """Save book catalog to Pickle file"""
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.books, file)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False

    def load_from_pickle(self, filename: str) -> bool:
        """Load book catalog from Pickle file"""
        try:
            with open(filename, 'rb') as file:
                self.books = pickle.load(file)
            return True
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return False
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return False 