import numpy as np
import pandas as pd
from typing import Dict

class SignalEngine:
    def __init__(self):
        self.rsi_period = 14
        self.rsi_oversold = 35
        self.rsi_overbought = 70
        self.stop_loss_pct = 0.03

    def generate(self, data_map: Dict[str, pd.DataFrame]) -> Dict[str, pd.Series]:
        signals = {}
        for code, df in data_map.items():
            close = df['close']
            signal = pd.Series(0.0, index=df.index)
            delta = close.diff()
            gain = delta.where(delta > 0, 0.0)
            loss = (-delta).where(delta < 0, 0.0)
            avg_gain = gain.ewm(alpha=1/self.rsi_period, adjust=False).mean()
            avg_loss = loss.ewm(alpha=1/self.rsi_period, adjust=False).mean()
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))
            position = 0.0
            entry_price = 0.0
            for i in range(1, len(close)):
                if position == 0.0:
                    if rsi.iloc[i] < self.rsi_oversold and not np.isnan(rsi.iloc[i]):
                        signal.iloc[i] = 1.0
                        position = 1.0
                        entry_price = close.iloc[i]
                else:
                    exit_signal = False
                    if rsi.iloc[i] > self.rsi_overbought:
                        exit_signal = True
                    if (close.iloc[i] - entry_price) / entry_price < -self.stop_loss_pct:
                        exit_signal = True
                    if exit_signal:
                        signal.iloc[i] = -1.0
                        position = 0.0
                        entry_price = 0.0
                    else:
                        signal.iloc[i] = 1.0
            signal = signal.fillna(0.0)
            signals[code] = signal
        return signals
