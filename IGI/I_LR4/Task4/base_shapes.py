from abc import ABC, abstractmethod
from typing import Tuple

class ColorMixin:
    """
    Миксин для работы с цветом фигуры.
    Добавляет функциональность управления цветом.
    """
    _available_colors = {
        'красный': 'red',
        'синий': 'blue',
        'зеленый': 'green',
        'желтый': 'yellow',
        'черный': 'black',
        'белый': 'white',
        'фиолетовый': 'purple',
        'оранжевый': 'orange'
    }
    
    def __init__(self, color: str = 'синий'):
        """
        Инициализация цвета фигуры.
        
        Args:
            color (str): Цвет фигуры на русском языке
            
        Raises:
            ValueError: Если указан недопустимый цвет
        """
        self._color = None
        self.color = color  # Используем сеттер для валидации
    
    @property
    def color(self) -> str:
        """Геттер для цвета фигуры"""
        return self._color
    
    @color.setter
    def color(self, value: str) -> None:
        """
        Сеттер для цвета фигуры.
        
        Args:
            value (str): Цвет фигуры на русском языке
            
        Raises:
            ValueError: Если указан недопустимый цвет
        """
        value = value.lower()
        if value not in self._available_colors:
            raise ValueError(
                f"Недопустимый цвет. Доступные цвета: {', '.join(self._available_colors.keys())}"
            )
        self._color = value
    
    @property
    def color_code(self) -> str:
        """Получение кода цвета для matplotlib"""
        return self._available_colors[self._color]

class Shape(ABC):
    """
    Абстрактный базовый класс для геометрических фигур.
    """
    
    # Статический атрибут для версии
    version = "1.0"
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Абстрактное свойство для получения названия фигуры"""
        pass
    
    @abstractmethod
    def area(self) -> float:
        """
        Абстрактный метод для вычисления площади фигуры.
        
        Returns:
            float: Площадь фигуры
        """
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """
        Абстрактный метод для вычисления периметра фигуры.
        
        Returns:
            float: Периметр фигуры
        """
        pass
    
    @abstractmethod
    def get_vertices(self) -> list:
        """
        Абстрактный метод для получения координат вершин фигуры.
        
        Returns:
            list: Список координат вершин
        """
        pass
    
    def __str__(self) -> str:
        """
        Магический метод для получения строкового представления фигуры.
        
        Returns:
            str: Строковое представление
        """
        return f"{self.name} (версия {self.version})"
    
    def __repr__(self) -> str:
        """
        Магический метод для получения программного представления фигуры.
        
        Returns:
            str: Программное представление
        """
        return f"{self.__class__.__name__}()" 