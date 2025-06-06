from base_shapes import Shape, ColorMixin
import math
from typing import List, Tuple

class IsoscelesTrapezoid(Shape, ColorMixin):
    """
    Класс для представления равнобедренной трапеции.
    Наследуется от Shape и использует ColorMixin.
    """
    
    # Статический атрибут с названием фигуры
    _shape_name = "Равнобедренная трапеция"
    
    def __init__(self, a: float, b: float, h: float, color: str = 'синий'):
        """
        Инициализация трапеции.
        
        Args:
            a (float): Длина нижнего основания
            b (float): Длина верхнего основания
            h (float): Высота трапеции
            color (str): Цвет фигуры
            
        Raises:
            ValueError: Если параметры некорректны
        """
        # Проверка корректности параметров
        if a <= 0 or b <= 0 or h <= 0:
            raise ValueError("Все размеры должны быть положительными")
        if b >= a:
            raise ValueError("Верхнее основание должно быть меньше нижнего")
            
        self._a = a  # нижнее основание
        self._b = b  # верхнее основание
        self._h = h  # высота
        
        # Вычисляем длину боковой стороны
        self._side = math.sqrt(h**2 + ((a - b)/2)**2)
        
        # Инициализируем цвет через миксин
        super().__init__(color)
    
    @property
    def name(self) -> str:
        """Получение названия фигуры"""
        return self._shape_name
    
    @property
    def a(self) -> float:
        """Геттер для нижнего основания"""
        return self._a
    
    @property
    def b(self) -> float:
        """Геттер для верхнего основания"""
        return self._b
    
    @property
    def h(self) -> float:
        """Геттер для высоты"""
        return self._h
    
    def area(self) -> float:
        """
        Вычисление площади трапеции.
        
        Returns:
            float: Площадь трапеции
        """
        return (self._a + self._b) * self._h / 2
    
    def perimeter(self) -> float:
        """
        Вычисление периметра трапеции.
        
        Returns:
            float: Периметр трапеции
        """
        return self._a + self._b + 2 * self._side
    
    def get_vertices(self) -> List[Tuple[float, float]]:
        """
        Получение координат вершин трапеции.
        Трапеция центрируется относительно начала координат.
        
        Returns:
            List[Tuple[float, float]]: Список координат вершин
        """
        # Вычисляем координаты вершин
        x_offset = (self._a - self._b) / 2
        
        # Координаты вершин (против часовой стрелки, начиная с левой нижней)
        vertices = [
            (-self._a/2, -self._h/2),  # левая нижняя
            (self._a/2, -self._h/2),   # правая нижняя
            (self._b/2, self._h/2),    # правая верхняя
            (-self._b/2, self._h/2)    # левая верхняя
        ]
        
        return vertices
    
    def __str__(self) -> str:
        """
        Строковое представление трапеции.
        
        Returns:
            str: Описание трапеции
        """
        return (
            f"{self.name} {self.color} цвета\n"
            f"Нижнее основание: {self._a:.2f}\n"
            f"Верхнее основание: {self._b:.2f}\n"
            f"Высота: {self._h:.2f}\n"
            f"Площадь: {self.area():.2f}\n"
            f"Периметр: {self.perimeter():.2f}"
        )
    
    def __repr__(self) -> str:
        """
        Программное представление трапеции.
        
        Returns:
            str: Представление для воссоздания объекта
        """
        return f"IsoscelesTrapezoid(a={self._a}, b={self._b}, h={self._h}, color='{self.color}')" 