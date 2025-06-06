from base_series import BaseSeries, SeriesStatisticsMixin
import numpy as np
import math
from typing import List, Dict, Tuple

class LogarithmicSeries(BaseSeries, SeriesStatisticsMixin):
    """
    Класс для работы с логарифмическим рядом ln(1+x).
    Наследуется от BaseSeries и использует SeriesStatisticsMixin.
    """
    
    def __init__(self, x_start: float = -0.9, x_end: float = 0.9, n_points: int = 100, n_terms: int = 10):
        """
        Инициализация класса для логарифмического ряда.
        
        Args:
            x_start (float): Начальное значение x (по умолчанию -0.9)
            x_end (float): Конечное значение x (по умолчанию 0.9)
            n_points (int): Количество точек (по умолчанию 100)
            n_terms (int): Количество членов ряда (по умолчанию 10)
            
        Raises:
            ValueError: Если значения x выходят за пределы области сходимости
        """
        if x_start <= -1 or x_end >= 1:
            raise ValueError("Значения x должны быть в интервале (-1, 1)")
        super().__init__(x_start, x_end, n_points, n_terms)
    
    def calculate_series(self, x: float) -> float:
        """
        Вычисляет значение логарифмического ряда ln(1+x).
        
        Args:
            x (float): Значение аргумента
            
        Returns:
            float: Значение ряда
            
        Raises:
            ValueError: Если x не в области сходимости
        """
        if abs(x) >= 1:
            raise ValueError("Значение x должно быть в интервале (-1, 1)")
            
        result = 0
        for n in range(1, self.n_terms + 1):
            result += ((-1)**(n-1) * x**n) / n
        return result
    
    def calculate_function(self, x: float) -> float:
        """
        Вычисляет точное значение функции ln(1+x).
        
        Args:
            x (float): Значение аргумента
            
        Returns:
            float: Значение функции
            
        Raises:
            ValueError: Если x не в области определения
        """
        if x <= -1:
            raise ValueError("Значение x должно быть больше -1")
        return math.log(1 + x)
    
    def get_statistics(self) -> Dict[str, float]:
        """
        Вычисляет статистические характеристики для значений ряда.
        
        Returns:
            Dict[str, float]: Словарь со статистическими характеристиками
        """
        series_values = self.get_series_values()
        return {
            'Среднее': self.calculate_mean(series_values),
            'Медиана': self.calculate_median(series_values),
            'Мода': self.calculate_mode(series_values),
            'Дисперсия': self.calculate_variance(series_values),
            'СКО': self.calculate_std(series_values)
        }
    
    def get_comparison_table(self) -> List[Dict[str, float]]:
        """
        Создает таблицу сравнения значений ряда и функции.
        
        Returns:
            List[Dict[str, float]]: Список словарей с результатами
        """
        series_values = self.get_series_values()
        function_values = self.get_function_values()
        
        return [
            {
                'x': x,
                'F(x)': series,
                'n': self.n_terms,
                'Math F(x)': func
            }
            for x, series, func in zip(self.x_values, series_values, function_values)
        ] 