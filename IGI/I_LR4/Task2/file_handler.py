import os
import zipfile
from typing import Dict, Any, List
import json

class FileHandler:
    """
    Класс для работы с файлами.
    Обеспечивает чтение, запись и архивацию файлов.
    """
    
    SUPPORTED_EXTENSIONS = ('.txt', '.md', '.log')
    
    @staticmethod
    def list_text_files(directory: str = '.') -> List[str]:
        """
        Получение списка текстовых файлов в указанной директории.
        
        Args:
            directory (str): Путь к директории для поиска
            
        Returns:
            List[str]: Список найденных текстовых файлов
        """
        text_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(FileHandler.SUPPORTED_EXTENSIONS):
                    full_path = os.path.join(root, file)
                    # Преобразуем путь в относительный
                    rel_path = os.path.relpath(full_path, directory)
                    text_files.append(rel_path)
        return sorted(text_files)
    
    @staticmethod
    def display_file_list(files: List[str]) -> None:
        """
        Отображение списка файлов с нумерацией.
        
        Args:
            files (List[str]): Список файлов для отображения
        """
        if not files:
            print("\nТекстовые файлы не найдены")
            return
            
        print("\nДоступные текстовые файлы:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
    
    @staticmethod
    def select_file(files: List[str]) -> str:
        """
        Выбор файла из списка.
        
        Args:
            files (List[str]): Список файлов для выбора
            
        Returns:
            str: Выбранный файл
            
        Raises:
            ValueError: Если введен некорректный номер файла
        """
        while True:
            try:
                choice = int(input("\nВведите номер файла (или 0 для отмены): "))
                if choice == 0:
                    raise ValueError("Операция отменена пользователем")
                if 1 <= choice <= len(files):
                    return files[choice - 1]
                print(f"Пожалуйста, введите число от 1 до {len(files)}")
            except ValueError as e:
                if str(e) == "Операция отменена пользователем":
                    raise
                print("Пожалуйста, введите целое число")
    
    @staticmethod
    def preview_file(filename: str, max_lines: int = 5) -> None:
        """
        Предварительный просмотр содержимого файла.
        
        Args:
            filename (str): Имя файла
            max_lines (int): Максимальное количество строк для отображения
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                print(f"\nПредварительный просмотр файла {filename}:")
                print("-" * 50)
                for i, line in enumerate(f, 1):
                    if i > max_lines:
                        print("...")
                        break
                    print(line.rstrip())
                print("-" * 50)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
    
    @staticmethod
    def read_text_file(filename: str) -> str:
        """
        Чтение текстового файла.
        
        Args:
            filename (str): Путь к файлу
            
        Returns:
            str: Содержимое файла
            
        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если файл пустой
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")
        
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            
        if not text.strip():
            raise ValueError("Файл пустой")
            
        return text
    
    @staticmethod
    def save_results(results: Dict[str, Any], filename: str) -> None:
        """
        Сохранение результатов в файл.
        
        Args:
            results (Dict[str, Any]): Результаты для сохранения
            filename (str): Имя файла
            
        Raises:
            IOError: При ошибке записи в файл
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise IOError(f"Ошибка при сохранении результатов: {e}")
    
    @staticmethod
    def create_zip_archive(source_file: str, zip_file: str) -> None:
        """
        Создание ZIP архива.
        
        Args:
            source_file (str): Файл для архивации
            zip_file (str): Имя ZIP файла
            
        Raises:
            FileNotFoundError: Если исходный файл не найден
            zipfile.BadZipFile: При ошибке создания архива
        """
        if not os.path.exists(source_file):
            raise FileNotFoundError(f"Файл {source_file} не найден")
        
        try:
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(source_file, os.path.basename(source_file))
        except zipfile.BadZipFile as e:
            raise zipfile.BadZipFile(f"Ошибка при создании архива: {e}")
    
    @staticmethod
    def get_zip_info(zip_file: str) -> Dict[str, Any]:
        """
        Получение информации о ZIP архиве.
        
        Args:
            zip_file (str): Путь к ZIP файлу
            
        Returns:
            Dict[str, Any]: Информация об архиве
            
        Raises:
            FileNotFoundError: Если архив не найден
            zipfile.BadZipFile: При ошибке чтения архива
        """
        if not os.path.exists(zip_file):
            raise FileNotFoundError(f"Архив {zip_file} не найден")
        
        try:
            with zipfile.ZipFile(zip_file, 'r') as zf:
                info = zf.infolist()[0]
                return {
                    'Имя файла': info.filename,
                    'Размер файла': f"{info.file_size:,} байт",
                    'Сжатый размер': f"{info.compress_size:,} байт",
                    'Степень сжатия': f"{(1 - info.compress_size / info.file_size) * 100:.1f}%"
                }
        except zipfile.BadZipFile as e:
            raise zipfile.BadZipFile(f"Ошибка при чтении архива: {e}")
    
    @staticmethod
    def ensure_directory_exists(directory: str) -> None:
        """
        Создает директорию, если она не существует.
        
        Args:
            directory (str): Путь к директории
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            raise ValueError(f"Не удалось создать директорию {directory}: {e}") 