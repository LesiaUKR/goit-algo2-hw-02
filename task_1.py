from typing import List, Dict
from dataclasses import dataclass
from colorama import Fore, Style, init

# Ініціалізація colorama для кольорового виведення в консоль
init(autoreset=True)


@dataclass
class PrintJob:
    """
    Represents a print job with its attributes.

    Attributes:
        id (str): Unique identifier for the print job.
        volume (float): Volume of the model in cm³.
        priority (int): Priority of the print job (1, 2, or 3).
        print_time (int): Time required to print the model in minutes.
    """
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    """
    Represents the constraints of the 3D printer.

    Attributes:
        max_volume (float): Maximum volume the printer can handle in cm³.
        max_items (int): Maximum number of items the printer can handle simultaneously.
    """
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes the 3D printing queue based on job priorities and printer constraints.

    Args:
        print_jobs (List[Dict]): List of print jobs.
        constraints (Dict): Printer constraints including max volume and max items.

    Returns:
        Dict: A dictionary containing the optimized print order and total printing time.
    """
    # Конвертуємо список словників у список об'єктів PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]

    # Сортуємо завдання за пріоритетом (1 - найвищий, 3 - найнижчий)
    jobs.sort(key=lambda x: x.priority)

    # Ініціалізуємо змінні для зберігання результату
    print_order = []
    total_time = 0
    current_volume = 0
    current_items = 0
    current_batch = []

    for job in jobs:
        # Перевіряємо, чи можна додати поточне завдання до поточної групи
        if (current_volume + job.volume <= constraints["max_volume"] and
                current_items + 1 <= constraints["max_items"]):
            current_batch.append(job)
            current_volume += job.volume
            current_items += 1
        else:
            # Якщо група заповнена, додаємо її до результату
            if current_batch:
                # Час групи - це максимальний час серед завдань у групі
                batch_time = max(job.print_time for job in current_batch)
                total_time += batch_time
                print_order.extend([job.id for job in current_batch])
                # Очищуємо поточну групу
                current_batch = [job]
                current_volume = job.volume
                current_items = 1

    # Додаємо останню групу, якщо вона існує
    if current_batch:
        batch_time = max(job.print_time for job in current_batch)
        total_time += batch_time
        print_order.extend([job.id for job in current_batch])

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    """
    Tests the optimize_printing function with different scenarios.
    """
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
        # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    # Виведення результатів тестів з кольоровим форматуванням
    print(Fore.GREEN + "Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(Fore.YELLOW + f"Порядок друку: {result1['print_order']}")
    print(Fore.YELLOW + f"Загальний час: {result1['total_time']} хвилин")

    print(Fore.GREEN + "\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(Fore.YELLOW + f"Порядок друку: {result2['print_order']}")
    print(Fore.YELLOW + f"Загальний час: {result2['total_time']} хвилин")

    print(Fore.GREEN + "\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(Fore.YELLOW + f"Порядок друку: {result3['print_order']}")
    print(Fore.YELLOW + f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()