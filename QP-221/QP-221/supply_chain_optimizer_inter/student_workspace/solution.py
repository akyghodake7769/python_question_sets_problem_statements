import pandas as pd

class WarehouseManager:
    def __init__(self):
        self.df_stock = None
        self.df_logs = None

    def load_data(self, stock_path: str, logs_path: str):
        self.df_stock = pd.read_csv(stock_path)
        self.df_logs = pd.read_csv(logs_path)

    def get_merged_data(self) -> pd.DataFrame:
        if self.df_stock is None or self.df_logs is None: return pd.DataFrame()
        return pd.merge(self.df_stock, self.df_logs, on=['SKU', 'Warehouse_ID'], how='inner')

class SupplyOptimizer:
    def get_at_risk_skus(self, df_stock: pd.DataFrame) -> list:
        # Filter where Stock < Safety
        at_risk = df_stock[df_stock['Stock'] < df_stock['Safety']]
        return sorted(at_risk['SKU'].unique().tolist())

    def calc_mean_lead_time(self, df_logs: pd.DataFrame) -> float:
        df = df_logs.copy()
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
        df['lead_time'] = (df['Delivery_Date'] - df['Order_Date']).dt.days
        return round(float(df['lead_time'].mean()), 1)

    def total_inventory_value(self, df_stock: pd.DataFrame) -> float:
        return float((df_stock['Stock'] * df_stock['Cost']).sum())

    def carrier_return_rate(self, df_logs: pd.DataFrame) -> dict:
        # {Carrier: % of status == 'Returned'}
        total = df_logs.groupby('Carrier').size()
        returned = df_logs[df_logs['Status'] == 'Returned'].groupby('Carrier').size()
        rate = (returned / total * 100).fillna(0)
        return rate.to_dict()

    def generate_summary(self, df_stock: pd.DataFrame, df_logs: pd.DataFrame) -> dict:
        # total_skus, critical_count (at risk), top_carrier (lowest return rate)
        # at_risk = self.get_at_risk_skus(df_stock)
        # rates = self.carrier_return_rate(df_logs)
        # best_carrier = min(rates, key=rates.get) if rates else "N/A"
        # return {
        #     'total_skus': int(df_stock['SKU'].nunique()),
        #     'critical_count': int(len(at_risk)),
        #     'best_carrier': best_carrier
        # }
        pass
