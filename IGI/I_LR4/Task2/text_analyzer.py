import re
from typing import List, Dict, Tuple
from collections import Counter
from base_analyzer import BaseTextAnalyzer, TextAnalyzerMixin

class TextAnalyzer(BaseTextAnalyzer, TextAnalyzerMixin):
    """
    Класс для анализа текста с расширенной функциональностью.
    Наследуется от BaseTextAnalyzer и использует TextAnalyzerMixin.
    """
    
    def __init__(self, text: str):
        super().__init__(text)  # Call parent class constructor
    
    def _split_into_sentences(self) -> List[str]:
        """
        Реализация абстрактного метода разделения текста на предложения.
        
        Returns:
            List[str]: Список предложений
        """
        # Используем более сложное регулярное выражение для корректного разделения
        sentences = []
        # Разбиваем текст на предложения, учитывая разные знаки препинания
        parts = re.split(r'([.!?]+(?:\s+|$))', self.text)
        
        # Собираем предложения обратно с их знаками препинания
        current_sentence = ""
        for part in parts:
            current_sentence += part
            if re.search(r'[.!?]+(?:\s+|$)', part):
                if current_sentence.strip():
                    sentences.append(current_sentence.strip())
                current_sentence = ""
        
        # Добавляем последнее предложение, если оно есть
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        
        return sentences
    
    def analyze(self) -> Dict:
        """
        Реализация абстрактного метода анализа текста.
        
        Returns:
            Dict: Результаты анализа, включая все метрики
        """
        return {
            'Количество предложений': len(self.sentences),
            'Типы предложений': self.get_sentence_types(),
            'Средняя длина предложения': self.get_average_sentence_length(),
            'Средняя длина слова': self.get_average_word_length(),
            'Количество смайликов': self.count_smileys(),
            'Email адреса': self.get_emails_and_names(),
            'Текст с замененными переменными': self.replace_math_vars(),
            'Слова с нечетным количеством букв': self.get_odd_length_words(),
            'Самое короткое слово на i': self.get_shortest_i_word(),
            'Повторяющиеся слова': self.get_repeated_words(),
            'Общее количество слов': self.count_words()
        }
    
    def get_sentence_types(self) -> Dict[str, int]:
        """
        Подсчет количества предложений каждого типа.
        
        Returns:
            Dict[str, int]: Словарь с количеством предложений каждого типа
        """
        types = {
            'повествовательные': 0,
            'вопросительные': 0,
            'побудительные': 0
        }
        
        for sentence in self.sentences:
            if sentence.endswith('?'):
                types['вопросительные'] += 1
            elif sentence.endswith('!'):
                types['побудительные'] += 1
            else:
                types['повествовательные'] += 1
        
        return types
    
    def get_average_sentence_length(self) -> float:
        """
        Вычисление средней длины предложения в символах.
        
        Returns:
            float: Средняя длина предложения
        """
        if not self.sentences:
            return 0.0
            
        total_length = sum(len(sentence) for sentence in self.sentences)
        return total_length / len(self.sentences)
    
    def get_average_word_length(self) -> float:
        """
        Вычисление средней длины слова в символах.
        
        Returns:
            float: Средняя длина слова
        """
        words = self.get_all_words()
        if not words:
            return 0.0
            
        total_length = sum(len(word) for word in words)
        return total_length / len(words)
    
    def count_smileys(self) -> int:
        """
        Подсчет количества смайликов в тексте.
        
        Returns:
            int: Количество найденных смайликов
        """
        pattern = r'[;:]-*([\(\)\[\]])\1+'
        return len(re.findall(pattern, self.text))
    
    def get_emails_and_names(self) -> List[Tuple[str, str]]:
        """
        Извлечение email адресов и соответствующих имен.
        
        Returns:
            List[Tuple[str, str]]: Список кортежей (email, имя)
        """
        pattern = r'(?:([^<>\n:]*?)\s*<)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>?'
        matches = re.finditer(pattern, self.text)
        return [(match.group(2), match.group(1).strip() if match.group(1) else '')
                for match in matches]
    
    def replace_math_vars(self) -> str:
        """
        Замена математических переменных формата $v_(i)$ на v[i].
        
        Returns:
            str: Текст с замененными переменными
        """
        return re.sub(r'\$v_\(([a-zA-Z0-9])\)\$', r'v[\1]', self.text)
    
    def get_odd_length_words(self) -> List[str]:
        """
        Поиск слов с нечетным количеством букв.
        
        Returns:
            List[str]: Список слов с нечетным количеством букв
        """
        words = self.get_all_words()
        return [word for word in words if len(word) % 2 != 0]
    
    def get_shortest_i_word(self) -> str:
        """
        Поиск самого короткого слова, начинающегося на 'i'.
        
        Returns:
            str: Самое короткое слово на 'i' или пустая строка
        """
        i_words = [word for word in re.findall(r'\b[iI]\w+\b', self.text)]
        return min(i_words, key=len) if i_words else ''
    
    def get_repeated_words(self) -> List[str]:
        """
        Поиск повторяющихся слов.
        
        Returns:
            List[str]: Список повторяющихся слов
        """
        words = re.findall(r'\b(?!v_\b)[a-zA-Zа-яА-Я]+\b', self.text.lower())
        word_counts = Counter(words)
        return [word for word, count in word_counts.items() if count > 1] 