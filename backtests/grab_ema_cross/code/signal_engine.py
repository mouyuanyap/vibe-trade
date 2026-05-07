import numpy as np
import pandas as pd
from typing import Dict

class SignalEngine:
    def __init__(self):
        self.ema_fast = 20
        self.ema_slow = 50
        self.vol_ma_period = 20
        self.trailing_stop_pct = 0.05

    def generate(self, data_map: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]:
        signals = {}
        for code, df in data_map.items():
            close = df['close']
            volume = df['volume']
            signal = pd.Series(0.0, index=df.index)
            ema20 = close.ewm(span=self.ema_fast).mean()
            ema50 = close.ewm(span=self.ema_slow).mean()
            vol_ma = volume.rolling(self.vol_ma_period).mean()
            position = 0.0
            highest_since_entry = 0.0
            for i in range(1, len(close)):
                if position == 0.0:
                    bullish_cross = (ema20.iloc[i] > ema50.iloc[i] and ema20.iloc[i-1] <= ema50.iloc[i-1])
                    vol_confirm = volume.iloc[i] > vol_ma.iloc[i]
                    if bullish_cross and vol_confirm:
                        signal.iloc[i] = 1.0
                        position = 1.0
                        highest_since_entry = close.iloc[i]
                else:
                    highest_since_entry = max(highest_since_entry, close.iloc[i])
                    trailing_stop = highest_since_entry * (1 - self.trailing_stop_pct)
                    bearish_cross = (ema20.iloc[i] < ema50.iloc[i] and ema20.iloc[i-1] >= ema50.iloc[i-1])
                    if bearish_cross or close.iloc[i] < trailing_stop:
                        signal.iloc[i] = -1.0
                        position = 0.0
                        highest_since_entry = 0.0
                    else:
                        signal.iloc[i] = 1.0
            signal = signal.fillna(0.0)
            signals[code] = signal
        return signals
