import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple
import os
from datetime import datetime
from pathlib import Path

class ShapeVisualizer:
    """
    Класс для визуализации геометрических фигур.
    """
    
    def __init__(self):
        """Инициализация визуализатора"""
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        
    def draw_shape(self, vertices: List[Tuple[float, float]], color: str, title: str = '') -> None:
        """
        Отрисовка фигуры по её вершинам.
        
        Args:
            vertices (List[Tuple[float, float]]): Список координат вершин
            color (str): Цвет фигуры
            title (str): Заголовок для графика
        """
        # Очистка предыдущего графика
        self.ax.clear()
        
        # Создание полигона
        polygon = patches.Polygon(vertices, facecolor=color, alpha=0.5)
        
        # Добавление полигона на график
        self.ax.add_patch(polygon)
        
        # Настройка осей
        all_x = [x for x, _ in vertices]
        all_y = [y for _, y in vertices]
        margin = max(max(all_x) - min(all_x), max(all_y) - min(all_y)) * 0.2
        
        self.ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        self.ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        
        # Добавление сетки
        self.ax.grid(True, linestyle='--', alpha=0.3)
        
        # Добавление осей координат
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        
        # Добавление заголовка
        if title:
            self.ax.set_title(title)
    
    def add_text(self, text: str, x: float, y: float) -> None:
        """
        Добавление текста на график.
        
        Args:
            text (str): Текст для добавления
            x (float): X-координата
            y (float): Y-координата
        """
        self.ax.text(x, y, text, ha='center', va='center')
    
    def save(self, filename: str = None) -> str:
        """
        Сохранение графика в файл в домашней директории пользователя.
        
        Args:
            filename (str, optional): Имя файла. По умолчанию None.
            
        Returns:
            str: Путь к сохраненному файлу
        """
        if filename is None:
            # Создаем имя файла на основе текущей даты и времени
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shape_{timestamp}.png"
        
        # Используем домашнюю директорию пользователя
        home_dir = str(Path.home())
        output_dir = os.path.join(home_dir, 'shapes_output')
        
        # Создаем директорию в домашней папке пользователя, если её нет
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        try:
            self.fig.savefig(filepath)
            return filepath
        except Exception as e:
            raise IOError(f"Ошибка при сохранении файла: {e}")
    
    def show(self) -> None:
        """Отображение графика"""
        plt.show()
    
    def close(self) -> None:
        """Закрытие окна с графиком"""
        plt.close(self.fig) 