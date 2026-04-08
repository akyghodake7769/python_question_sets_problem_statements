# from typing import List, Generator, Tuple, Callable
# from functools import wraps

# # Complete the 'generate_trading_report' function below.
# #
# # The function is expected to return a LIST_OF_STRINGS.
# # The function accepts INTEGER_ARRAY prices as parameter.
# #
# # You must implement:
# # 1. A decorator 'validate_prices' to validate input
# # 2. A generator function 'find_transactions' that yields transaction tuples
# # 3. The main function 'generate_trading_report' that formats the output

# def validate_prices(func: Callable) -> Callable:
#     """Decorator to validate price data"""
#     @wraps(func)
#     def wrapper(prices: List[int]) -> Generator[Tuple[int, int, int, int, int], None, None]:
#         # Add validation logic here
#         return func(prices)
#     return wrapper

# @validate_prices
# def find_transactions(prices: List[int]) -> Generator[Tuple[int, int, int, int, int], None, None]:
#     """Generator that yields (buy_day, buy_price, sell_day, sell_price, profit)"""
#     pass

# def generate_trading_report(prices: List[int]) -> List[str]:
#     """Generate formatted trading report"""
#     pass

# if __name__ == '__main__':
#     try:
#         n = int(input().strip())
#         prices = list(map(int, input().strip().split()))

#         report = generate_trading_report(prices)

#         for line in report:
#             print(line)
#     except ValueError as e:
#         print(f"Error: {e}")
#     except Exception as e:
#         print(f"Unexpected Error: {e}")


from typing import List, Generator, Tuple, Callable
from functools import wraps

# Reference Solution for RT-01 Portfolio Trading Optimizer

def validate_prices(func: Callable) -> Callable:
    """Decorator to validate price data"""
    @wraps(func)
    def wrapper(prices: List[int]) -> Generator[Tuple[int, int, int, int, int], None, None]:
        if any(p < 0 for p in prices):
            raise ValueError("prices must be non-negative")
        return func(prices)
    return wrapper

@validate_prices
def find_transactions(prices: List[int]) -> Generator[Tuple[int, int, int, int, int], None, None]:
    """Generator that yields (buy_day, buy_price, sell_day, sell_price, profit)"""
    if not prices:
        return
    
    i = 0
    n = len(prices)
    while i < n - 1:
        # Find local minimum
        while i < n - 1 and prices[i] >= prices[i+1]:
            i += 1
        if i == n - 1:
            break
        buy_day = i
        buy_price = prices[i]
        
        # Find local maximum
        i += 1
        while i < n - 1 and prices[i] <= prices[i+1]:
            i += 1
        sell_day = i
        sell_price = prices[i]
        
        profit = sell_price - buy_price
        yield (buy_day, buy_price, sell_day, sell_price, profit)

def generate_trading_report(prices: List[int]) -> List[str]:
    """Generate formatted trading report"""
    report = []
    total_profit = 0
    
    for buy_day, buy_price, sell_day, sell_price, profit in find_transactions(prices):
        total_profit += profit
        report.append(f"buy_day={buy_day} buy_price={buy_price} sell_day={sell_day} sell_price={sell_price} profit={profit}")
        
    report.append(f"total_profit={total_profit}")
    return report

# if __name__ == '__main__':
#     try:
#         # Standard HackerRank input reading
#         line1 = input().strip()
#         if not line1:
#             sys.exit(0)
#         n = int(line1)
        
#         line2 = input().strip()
#         prices = list(map(int, line2.split()))

#         report = generate_trading_report(prices)

#         for line in report:
#             print(line)
#     except EOFError:
#         pass
#     except ValueError as e:
#         print(f"Error: {e}")
#     except Exception as e:
#         print(f"Unexpected Error: {e}")
if __name__ == '__main__':
    n = int(input().strip())
    prices = list(map(int, input().strip().split()))
    
    report = generate_trading_report(prices)
    
    for line in report:
        print(line)