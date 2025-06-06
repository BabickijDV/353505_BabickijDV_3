import re
import zipfile
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
from collections import Counter
from text_analyzer import TextAnalyzer
from file_handler import FileHandler
import sys
from datetime import datetime

class TextAnalyzerBase(ABC):
    """
    Abstract base class for text analyzers.
    Defines the common interface for all text analysis operations.
    """
    
    @abstractmethod
    def analyze(self, text: str) -> Dict:
        """Perform text analysis and return results as a dictionary"""
        pass

class BasicTextAnalyzer(TextAnalyzerBase):
    """
    Basic text analyzer that provides fundamental text statistics.
    Inherits from TextAnalyzerBase.
    """
    
    # Static attribute - shared by all instances
    version = "1.0"
    
    def __init__(self):
        # Dynamic attributes - specific to each instance
        self._text = ""
        self._results = {}
        
    @property
    def text(self) -> str:
        """Getter for the text property"""
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        """Setter for the text property"""
        if not isinstance(value, str):
            raise ValueError("Text must be a string")
        self._text = value
        self._results = {}  # Reset results when text changes
        
    def analyze(self, text: str) -> Dict:
        """
        Perform basic text analysis including:
        - Sentence count
        - Sentence type counts
        - Average sentence length
        - Average word length
        """
        self.text = text
        self._count_sentences()
        self._classify_sentences()
        self._calculate_avg_sentence_length()
        self._calculate_avg_word_length()
        return self._results
    
    def _count_sentences(self) -> None:
        """Count total number of sentences in the text"""
        sentences = re.split(r'[.!?]+', self.text)
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        self._results['total_sentences'] = len(sentences)
    
    def _classify_sentences(self) -> None:
        """Classify sentences by type (declarative, interrogative, exclamatory)"""
        declarative = len(re.findall(r'[^!?]*\.', self.text))
        interrogative = len(re.findall(r'[^.]*\?', self.text))
        exclamatory = len(re.findall(r'[^.]*!', self.text))
        
        self._results['declarative_sentences'] = declarative
        self._results['interrogative_sentences'] = interrogative
        self._results['exclamatory_sentences'] = exclamatory
    
    def _calculate_avg_sentence_length(self) -> None:
        """Calculate average sentence length in characters (words only)"""
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            self._results['avg_sentence_length'] = 0
            return
            
        total_chars = 0
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence)
            total_chars += sum(len(word) for word in words)
            
        self._results['avg_sentence_length'] = total_chars / len(sentences)
    
    def _calculate_avg_word_length(self) -> None:
        """Calculate average word length in characters"""
        words = re.findall(r'\b\w+\b', self.text)
        
        if not words:
            self._results['avg_word_length'] = 0
            return
            
        total_chars = sum(len(word) for word in words)
        self._results['avg_word_length'] = total_chars / len(words)

class AdvancedTextAnalyzer(BasicTextAnalyzer):
    """
    Advanced text analyzer that extends BasicTextAnalyzer with additional features:
    - Email extraction
    - Variable substitution
    - Word analysis
    - Smiley detection
    """
    
    def __init__(self):
        super().__init__()
        self._email_pattern = r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'
        self._variable_pattern = r'\$v_\(([a-zA-Z0-9])\)\$'
        self._smiley_pattern = r'(?::|;)-*[\(\)\[\]]+'
    
    def analyze(self, text: str) -> Dict:
        """
        Perform advanced text analysis including basic stats plus:
        - Email extraction
        - Variable substitution
        - Word analysis
        - Smiley detection
        """
        # First get basic analysis from parent class
        super().analyze(text)
        
        # Add advanced analysis
        self._extract_emails()
        self._substitute_variables()
        self._analyze_words()
        self._count_smileys()
        
        return self._results
    
    def _extract_emails(self) -> None:
        """Extract email addresses and usernames from text"""
        emails = re.findall(self._email_pattern, self.text)
        self._results['emails'] = [{'username': e[0], 'domain': e[1]} for e in emails]
    
    def _substitute_variables(self) -> None:
        """Substitute $v_(i)$ patterns with v[i]"""
        def replacer(match):
            return f'v[{match.group(1)}]'
        
        substituted_text = re.sub(self._variable_pattern, replacer, self.text)
        self._results['substituted_text'] = substituted_text
    
    def _analyze_words(self) -> None:
        """Analyze words in text"""
        words = re.findall(r'\b\w+\b', self.text.lower())
        
        # Words with odd letter count
        odd_length_words = [word for word in words if len(word) % 2 != 0]
        
        # Shortest word starting with 'i'
        i_words = [word for word in words if word.startswith('i')]
        shortest_i_word = min(i_words, key=len, default=None)
        
        # Find duplicate words
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        duplicates = [word for word, count in word_counts.items() if count > 1]
        
        self._results['odd_length_words'] = odd_length_words
        self._results['shortest_i_word'] = shortest_i_word
        self._results['duplicate_words'] = duplicates
    
    def _count_smileys(self) -> None:
        """Count valid smileys in text"""
        smileys = re.findall(self._smiley_pattern, self.text)
        valid_smileys = []
        
        for smiley in smileys:
            # Check that all brackets at the end are the same
            brackets = re.sub(r'^[:;]-*', '', smiley)
            if len(set(brackets)) == 1 and brackets[0] in '()[]':
                valid_smileys.append(smiley)
        
        self._results['smileys'] = valid_smileys
        self._results['smiley_count'] = len(valid_smileys)

