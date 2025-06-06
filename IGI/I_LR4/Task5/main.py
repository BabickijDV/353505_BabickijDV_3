#Task5
#Lab Work 4: Object-Oriented Programming in Python
#Version: 1.0
#Developer: Бабицкий Дмитрий Валерьевич
#Date: 26.05.2025

from random_matrix import RandomMatrix
from typing import Tuple, Optional

def get_int_input(prompt: str, min_val: int = 1) -> int:
    """
    Получение целочисленного ввода от пользователя с проверкой.
    
    Args:
        prompt (str): Приглашение к вводу
        min_val (int): Минимальное допустимое значение
        
    Returns:
        int: Введенное число
        
    Raises:
        ValueError: Если введено не целое число или число меньше min_val
    """
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"Значение должно быть не меньше {min_val}!")
                continue
            return value
        except ValueError:
            print("Пожалуйста, введите целое число!")

def get_matrix_params() -> Tuple[int, int, int, int]:
    """
    Получение параметров матрицы от пользователя.
    
    Returns:
        Tuple[int, int, int, int]: кортеж (строки, столбцы, мин_значение, макс_значение)
    """
    print("\nВвод параметров матрицы:")
    rows = get_int_input("Введите количество строк: ")
    cols = get_int_input("Введите количество столбцов: ")
    
    print("\nВвод диапазона значений:")
    while True:
        min_val = get_int_input("Введите минимальное значение: ", min_val=-1000)
        max_val = get_int_input("Введите максимальное значение: ", min_val=-1000)
        if min_val < max_val:
            break
        print("Минимальное значение должно быть меньше максимального!")
    
    return rows, cols, min_val, max_val

def print_matrix_stats(matrix: RandomMatrix) -> None:
    """
    Вывод статистической информации о матрице.
    
    Args:
        matrix (RandomMatrix): Матрица для анализа
    """
    print("\nСтатистическая информация:")
    print(f"Среднее значение: {matrix.mean():.2f}")
    print(f"Медиана: {matrix.median():.2f}")
    print(f"Дисперсия: {matrix.var():.2f}")
    print(f"Стандартное отклонение: {matrix.std():.2f}")
    
    # Поиск минимальной суммы строки
    min_row_idx, min_sum = matrix.min_row_sum()
    print(f"\nМинимальная сумма элементов: {min_sum:.2f} (строка {min_row_idx + 1})")
    
    # Вычисление корреляции между четными и нечетными элементами
    correlation = matrix.correlation_even_odd()
    print(f"Коэффициент корреляции между четными и нечетными элементами: {correlation:.4f}")

def demonstrate_matrix_operations(matrix: RandomMatrix) -> None:
    """
    Демонстрация операций с матрицей.
    
    Args:
        matrix (RandomMatrix): Матрица для демонстрации
    """
    print("\nДемонстрация операций с матрицей:")
    
    # Демонстрация индексирования
    if matrix.shape[0] > 0 and matrix.shape[1] > 0:
        print("\n1. Получение элемента по индексу:")
        try:
            element = matrix.get_element(0, 0)
            print(f"Первый элемент матрицы: {element}")
        except IndexError as e:
            print(f"Ошибка: {e}")
    
    # Демонстрация среза
    print("\n2. Получение среза матрицы:")
    try:
        # Получаем первые 2 строки и 2 столбца (если они есть)
        slice_rows = slice(0, min(2, matrix.shape[0]))
        slice_cols = slice(0, min(2, matrix.shape[1]))
        submatrix = matrix.get_slice(slice_rows, slice_cols)
        print("Срез матрицы (до 2x2):")
        print(submatrix)
    except Exception as e:
        print(f"Ошибка при получении среза: {e}")

def main():
    """Основная функция программы"""
    while True:
        try:
            # Получаем параметры матрицы
            rows, cols, min_val, max_val = get_matrix_params()
            
            # Создаем матрицу
            matrix = RandomMatrix(rows, cols, min_val, max_val)
            
            # Выводим матрицу
            print("\nСгенерированная матрица:")
            print(matrix)
            
            # Демонстрируем операции с матрицей
            demonstrate_matrix_operations(matrix)
            
            # Выводим статистику
            print_matrix_stats(matrix)
            
            # Спрашиваем о продолжении
            if input("\nХотите создать еще одну матрицу? (да/нет): ").lower() != 'да':
                break
                
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            if input("\nХотите попробовать снова? (да/нет): ").lower() != 'да':
                break
    
    print("\nСпасибо за использование программы!")

if __name__ == "__main__":
    main()