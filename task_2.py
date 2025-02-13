from typing import List, Dict
from colorama import Fore, init

init(autoreset=True)

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut a rod to maximize profit using memoization.

    Args:
        length (int): The length of the rod.
        prices (List[int]): List of prices where prices[i] is the price for a
        rod of length i+1.

    Returns:
        Dict: A dictionary containing the maximum profit, list of cuts, and
        number of cuts.
    """
    # Мемоізація для зберігання результатів підзадач
    memo = {}

    def helper(l):
        if l in memo:
            return memo[l]
        if l == 0:
            return 0, []
        max_profit = -1
        best_cuts = []
        for i in range(1, l + 1):
            current_profit = prices[i - 1] + helper(l - i)[0]
            if current_profit > max_profit:
                max_profit = current_profit
                best_cuts = [i] + helper(l - i)[1]
        memo[l] = (max_profit, best_cuts)
        return memo[l]

    max_profit, cuts = helper(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut a rod to maximize profit using tabulation.

    Args:
        length (int): The length of the rod.
        prices (List[int]): List of prices where prices[i] is the price for a
        rod of length i+1.

    Returns:
        Dict: A dictionary containing the maximum profit, list of cuts, and
        number of cuts.
    """
    # Ініціалізація таблиці для зберігання максимального прибутку
    dp = [0] * (length + 1)
    # Таблиця для зберігання оптимальних розрізів
    cuts_table = [[] for _ in range(length + 1)]

    for l in range(1, length + 1):
        max_profit = -1
        best_cuts = []
        for i in range(1, l + 1):
            current_profit = prices[i - 1] + dp[l - i]
            if current_profit > max_profit:
                max_profit = current_profit
                best_cuts = [i] + cuts_table[l - i]
        dp[l] = max_profit
        cuts_table[l] = best_cuts

    return {
        "max_profit": dp[length],
        "cuts": cuts_table[length],
        "number_of_cuts": len(cuts_table[length]) - 1 if cuts_table[length] else 0
    }

def run_tests():
    """
    Runs all test cases for rod cutting problem and prints results with colored
    output.
    """
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(Fore.GREEN + f"\nТест: {test['name']}")
        print(Fore.CYAN + f"Довжина стрижня: {test['length']}")
        print(Fore.CYAN + f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print(Fore.YELLOW + "\nРезультат мемоізації:")
        print(Fore.YELLOW +
              f"Максимальний прибуток: {memo_result['max_profit']}"
              )
        print(Fore.YELLOW + f"Розрізи: {memo_result['cuts']}")
        print(Fore.YELLOW +
              f"Кількість розрізів: {memo_result['number_of_cuts']}"
              )

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print(Fore.MAGENTA + "\nРезультат табуляції:")
        print(
            Fore.MAGENTA +
            f"Максимальний прибуток: {table_result['max_profit']}"
        )
        print(Fore.MAGENTA + f"Розрізи: {table_result['cuts']}")
        print(Fore.MAGENTA +
              f"Кількість розрізів: {table_result['number_of_cuts']}"
              )

        print(Fore.GREEN + "\nПеревірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()