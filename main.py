import timeit
import matplotlib.pyplot as plt
from typing import Callable, Dict, List


def gen_bin_tree_recursive(height: int, root: int, l_b: Callable[[int], int] = lambda x: x * 3,
                           r_b: Callable[[int], int] = lambda x: x - 4) -> Dict[int, List[Dict[int, List]]]:
    """
    Рекурсивная версия функции построения бинарного дерева.

    Эта функция строит бинарное дерево с заданной высотой и значением корня. Значения для левого и правого потомков вычисляются с использованием переданных
    функций. Если высота дерева равна нулю, то возвращается пустой лист.
    height (int): Высота дерева (количество уровней дерева).
    root (int): Значение, которое будет в корне дерева.
    l_b (Callable[[int], int]): Функция для вычисления левого потомка.
    r_b (Callable[[int], int]): Функция для вычисления правого потомка.
    dict: Возвращает словарь, где ключом является значение узла, а значением - список с левого и правого потомков.
    """
    if height == 0:
        return {root: []}

    left_leaf = gen_bin_tree_recursive(height - 1, l_b(root))
    right_leaf = gen_bin_tree_recursive(height - 1, r_b(root))

    return {
        root: [left_leaf, right_leaf]
    }


def gen_bin_tree_iterative(height: int, root: int, l_b: Callable[[int], int] = lambda x: x * 3,
                           r_b: Callable[[int], int] = lambda x: x - 4) -> List:
    """
    Нерекурсивная версия функции построения бинарного дерева с использованием очереди.

    Эта функция строит бинарное дерево с заданной высотой и значением корня. Значения для левого и правого потомков вычисляются с использованием переданных
    функций. Вместо рекурсии используется очередь для итеративного построения дерева.

    height (int): Высота дерева (количество уровней дерева).
    root (int): Значение, которое будет в корне дерева.
    l_b (Callable[[int], int]): Функция для вычисления левого потомка. По умолчанию умножает значение на 3.
    r_b (Callable[[int], int]): Функция для вычисления правого потомка. По умолчанию вычитает 4.
    list: Возвращает список, представляющий бинарное дерево, где каждый узел имеет структуру: [значение, левый потомок, правый потомок].
    """
    tree = [root]
    queue = [(root, height)]

    while queue:
        current, h = queue.pop(0)
        if h > 0:
            left = l_b(current)
            right = r_b(current)
            tree.append([left, [], []])
            tree.append([right, [], []])
            queue.append((left, h - 1))
            queue.append((right, h - 1))

    return tree


def benchmark(func: Callable, root: int, height: int, number: int = 1, repeat: int = 5) -> float:
    """
    Замер времени работы функции.

    Измеряет минимальное время выполнения функции с использованием timeit.repeat для нескольких повторений.
    Возвращает минимальное время выполнения функции.

    func (Callable): Функция, для которой замеряется время.
    root (int): Значение корня дерева, которое передается в функцию.
    height (int): Высота дерева, которое передается в функцию.
    number (int): Количество повторений функции для одного замера. По умолчанию 1.
    repeat (int): Количество замеров. По умолчанию 5.
    float: Минимальное время выполнения функции из нескольких замеров.
    """
    times = timeit.repeat(lambda: func(height, root), number=number, repeat=repeat)
    return min(times)


def main():
    """
    Основная функция для тестирования времени работы рекурсивной и нерекурсивной версии построения бинарного дерева.

    Функция замеряет время работы для деревьев с разной высотой и строит график для сравнения времени выполнения.

    """
    root = 7  # Значение корня дерева
    heights = range(1, 11)  # Высоты дерева от 1 до 10
    recursive_times = []
    iterative_times = []

    # Замеряем время для каждой высоты дерева
    for height in heights:
        recursive_times.append(benchmark(gen_bin_tree_recursive, root, height, repeat=5, number=1))
        iterative_times.append(benchmark(gen_bin_tree_iterative, root, height, repeat=5, number=1))

    # Строим график
    plt.plot(heights, recursive_times, label="Рекурсивный метод", color='blue')
    plt.plot(heights, iterative_times, label="Нерекурсивный метод", color='green')
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек.)")
    plt.title("Сравнение реализаций построения бинарного дерева")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
