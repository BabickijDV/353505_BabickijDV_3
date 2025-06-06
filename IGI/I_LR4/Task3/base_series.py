from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict, Tuple
import math
from scipy import stats

class SeriesStatisticsMixin:
    """Миксин для расчета статистических характеристик последовательности"""
    
    def calculate_mean(self, values: List[float]) -> float:
        """
        Вычисляет среднее арифметическое последовательности.
        
        Args:
            values (List[float]): Список значений
            
        Returns:
            float: Среднее арифметическое
        """
        return np.mean(values)
    
    def calculate_median(self, values: List[float]) -> float:
        """
        Вычисляет медиану последовательности.
        
        Args:
            values (List[float]): Список значений
            
        Returns:
            float: Медиана
        """
        return np.median(values)
    
    def calculate_mode(self, values: List[float]) -> float:
        """
        Вычисляет моду последовательности.
        
        Args:
            values (List[float]): Список значений
            
        Returns:
            float: Мода или среднее значение, если мода не может быть определена
        """
        try:
            # Используем numpy для более надежного вычисления моды
            values_array = np.array(values)
            unique_values, counts = np.unique(values_array, return_counts=True)
            
            # Находим индексы значений с максимальной частотой
            max_count_indices = np.where(counts == counts.max())[0]
            
            # Если все значения встречаются одинаковое число раз,
            # возвращаем среднее значение
            if len(max_count_indices) == len(unique_values):
                return float(np.mean(values_array))
            
            # Иначе возвращаем первое значение с максимальной частотой
            return float(unique_values[max_count_indices[0]])
            
        except Exception:
            # В случае ошибки возвращаем среднее значение
            return float(np.mean(values))
    
    def calculate_variance(self, values: List[float]) -> float:
        """
        Вычисляет дисперсию последовательности.
        
        Args:
            values (List[float]): Список значений
            
        Returns:
            float: Дисперсия
        """
        return np.var(values)
    
    def calculate_std(self, values: List[float]) -> float:
        """
        Вычисляет среднеквадратическое отклонение последовательности.
        
        Args:
            values (List[float]): Список значений
            
        Returns:
            float: СКО
        """
        return np.std(values)

class BaseSeries(ABC):
    """
    Абстрактный базовый класс для работы с рядами.
    
    Attributes:
        x_values (List[float]): Значения аргумента
        n_terms (int): Количество членов ряда
        _results (Dict): Кэш результатов вычислений
        version (str): Версия класса
    """
    
    version = "1.0"  # Статический атрибут
    
    def __init__(self, x_start: float, x_end: float, n_points: int, n_terms: int):
        """
        Инициализация базового класса.
        
        Args:
            x_start (float): Начальное значение x
            x_end (float): Конечное значение x
            n_points (int): Количество точек
            n_terms (int): Количество членов ряда
            
        Raises:
            ValueError: Если входные параметры некорректны
        """
        if not isinstance(n_points, int) or n_points <= 0:
            raise ValueError("Количество точек должно быть положительным целым числом")
        if not isinstance(n_terms, int) or n_terms <= 0:
            raise ValueError("Количество членов ряда должно быть положительным целым числом")
            
        self._x_values = np.linspace(x_start, x_end, n_points)
        self._n_terms = n_terms
        self._results = {}  # Кэш результатов
        
    @property
    def x_values(self) -> np.ndarray:
        """Геттер для значений аргумента"""
        return self._x_values
    
    @property
    def n_terms(self) -> int:
        """Геттер для количества членов ряда"""
        return self._n_terms
    
    @n_terms.setter
    def n_terms(self, value: int) -> None:
        """
        Сеттер для количества членов ряда.
        
        Args:
            value (int): Новое количество членов ряда
            
        Raises:
            ValueError: Если значение некорректно
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Количество членов ряда должно быть положительным целым числом")
        self._n_terms = value
        self._results.clear()  # Очищаем кэш при изменении параметров
    
    @abstractmethod
    def calculate_series(self, x: float) -> float:
        """
        Абстрактный метод вычисления значения ряда.
        
        Args:
            x (float): Значение аргумента
            
        Returns:
            float: Значение ряда
        """
        pass
    
    @abstractmethod
    def calculate_function(self, x: float) -> float:
        """
        Абстрактный метод вычисления значения функции.
        
        Args:
            x (float): Значение аргумента
            
        Returns:
            float: Значение функции
        """
        pass
    
    def get_series_values(self) -> np.ndarray:
        """
        Вычисляет значения ряда для всех точек.
        
        Returns:
            np.ndarray: Массив значений ряда
        """
        if 'series_values' not in self._results:
            self._results['series_values'] = np.array([self.calculate_series(x) for x in self.x_values])
        return self._results['series_values']
    
    def get_function_values(self) -> np.ndarray:
        """
        Вычисляет значения функции для всех точек.
        
        Returns:
            np.ndarray: Массив значений функции
        """
        if 'function_values' not in self._results:
            self._results['function_values'] = np.array([self.calculate_function(x) for x in self.x_values])
        return self._results['function_values']
    
    def __len__(self) -> int:
        """
        Возвращает количество точек.
        
        Returns:
            int: Количество точек
        """
        return len(self._x_values)
    
    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта.
        
        Returns:
            str: Строковое представление
        """
        return f"{self.__class__.__name__}(version={self.version}, points={len(self)}, terms={self.n_terms})" 