import pandas as pd
import sys

class PortfolioAnalyzer:
    def __init__(self):
        self.df = None

    def load_portfolio(self, csv_path: str):
        # Implementation here
        pass

    def calculate_metrics(self):
        # Implementation here
        pass

    def get_total_market_value(self) -> float:
        # Implementation here
        return 0.0

    def get_top_performer(self) -> str:
        # Implementation here
        return ""

    def get_underperforming_assets(self, threshold_pct: float) -> list:
        # Implementation here
        return []

    def apply_sector_mapping(self, sector_csv: str):
        # Implementation here
        pass

# Note: Don't make changes in below code.
if __name__ == "__main__":
    # Command processor for standardized evaluation
    analyzer = PortfolioAnalyzer()
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "LOAD": analyzer.load_portfolio(parts[1])
        elif cmd == "CALC": analyzer.calculate_metrics()
        elif cmd == "TOTAL":
            val = analyzer.get_total_market_value()
            print(f"Total Value: {val:.1f}")
        elif cmd == "TOP": print(f"Top: {analyzer.get_top_performer()}")
        elif cmd == "UNDER": print(f"Under: {', '.join(analyzer.get_underperforming_assets(float(parts[1])))}")
        elif cmd == "SECTOR": analyzer.apply_sector_mapping(parts[1])
        elif cmd == "SHOW": print(analyzer.df[['symbol', 'gain_loss_pct', 'sector']].to_string(index=False))
