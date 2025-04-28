"""
Модуль для работы с геометрическими фигурами.

Этот модуль предоставляет классы для работы с основными геометрическими фигурами:
- Circle (круг)
- Rectangle (прямоугольник)
- Triangle (треугольник)

Пример использования:
>>> circle = Circle(radius=5)
>>> print(f"Площадь круга: {circle.area():.2f}")
Площадь круга: 78.54
"""

import math
from typing import Union, Tuple


class Circle:
    """Класс для представления круга и вычисления его характеристик.

    Attributes:
        radius (float): Радиус круга. Должен быть положительным числом.
    """

    def __init__(self, radius: float):
        """Инициализирует круг с заданным радиусом.

        Args:
            radius: Радиус круга. Должен быть > 0.

        Raises:
            ValueError: Если радиус отрицательный или нулевой.
        """
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным числом")
        self.radius = radius

    def area(self) -> float:
        """Вычисляет площадь круга.

        Returns:
            Площадь круга по формуле πr².

        Example:
            >>> circle = Circle(radius=2)
            >>> circle.area()
            12.566370614359172
        """
        return math.pi * self.radius ** 2

    def circumference(self) -> float:
        """Вычисляет длину окружности.

        Returns:
            Длина окружности по формуле 2πr.
        """
        return 2 * math.pi * self.radius


class Rectangle:
    """Класс для представления прямоугольника.

    Attributes:
        length (float): Длина прямоугольника.
        width (float): Ширина прямоугольника.
    """

    def __init__(self, length: float, width: float):
        """Инициализирует прямоугольник с заданными длиной и шириной.

        Parameters
        ----------
        length : float
            Длина прямоугольника, должна быть > 0
        width : float
            Ширина прямоугольника, должна быть > 0

        Raises
        ------
        ValueError
            Если длина или ширина <= 0
        """
        if length <= 0 or width <= 0:
            raise ValueError("Длина и ширина должны быть положительными числами")
        self.length = length
        self.width = width

    def area(self) -> float:
        """Вычисляет площадь прямоугольника.

        Returns
        -------
        float
            Площадь прямоугольника (length * width)
        """
        return self.length * self.width

    def perimeter(self) -> float:
        """Вычисляет периметр прямоугольника.

        Returns
        -------
        float
            Периметр прямоугольника (2*(length + width))
        """
        return 2 * (self.length + self.width)

    def is_square(self) -> bool:
        """Проверяет, является ли прямоугольник квадратом.

        Returns
        -------
        bool
            True если длина равна ширине, иначе False
        """
        return self.length == self.width


class Triangle:
    """Класс для представления треугольника.

    Attributes
    ----------
    side_a : float
        Первая сторона треугольника
    side_b : float
        Вторая сторона треугольника
    side_c : float
        Третья сторона треугольника
    """

    def __init__(self, side_a: float, side_b: float, side_c: float):
        """Инициализирует треугольник с тремя сторонами.

        Args:
            side_a: Первая сторона треугольника
            side_b: Вторая сторона треугольника
            side_c: Третья сторона треугольника

        Raises:
            ValueError: Если стороны не могут образовать треугольник
        """
        sides = [side_a, side_b, side_c]
        if any(s <= 0 for s in sides):
            raise ValueError("Все стороны должны быть положительными числами")

        sides_sorted = sorted(sides)
        if sides_sorted[0] + sides_sorted[1] <= sides_sorted[2]:
            raise ValueError("Сумма любых двух сторон должна быть больше третьей")

        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self) -> float:
        """Вычисляет площадь треугольника по формуле Герона.

        Returns:
            Площадь треугольника.

        Example:
            >>> triangle = Triangle(3, 4, 5)
            >>> triangle.area()
            6.0
        """
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))

    def perimeter(self) -> float:
        """Вычисляет периметр треугольника.

        Returns:
            Сумма всех сторон треугольника.
        """
        return self.side_a + self.side_b + self.side_c

    def is_right(self) -> bool:
        """Проверяет, является ли треугольник прямоугольным.

        Returns:
            True если треугольник прямоугольный (a² + b² = c²)
        """
        sides = sorted([self.side_a, self.side_b, self.side_c])
        return math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2)


if __name__ == "__main__":
    try:
        circle = Circle(radius=5)
        print(f"Площадь круга: {circle.area():.2f}")

        rect = Rectangle(4, 5)
        print(f"Площадь прямоугольника: {rect.area()}")
        print(f"Это квадрат? {'Да' if rect.is_square() else 'Нет'}")

        triangle = Triangle(3, 4, 5)
        print(f"Площадь треугольника: {triangle.area()}")
        print(f"Это прямоугольный треугольник? {'Да' if triangle.is_right() else 'Нет'}")

    except ValueError as e:
        print(f"Ошибка: {e}")