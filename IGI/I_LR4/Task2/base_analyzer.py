from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

class TextAnalyzerMixin:
    """Миксин для дополнительных функций анализа текста"""
    def count_words(self) -> int:
        """Подсчет общего количества слов в тексте"""
        return len(self.get_all_words())
    
    def get_all_words(self) -> List[str]:
        """Получение списка всех слов"""
        import re
        return re.findall(r'\b[a-zA-Zа-яА-Я]+\b', self.text)

class BaseTextAnalyzer(ABC):
    """
    Абстрактный базовый класс для анализа текста.
    
    Attributes:
        text (str): Анализируемый текст
        _sentences (List[str]): Кэшированный список предложений
        version (str): Версия анализатора (статический атрибут)
    """
    
    version = "1.0"  # Статический атрибут
    
    def __init__(self, text: str):
        """
        Инициализация анализатора текста.
        
        Args:
            text (str): Текст для анализа
        
        Raises:
            ValueError: Если текст пустой или None
        """
        if not text or not isinstance(text, str):
            raise ValueError("Текст не может быть пустым или None")
        self._text = text
        self._cached_sentences = None  # Динамический атрибут для кэширования
    
    @property
    def text(self) -> str:
        """Геттер для текста"""
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        """
        Сеттер для текста.
        
        Args:
            value (str): Новый текст
            
        Raises:
            ValueError: Если текст пустой или None
        """
        if not value or not isinstance(value, str):
            raise ValueError("Текст не может быть пустым или None")
        self._text = value
        self._cached_sentences = None  # Сброс кэша
    
    @property
    def sentences(self) -> List[str]:
        """
        Свойство для получения списка предложений с кэшированием.
        Это свойство только для чтения, изменение списка предложений
        должно происходить через изменение текста.
        
        Returns:
            List[str]: Список предложений
        """
        if self._cached_sentences is None:
            self._cached_sentences = self._split_into_sentences()
        return self._cached_sentences
    
    @abstractmethod
    def _split_into_sentences(self) -> List[str]:
        """
        Абстрактный метод разделения текста на предложения.
        
        Returns:
            List[str]: Список предложений
        """
        pass
    
    @abstractmethod
    def analyze(self) -> Dict:
        """
        Абстрактный метод анализа текста.
        
        Returns:
            Dict: Результаты анализа
        """
        pass
    
    def __len__(self) -> int:
        """
        Магический метод для получения длины текста.
        
        Returns:
            int: Количество символов в тексте
        """
        return len(self._text)
    
    def __str__(self) -> str:
        """
        Магический метод для строкового представления.
        
        Returns:
            str: Информация об анализаторе
        """
        return f"TextAnalyzer(version={self.version}, text_length={len(self)})"
    
    @classmethod
    def get_version(cls) -> str:
        """
        Классовый метод для получения версии.
        
        Returns:
            str: Версия анализатора
        """
        return cls.version 