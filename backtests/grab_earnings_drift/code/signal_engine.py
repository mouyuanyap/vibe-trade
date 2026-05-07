import numpy as np
import pandas as pd
from typing import Dict

class SignalEngine:
    def __init__(self):
        self.pre_earnings_days = 5
        self.post_earnings_days = 2

    def generate(self, data_map: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]:
        signals = {}
        earnings_dates = [
            "2024-05-15", "2024-08-15", "2024-11-15",
            "2025-02-12", "2025-05-05", "2025-08-20", "2025-11-15",
        ]
        earnings_dates = pd.to_datetime(earnings_dates)
        for code, df in data_map.items():
            signal = pd.Series(0.0, index=df.index)
            for ed in earnings_dates:
                entry_date = ed - pd.Timedelta(days=self.pre_earnings_days)
                exit_date = ed + pd.Timedelta(days=self.post_earnings_days)
                entry_idx = df.index[(df.index >= entry_date) & (df.index < ed)]
                for ei in entry_idx:
                    signal.loc[ei] = 1.0
                exit_idx = df.index[(df.index >= ed) & (df.index <= exit_date)]
                for ei in exit_idx:
                    signal.loc[ei] = -1.0
            signal = signal.fillna(0.0)
            signals[code] = signal
        return signals
