import numpy as np
import pandas as pd
from typing import Dict

class SignalEngine:
    def __init__(self):
        self.pre_earnings_days = 5
        self.post_earnings_days = 2

    def generate(self, data_map: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]:
        signals = {}
        # NVDA earnings dates (approximate announcement dates)
        # Q4 FY2025: 2024-02-21, Q1 FY2026: 2024-05-22, Q2 FY2026: 2024-08-28
        # Q3 FY2026: 2024-11-20, Q4 FY2026: 2025-02-26, Q1 FY2027: 2025-05-28 (approx)
        earnings_dates = [
            "2024-02-21", "2024-05-22", "2024-08-28", "2024-11-20",
            "2025-02-26", "2025-05-28", "2025-08-27", "2025-11-19",
        ]
        earnings_dates = pd.to_datetime(earnings_dates)

        for code, df in data_map.items():
            signal = pd.Series(0.0, index=df.index)

            for ed in earnings_dates:
                # Find the nearest trading day before the earnings date
                valid_dates = df.index[df.index <= ed]
                if len(valid_dates) == 0:
                    continue

                entry_date = ed - pd.Timedelta(days=self.pre_earnings_days)
                exit_date = ed + pd.Timedelta(days=self.post_earnings_days)

                # Find actual trading days
                entry_mask = (df.index >= entry_date) & (df.index < ed)
                exit_mask = (df.index >= ed) & (df.index <= exit_date)

                # Find the exact trading day closest to entry_date
                entry_idx = df.index[df.index <= ed]
                entry_idx = entry_idx[-self.pre_earnings_days:] if len(entry_idx) >= self.pre_earnings_days else entry_idx

                if len(entry_idx) >= self.pre_earnings_days:
                    for i in range(len(entry_idx)):
                        if entry_idx[i] >= entry_date:
                            signal.loc[entry_idx[i]] = 1.0

                # Exit after earnings
                exit_idx = df.index[(df.index >= ed) & (df.index <= exit_date)]
                for ei in exit_idx:
                    signal.loc[ei] = -1.0 if signal.loc[ei] != 1.0 else 0.0

            signal = signal.fillna(0.0)
            signals[code] = signal
        return signals
