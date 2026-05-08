import pandas as pd
import numpy as np
from typing import Dict

class SignalEngine:
    def generate(self, data_map: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]:
        signals = {}
        for code, df in data_map.items():
            close = df["close"]
            volume = df["volume"]
            delta = close.diff()
            gain = delta.where(delta > 0, 0.0)
            loss = (-delta).where(delta < 0, 0.0)
            avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
            avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
            rs = avg_gain / avg_loss.replace(0, np.nan)
            rsi = 100.0 - (100.0 / (1.0 + rs))
            signal_a = pd.Series(0.0, index=df.index)
            signal_a[rsi < 35] = 1.0
            signal_a[rsi > 70] = -1.0
            ema20 = close.ewm(span=20, adjust=False).mean()
            ema50 = close.ewm(span=50, adjust=False).mean()
            vol_ma20 = volume.rolling(20).mean()
            signal_b = pd.Series(0.0, index=df.index)
            high_vol = volume > vol_ma20
            signal_b[(ema20 > ema50) & high_vol] = 1.0
            signal_b[(ema20 < ema50) & high_vol] = -1.0
            earnings_dates = [
                "2024-06-12", "2024-09-05", "2024-12-12",
                "2025-03-06", "2025-06-12", "2025-09-04",
                "2025-12-11", "2026-03-04"
            ]
            signal_c = pd.Series(0.0, index=df.index)
            for ed in earnings_dates:
                ed_ts = pd.Timestamp(ed)
                if ed_ts in df.index:
                    idx_loc = df.index.get_loc(ed_ts)
                    entry_idx = max(0, idx_loc - 5)
                    exit_idx = min(len(df) - 1, idx_loc + 2)
                    signal_c.iloc[entry_idx:exit_idx] = 1.0
            combined = (signal_a.fillna(0) + signal_b.fillna(0) + signal_c.fillna(0)) / 3.0
            combined = combined.clip(-1.0, 1.0)
            signals[code] = combined
        return signals
