from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple, Optional

class MatrixStatsMixin:
    """
    Миксин для статистических операций с матрицей.
    """
    
    def mean(self) -> float:
        """Вычисление среднего значения матрицы"""
        return np.mean(self.data)
    
    def median(self) -> float:
        """Вычисление медианы матрицы"""
        return np.median(self.data)
    
    def var(self) -> float:
        """Вычисление дисперсии матрицы"""
        return np.var(self.data)
    
    def std(self) -> float:
        """Вычисление стандартного отклонения матрицы"""
        return np.std(self.data)
    
    def correlation_even_odd(self) -> float:
        """
        Вычисление коэффициента корреляции между элементами с четными и нечетными индексами.
        
        Returns:
            float: Коэффициент корреляции
        """
        # Получаем элементы с четными и нечетными индексами
        flat_data = self.data.flatten()
        even_indices = flat_data[::2]  # элементы с четными индексами
        odd_indices = flat_data[1::2]  # элементы с нечетными индексами
        
        # Если длины разные, обрезаем более длинный массив
        min_length = min(len(even_indices), len(odd_indices))
        even_indices = even_indices[:min_length]
        odd_indices = odd_indices[:min_length]
        
        # Вычисляем коэффициент корреляции
        correlation_matrix = np.corrcoef(even_indices, odd_indices)
        return correlation_matrix[0, 1]  # Возвращаем коэффициент корреляции

class Matrix(ABC, MatrixStatsMixin):
    """
    Абстрактный базовый класс для работы с матрицами.
    """
    
    # Статический атрибут для версии
    version = "1.0"
    
    def __init__(self, rows: int, cols: int):
        """
        Инициализация матрицы.
        
        Args:
            rows (int): Количество строк
            cols (int): Количество столбцов
            
        Raises:
            ValueError: Если размеры матрицы некорректны
        """
        if rows <= 0 or cols <= 0:
            raise ValueError("Размеры матрицы должны быть положительными числами")
        
        self._rows = rows
        self._cols = cols
        self._data = None
    
    @property
    def shape(self) -> Tuple[int, int]:
        """Получение размеров матрицы"""
        return self._rows, self._cols
    
    @property
    def data(self) -> np.ndarray:
        """Получение данных матрицы"""
        return self._data
    
    @abstractmethod
    def generate(self) -> None:
        """Абстрактный метод для генерации матрицы"""
        pass
    
    def min_row_sum(self) -> Tuple[int, float]:
        """
        Поиск минимальной суммы среди строк матрицы.
        
        Returns:
            Tuple[int, float]: (индекс строки, минимальная сумма)
        """
        row_sums = np.sum(self._data, axis=1)
        min_idx = np.argmin(row_sums)
        return min_idx, row_sums[min_idx]
    
    def __str__(self) -> str:
        """
        Строковое представление матрицы.
        
        Returns:
            str: Матрица в виде строки
        """
        if self._data is None:
            return "Матрица не инициализирована"
        
        return f"Матрица размером {self._rows}x{self._cols}:\n{self._data}"
    
    def __repr__(self) -> str:
        """
        Программное представление матрицы.
        
        Returns:
            str: Представление для воссоздания объекта
        """
        return f"{self.__class__.__name__}(rows={self._rows}, cols={self._cols})" 