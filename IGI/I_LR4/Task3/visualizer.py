import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional
import os
from datetime import datetime

class SeriesVisualizer:
    """
    Класс для визуализации результатов вычислений рядов.
    """
    
    def __init__(self):
        """Инициализация визуализатора"""
        self.fig = None
        self.ax = None
    
    def create_plot(self, title: str = "График функции и её разложения в ряд"):
        """
        Создает новый график.
        
        Args:
            title (str): Заголовок графика
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title(title)
        self.ax.grid(True)
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    def plot_series(self, x_values: np.ndarray, series_values: np.ndarray, 
                   function_values: np.ndarray, n_terms: int):
        """
        Отображает график ряда и функции.
        
        Args:
            x_values (np.ndarray): Значения аргумента
            series_values (np.ndarray): Значения ряда
            function_values (np.ndarray): Значения функции
            n_terms (int): Количество членов ряда
        """
        if self.ax is None:
            self.create_plot()
        
        # График ряда
        series_line, = self.ax.plot(x_values, series_values, 'b-', 
                                  label=f'Ряд (n={n_terms})')
        
        # График функции
        func_line, = self.ax.plot(x_values, function_values, 'r--', 
                                label='ln(1+x)')
        
        # Добавляем подписи
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.legend()
        
        # Добавляем аннотацию с информацией о точности
        max_error = np.max(np.abs(series_values - function_values))
        self.ax.annotate(f'Максимальная погрешность: {max_error:.2e}',
                        xy=(0.02, 0.95), xycoords='axes fraction',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def save_plot(self, filename: Optional[str] = None) -> str:
        """
        Сохраняет график в файл.
        
        Args:
            filename (Optional[str]): Имя файла. Если не указано, 
                                    генерируется автоматически.
        
        Returns:
            str: Путь к сохраненному файлу
        """
        if self.fig is None:
            raise ValueError("График не создан")
            
        try:
            # Создаем директорию plots в текущей папке скрипта
            plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
            os.makedirs(plots_dir, exist_ok=True)
            
            if filename is None:
                # Генерируем имя файла с временной меткой
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(plots_dir, f'plot_{timestamp}.png')
            else:
                # Если указано имя файла, добавляем к нему путь к директории plots
                filename = os.path.join(plots_dir, os.path.basename(filename))
            
            # Сохраняем график с высоким разрешением
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close(self.fig)
            return filename
            
        except Exception as e:
            raise ValueError(f"Не удалось сохранить график: {e}")
    
    def display_plot(self):
        """Отображает график"""
        if self.fig is None:
            raise ValueError("График не создан")
        plt.show()
    
    def clear(self):
        """Очищает текущий график"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None 