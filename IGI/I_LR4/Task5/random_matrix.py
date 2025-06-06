import numpy as np
from matrix_base import Matrix
from typing import Optional, Tuple

class RandomMatrix(Matrix):
    """
    Класс для работы со случайной целочисленной матрицей.
    """
    
    def __init__(self, rows: int, cols: int, min_val: int = 0, max_val: int = 100):
        """
        Инициализация случайной матрицы.
        
        Args:
            rows (int): Количество строк
            cols (int): Количество столбцов
            min_val (int): Минимальное значение для генерации
            max_val (int): Максимальное значение для генерации
            
        Raises:
            ValueError: Если параметры некорректны
        """
        super().__init__(rows, cols)
        
        if min_val >= max_val:
            raise ValueError("Минимальное значение должно быть меньше максимального")
        
        self._min_val = min_val
        self._max_val = max_val
        self.generate()
    
    @property
    def min_val(self) -> int:
        """Получение минимального значения"""
        return self._min_val
    
    @property
    def max_val(self) -> int:
        """Получение максимального значения"""
        return self._max_val
    
    def generate(self) -> None:
        """
        Генерация случайной целочисленной матрицы.
        Использует numpy.random.randint для генерации случайных чисел.
        """
        self._data = np.random.randint(
            self._min_val,
            self._max_val + 1,  # +1 так как randint не включает верхнюю границу
            size=(self._rows, self._cols)
        )
    
    def get_element(self, row: int, col: int) -> int:
        """
        Получение элемента матрицы по индексам.
        
        Args:
            row (int): Индекс строки
            col (int): Индекс столбца
            
        Returns:
            int: Значение элемента
            
        Raises:
            IndexError: Если индексы выходят за границы матрицы
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Индексы выходят за границы матрицы")
        return self._data[row, col]
    
    def get_slice(self, row_slice: slice, col_slice: slice) -> np.ndarray:
        """
        Получение среза матрицы.
        
        Args:
            row_slice (slice): Срез по строкам
            col_slice (slice): Срез по столбцам
            
        Returns:
            np.ndarray: Срез матрицы
        """
        return self._data[row_slice, col_slice]
    
    def __str__(self) -> str:
        """
        Строковое представление случайной матрицы.
        
        Returns:
            str: Матрица в виде строки с дополнительной информацией
        """
        base_str = super().__str__()
        return f"{base_str}\nДиапазон значений: [{self._min_val}, {self._max_val}]"
    
    def __repr__(self) -> str:
        """
        Программное представление случайной матрицы.
        
        Returns:
            str: Представление для воссоздания объекта
        """
        return (
            f"{self.__class__.__name__}(rows={self._rows}, cols={self._cols}, "
            f"min_val={self._min_val}, max_val={self._max_val})"
        ) 