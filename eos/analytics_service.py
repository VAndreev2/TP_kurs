# analytics_service.py

import pandas as pd
from typing import List, Dict

class AnalyticsService:
    def __init__(self, data: List[Dict]):
        self.data = data
        self.df = pd.DataFrame(data)

    def calculate_statistics(self, column_name: str) -> Dict:
        if column_name not in self.df.columns:
            raise ValueError(f"Колонка '{column_name}' не обнаружена.")

        statistics = {}
        statistics['sum'] = self.df[column_name].sum()
        statistics['mean'] = self.df[column_name].mean()
        statistics['median'] = self.df[column_name].median()
        statistics['max'] = self.df[column_name].max()
        statistics['min'] = self.df[column_name].min()

        return statistics