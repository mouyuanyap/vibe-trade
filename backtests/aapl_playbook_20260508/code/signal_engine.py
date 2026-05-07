import numpy as np
import pandas as pd
from typing import Dict

class SignalEngine:
    def generate(self, data_map: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]:
        results = {}
        for code, df in data_map.items():
            close = df["close"]
            signal = self._earnings_drift(close)
            results[code] = signal
        return results

    def _earnings_drift(self, close):
        earnings_dates = [
            "2024-08-01", "2024-10-31", "2025-01-30",
            "2025-05-01", "2025-07-31", "2025-10-30",
            "2026-01-29", "2026-04-30"
        ]

        signal = pd.Series(0.0, index=close.index)
        idx = pd.DatetimeIndex(close.index)

        for ed in earnings_dates:
            ed_dt = pd.Timestamp(ed)
            if ed_dt < idx.min() or ed_dt > idx.max():
                continue
            pre_dates = idx[(idx >= ed_dt - pd.Timedelta(days=10)) & (idx < ed_dt)]
            post_dates = idx[(idx > ed_dt) & (idx <= ed_dt + pd.Timedelta(days=4))]
            for i in pre_dates:
                if i in signal.index:
                    signal.loc[i] = 1.0
            for i in post_dates:
                if i in signal.index:
                    signal.loc[i] = -1.0

        return signal.fillna(0.0)
