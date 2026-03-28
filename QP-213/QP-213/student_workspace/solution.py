# import pandas as pd

# class SalesTracker:
#     def __init__(self):
#         # TODO: Initialize self.df_sales and self.df_reviews
#         pass

#     def load_csvs(self, sales_path: str, reviews_path: str):
#         # TODO: Load CSVs into DataFrames
#         pass

#     def get_top_sellers(self, min_units: int) -> pd.DataFrame:
#         # TODO: Filter rows where Units_Sold >= min_units
#         return pd.DataFrame()

#     def category_price_analysis(self) -> pd.Series:
#         # TODO: Group by Category and return mean Unit_Price
#         return pd.Series()

# class SentimentAnalyzer:
#     def aggregate_reviews(self, df_reviews: pd.DataFrame) -> pd.DataFrame:
#         # TODO: Group by Product_ID and return mean Rating
#         return pd.DataFrame()

#     def get_correlation_summary(self, df_sales: pd.DataFrame, df_reviews: pd.DataFrame) -> pd.DataFrame:
#         # TODO: Merge sales with aggregated reviews
#         return pd.DataFrame()

#     def discount_performance(self, df_sales: pd.DataFrame) -> dict:
#         # TODO: Return avg sales for discounted vs non-discounted items
#         return {}

#     def detect_opportunities(self, df_merged: pd.DataFrame) -> list:
#         # TODO: Identify Product_IDs where Rating > 4.0 and Sales < Median
#         return []