class TextAnalysisReport:
    """
    Class for generating and managing text analysis reports.
    Uses composition with TextAnalyzer classes.
    """
    
    def __init__(self, analyzer: TextAnalyzerBase):
        self._analyzer = analyzer
        self._analysis_results = {}
    
    def generate_report(self, text: str) -> Dict:
        """Generate analysis report using the provided analyzer"""
        self._analysis_results = self._analyzer.analyze(text)
        return self._analysis_results
    
    def save_report_to_file(self, filename: str) -> None:
        """Save analysis results to a text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Text Analysis Report\n")
            f.write("===================\n\n")
            
            # Basic statistics
            f.write("Basic Statistics:\n")
            f.write(f"- Total sentences: {self._analysis_results.get('total_sentences', 0)}\n")
            f.write(f"- Declarative sentences: {self._analysis_results.get('declarative_sentences', 0)}\n")
            f.write(f"- Interrogative sentences: {self._analysis_results.get('interrogative_sentences', 0)}\n")
            f.write(f"- Exclamatory sentences: {self._analysis_results.get('exclamatory_sentences', 0)}\n")
            f.write(f"- Average sentence length: {self._analysis_results.get('avg_sentence_length', 0):.2f} characters\n")
            f.write(f"- Average word length: {self._analysis_results.get('avg_word_length', 0):.2f} characters\n")
            f.write(f"- Smiley count: {self._analysis_results.get('smiley_count', 0)}\n")
            
            # Email information
            if 'emails' in self._analysis_results and self._analysis_results['emails']:
                f.write("\nEmail Addresses Found:\n")
                for email in self._analysis_results['emails']:
                    f.write(f"- {email['username']}@{email['domain']}\n")
            
            # Word analysis
            f.write("\nWord Analysis:\n")
            f.write(f"- Words with odd letter count: {len(self._analysis_results.get('odd_length_words', []))}\n")
            
            if 'shortest_i_word' in self._analysis_results and self._analysis_results['shortest_i_word']:
                f.write(f"- Shortest word starting with 'i': {self._analysis_results['shortest_i_word']}\n")
            
            if 'duplicate_words' in self._analysis_results and self._analysis_results['duplicate_words']:
                f.write("- Duplicate words found:\n")
                for word in set(self._analysis_results['duplicate_words']):
                    f.write(f"  - {word}\n")
            
            # Substituted text
            if 'substituted_text' in self._analysis_results:
                f.write("\nText with Variables Substituted:\n")
                f.write(self._analysis_results['substituted_text'] + "\n")
            
            # Smileys found
            if 'smileys' in self._analysis_results and self._analysis_results['smileys']:
                f.write("\nValid Smileys Found:\n")
                for smiley in self._analysis_results['smileys']:
                    f.write(f"- {smiley}\n")
    
    @staticmethod
    def create_zip_archive(source_file: str, zip_filename: str) -> None:
        """Create a ZIP archive containing the report file"""
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(source_file, os.path.basename(source_file))
    
    @staticmethod
    def get_zip_file_info(zip_filename: str) -> Dict:
        """Get information about files in a ZIP archive"""
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            return {
                'file_count': len(zipf.namelist()),
                'files': zipf.namelist(),
                'archive_size': os.path.getsize(zip_filename),
                'compression_info': [
                    {
                        'filename': name,
                        'compress_size': info.compress_size,
                        'file_size': info.file_size,
                        'compression_ratio': info.compress_size / info.file_size if info.file_size else 0
                    }
                    for name, info in zipf.infolist()
                ]
            }

class UserInterface:
    """
    Класс для управления пользовательским интерфейсом.
    """
    
    def __init__(self):
        """Инициализация интерфейса"""
        self.analyzer: Optional[TextAnalyzer] = None
        self.results: Optional[Dict] = None
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Отображение главного меню"""
        print("\n=== Анализатор текста ===")
        print("1. Загрузить текст из файла")
        print("2. Ввести текст вручную")
        print("3. Выход")
    
    def get_user_choice(self, min_value: int, max_value: int) -> int:
        """
        Получение выбора пользователя с валидацией.
        
        Args:
            min_value (int): Минимальное допустимое значение
            max_value (int): Максимальное допустимое значение
        
        Returns:
            int: Выбор пользователя
        """
        while True:
            try:
                choice = int(input(f"\nВыберите действие ({min_value}-{max_value}): "))
                if min_value <= choice <= max_value:
                    return choice
                print(f"Пожалуйста, введите число от {min_value} до {max_value}")
            except ValueError:
                print("Пожалуйста, введите целое число")
    
    def save_results_automatically(self):
        """
        Автоматическое сохранение результатов с временной меткой.
        """
        if not self.results:
            return
        
        try:
            # Создаем директорию для результатов в текущей папке
            results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
            FileHandler.ensure_directory_exists(results_dir)
            
            # Генерируем имя файла с временной меткой
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(results_dir, f"analysis_results_{timestamp}.txt")
            zip_file = os.path.join(results_dir, f"analysis_results_{timestamp}.zip")
            
            # Сохраняем результаты
            FileHandler.save_results(self.results, output_file)
            FileHandler.create_zip_archive(output_file, zip_file)
            
            # Получаем информацию о файлах
            zip_info = FileHandler.get_zip_info(zip_file)
            
            print("\nРезультаты автоматически сохранены:")
            print(f"Текстовый файл: {output_file}")
            print(f"ZIP архив: {zip_file}")
            print("\nИнформация о ZIP архиве:")
            for key, value in zip_info.items():
                print(f"{key}: {value}")
            
        except Exception as e:
            print(f"\nОшибка при сохранении результатов: {e}")
    
    def process_text(self):
        """
        Автоматический анализ текста и вывод результатов.
        """
        try:
            self.results = self.analyzer.analyze()
            print("\n=== Результаты анализа текста ===")
            for key, value in self.results.items():
                print(f"\n{key}:")
                print(value)
            
            # Автоматически сохраняем результаты
            self.save_results_automatically()
            
        except Exception as e:
            print(f"Ошибка при анализе текста: {e}")
    
    def load_text_from_file(self):
        """Загрузка текста из файла с выбором из списка"""
        try:
            # Получаем список текстовых файлов
            files = FileHandler.list_text_files()
            
            # Отображаем список файлов
            FileHandler.display_file_list(files)
            
            if not files:
                print("\nСоздайте текстовый файл и повторите попытку.")
                return
            
            # Выбор файла
            try:
                selected_file = FileHandler.select_file(files)
            except ValueError as e:
                if str(e) == "Операция отменена пользователем":
                    print("\nЗагрузка файла отменена.")
                    return
                raise
            
            # Предварительный просмотр файла
            FileHandler.preview_file(selected_file)
            
            # Подтверждение выбора
            confirm = input("\nИспользовать этот файл? (y/n): ").lower()
            if confirm != 'y':
                print("Загрузка файла отменена.")
                return
            
            # Загрузка текста
            text = FileHandler.read_text_file(selected_file)
            self.analyzer = TextAnalyzer(text)
            print("\nТекст успешно загружен!")
            
            # Автоматический анализ
            self.process_text()
            
        except FileNotFoundError:
            print("\nОшибка: Файл не найден")
        except ValueError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nПроизошла неожиданная ошибка: {e}")
    
    def input_text(self):
        """Ввод текста вручную"""
        print("\nВведите текст (для завершения введите пустую строку):")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        
        text = '\n'.join(lines)
        try:
            self.analyzer = TextAnalyzer(text)
            print("Текст успешно загружен!")
            self.process_text()  # Автоматический анализ после ввода
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    def run(self):
        """Основной цикл программы"""
        while True:
            try:
                self.clear_screen()
                self.display_menu()
                choice = self.get_user_choice(1, 3)
                
                if choice == 1:
                    self.load_text_from_file()
                elif choice == 2:
                    self.input_text()
                elif choice == 3:
                    print("\nСпасибо за использование программы!")
                    break
                
                input("\nНажмите Enter для продолжения...")
            
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем.")
                sys.exit(0)
            except Exception as e:
                print(f"\nПроизошла неожиданная ошибка: {e}")
                input("\nНажмите Enter для продолжения...")

def main():
    """Точка входа в программу"""
    ui = UserInterface()
    ui.run()

if __name__ == "__main__":
    main()