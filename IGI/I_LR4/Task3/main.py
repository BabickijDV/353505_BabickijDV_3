#Task3
#Lab Work 4: Object-Oriented Programming in Python
#Version: 1.0
#Developer: Бабицкий Дмитрий Валерьевич
#Date: 25.05.2025


#This program demonstrates object-oriented programming concepts by:
#1. Calculating the Taylor series expansion of ln(1+x)
#2. Comparing it with math library implementation
#3. Providing statistical analysis of the results
#4. Visualizing the data with matplotlib

from logarithmic_series import LogarithmicSeries
from visualizer import SeriesVisualizer
import os
import sys
from typing import Tuple, Optional

class UserInterface:
    """
    Класс для управления пользовательским интерфейсом.
    """
    
    def __init__(self):
        """Инициализация интерфейса"""
        self.series = None
        self.visualizer = SeriesVisualizer()
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_float_input(self, prompt: str, min_value: float, max_value: float) -> float:
        """
        Получение вещественного числа с проверкой диапазона.
        
        Args:
            prompt (str): Приглашение к вводу
            min_value (float): Минимальное значение
            max_value (float): Максимальное значение
            
        Returns:
            float: Введенное число
        """
        while True:
            try:
                value = float(input(prompt))
                if min_value <= value <= max_value:
                    return value
                print(f"Значение должно быть в диапазоне [{min_value}, {max_value}]")
            except ValueError:
                print("Пожалуйста, введите число")
    
    def get_int_input(self, prompt: str, min_value: int, max_value: int) -> int:
        """
        Получение целого числа с проверкой диапазона.
        
        Args:
            prompt (str): Приглашение к вводу
            min_value (int): Минимальное значение
            max_value (int): Максимальное значение
            
        Returns:
            int: Введенное число
        """
        while True:
            try:
                value = int(input(prompt))
                if min_value <= value <= max_value:
                    return value
                print(f"Значение должно быть в диапазоне [{min_value}, {max_value}]")
            except ValueError:
                print("Пожалуйста, введите целое число")
    
    def get_series_parameters(self) -> Tuple[float, float, int, int]:
        """
        Получение параметров для расчета ряда.
        
        Returns:
            Tuple[float, float, int, int]: Параметры (x_start, x_end, n_points, n_terms)
        """
        print("\nВведите параметры для расчета:")
        x_start = self.get_float_input("Начальное значение x (-0.99 до 0): ", -0.99, 0)
        x_end = self.get_float_input("Конечное значение x (0 до 0.99): ", 0, 0.99)
        n_points = self.get_int_input("Количество точек (10-1000): ", 10, 1000)
        n_terms = self.get_int_input("Количество членов ряда (1-100): ", 1, 100)
        return x_start, x_end, n_points, n_terms
    
    def calculate_and_show(self):
        """Расчет и отображение результатов"""
        try:
            if self.series is None:
                params = self.get_series_parameters()
                self.series = LogarithmicSeries(*params)
            
            # Получаем значения
            x_values = self.series.x_values
            series_values = self.series.get_series_values()
            function_values = self.series.get_function_values()
            
            # Выводим таблицу значений
            print("\nТаблица значений:")
            print("-" * 60)
            print(f"{'x':>10} | {'F(x)':>12} | {'n':>3} | {'Math F(x)':>12}")
            print("-" * 60)
            for x, fx, mfx in zip(x_values, series_values, function_values):
                print(f"{x:10.4f} | {fx:12.6f} | {self.series.n_terms:3d} | {mfx:12.6f}")
            print("-" * 60)
            
            # Выводим статистику
            print("\nСтатистические характеристики:")
            for name, value in self.series.get_statistics().items():
                print(f"{name}: {value:.6f}")
            
            # Строим график
            self.visualizer.create_plot()
            self.visualizer.plot_series(x_values, series_values, function_values, self.series.n_terms)
            
            # Сохраняем график
            filename = self.visualizer.save_plot()
            print(f"\nГрафик сохранен в файл: {filename}")
            
            # Показываем график
            self.visualizer.display_plot()
            
        except Exception as e:
            print(f"\nОшибка при расчете: {e}")
    
    def change_parameters(self):
        """Изменение параметров расчета"""
        try:
            params = self.get_series_parameters()
            self.series = LogarithmicSeries(*params)
            print("\nПараметры успешно обновлены")
        except Exception as e:
            print(f"\nОшибка при изменении параметров: {e}")
    
    def display_menu(self):
        """Отображение главного меню"""
        print("\n=== Разложение ln(1+x) в ряд ===")
        print("1. Рассчитать и показать результаты")
        print("2. Изменить параметры")
        print("3. Выход")
    
    def run(self):
        """Основной цикл программы"""
        while True:
            try:
                self.clear_screen()
                self.display_menu()
                choice = self.get_int_input("\nВыберите действие (1-3): ", 1, 3)
                
                if choice == 1:
                    self.calculate_and_show()
                elif choice == 2:
                    self.change_parameters()
                else:
                    print("\nСпасибо за использование программы!")
                    break
                
                input("\nНажмите Enter для продолжения...")
                
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем")
                sys.exit(0)
            except Exception as e:
                print(f"\nПроизошла неожиданная ошибка: {e}")
                input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()