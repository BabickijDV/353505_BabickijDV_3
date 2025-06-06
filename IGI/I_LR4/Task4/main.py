#Task4
#Lab Work 4: Object-Oriented Programming in Python
#Version: 1.0
#Developer: Бабицкий Дмитрий Валерьевич
#Date: 26.05.2025

from trapezoid import IsoscelesTrapezoid
from visualizer import ShapeVisualizer
import sys
from typing import Tuple, Optional

def get_float_input(prompt: str) -> float:
    """
    Получение числового ввода от пользователя с проверкой.
    
    Args:
        prompt (str): Приглашение к вводу
        
    Returns:
        float: Введенное число
        
    Raises:
        ValueError: Если введено не число
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Значение должно быть положительным!")
                continue
            return value
        except ValueError:
            print("Пожалуйста, введите корректное число!")

def get_color_input() -> str:
    """
    Получение цвета от пользователя.
    
    Returns:
        str: Выбранный цвет
    """
    print("\nДоступные цвета:")
    colors = [
        'красный', 'синий', 'зеленый', 'желтый',
        'черный', 'белый', 'фиолетовый', 'оранжевый'
    ]
    
    for i, color in enumerate(colors, 1):
        print(f"{i}. {color}")
    
    while True:
        try:
            choice = int(input("\nВыберите номер цвета: "))
            if 1 <= choice <= len(colors):
                return colors[choice - 1]
            print(f"Пожалуйста, выберите число от 1 до {len(colors)}!")
        except ValueError:
            print("Пожалуйста, введите корректный номер!")

def get_trapezoid_params() -> Tuple[float, float, float, str]:
    """
    Получение параметров трапеции от пользователя.
    
    Returns:
        Tuple[float, float, float, str]: кортеж (нижнее основание, верхнее основание, высота, цвет)
    """
    print("\nВвод параметров трапеции:")
    while True:
        try:
            a = get_float_input("Введите длину нижнего основания (a): ")
            b = get_float_input("Введите длину верхнего основания (b): ")
            if b >= a:
                print("Верхнее основание должно быть меньше нижнего!")
                continue
            h = get_float_input("Введите высоту (h): ")
            color = get_color_input()
            return a, b, h, color
        except ValueError as e:
            print(f"Ошибка: {e}")

def get_text_input() -> Optional[str]:
    """
    Получение текста для подписи фигуры.
    
    Returns:
        Optional[str]: Текст подписи или None, если подпись не нужна
    """
    answer = input("\nХотите добавить текст на фигуру? (да/нет): ").lower()
    if answer == 'да':
        return input("Введите текст: ")
    return None

def main():
    """Основная функция программы"""
    while True:
        try:
            # Получаем параметры трапеции
            a, b, h, color = get_trapezoid_params()
            
            # Создаем трапецию
            trapezoid = IsoscelesTrapezoid(a, b, h, color)
            
            # Выводим информацию о трапеции
            print("\nИнформация о фигуре:")
            print(trapezoid)
            
            # Создаем визуализатор
            visualizer = ShapeVisualizer()
            
            # Получаем текст для подписи
            text = get_text_input()
            
            # Отрисовываем трапецию
            visualizer.draw_shape(
                trapezoid.get_vertices(),
                trapezoid.color_code,
                f"{trapezoid.name} ({trapezoid.color} цвета)"
            )
            
            # Добавляем текст, если он есть
            if text:
                visualizer.add_text(text, 0, 0)
            
            # Сохраняем изображение
            filepath = visualizer.save()
            print(f"\nИзображение сохранено в файл: {filepath}")
            
            # Показываем изображение
            visualizer.show()
            
            # Спрашиваем о продолжении
            if input("\nХотите создать еще одну фигуру? (да/нет): ").lower() != 'да':
                break
                
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            if input("\nХотите попробовать снова? (да/нет): ").lower() != 'да':
                break
        finally:
            # Закрываем окно с графиком
            visualizer.close()
    
    print("\nСпасибо за использование программы!")

if __name__ == "__main__":
    main()
