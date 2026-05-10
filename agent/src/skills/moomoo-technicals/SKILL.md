---
name: moomoo-technicals
description: >
  Calculate technical indicators (EMA, SMA, MACD, RSI, etc.) for US/HK stocks using
  moomoo OpenD API data. This skill encapsulates a critical finding: the default
  forward-rehab adjustment in moomoo's get_kline distorts historical prices (making them
  useless for indicator calculation). Always use --rehab none when fetching kline data
  for technical analysis. Use this skill whenever the user asks for EMA, moving averages,
  or any technical indicator on a stock.
---

# Moomoo Technical Indicators

Calculate technical indicators using raw (unadjusted) OHLCV data from the moomoo OpenD API.

## Critical: Rehab Adjustment Warning

**The default `--rehab forward` (AuType.QFQ) adjustment in moomoo's kline API severely
distorts historical prices.** It can turn a $215 close into ~$173, rendering
all technical indicators wrong.

### Evidence (NVDA, 2026-05-08)

| Rehab Mode | Close Price | Correct? |
|------------|------------|----------|
| `--rehab forward` (default) | 173.71 | Wrong |
| `--rehab none` | 215.20 | Correct (matches snapshot) |

### Rule

**Always pass `--rehab none` when fetching kline data for technical indicators.**
Never rely on the default forward adjustment. Verify the latest close against
`get_snapshot.py` if in doubt.

## Script Paths

All scripts live under the moomoo skill base directory. Check both locations:

```
skills/moomooapi/scripts/quote/get_kline.py
~/.claude/skills/moomooapi/scripts/quote/get_kline.py
~/.claude/skills/moomooapi/scripts/quote/get_snapshot.py
```

## Fetching Data

**Important:** The `get_kline.py` script prints a log line to stdout before the JSON.
Always filter with `grep` before piping to Python:

```bash
# Correct: filter out the log line, then parse JSON
python ~/.claude/skills/moomooapi/scripts/quote/get_kline.py US.NVDA \
  --ktype 1d --num 200 --rehab none --json 2>&1 \
  | grep '^{"code"' | python3 -c "..."

# Wrong: will fail with JSONDecodeError "Extra data"
python ~/.claude/skills/moomooapi/scripts/quote/get_kline.py US.NVDA \
  --ktype 1d --num 200 --rehab none --json | python3 -c "..."
```

For EMA 60 you need at least 120 bars; 200 is a safe default.

## Timeframes

| `--ktype` | Description | Use case |
|-----------|------------|----------|
| `1d` | Daily bars | Short-term (days to weeks) |
| `1w` | Weekly bars | Medium-term (weeks to months) |

Always compare daily and weekly readings — alignment across timeframes gives stronger signals.

## Calculating Indicators (full working code)

After fetching kline data with `--rehab none --json`, pipe through `grep '^{"code"'` and then:

```python
import json, sys

data = json.load(sys.stdin)
closes = [bar['close'] for bar in data['data']]

# --- EMA ---
def ema(series, period):
    k = 2 / (period + 1)
    out = [series[0]]
    for v in series[1:]:
        out.append(v * k + out[-1] * (1 - k))
    return out

# --- RSI(14) with Wilder's smoothing ---
period = 14
gains, losses = [], []
for i in range(1, len(closes)):
    diff = closes[i] - closes[i-1]
    gains.append(diff if diff > 0 else 0)
    losses.append(abs(diff) if diff < 0 else 0)

avg_gain = sum(gains[:period]) / period
avg_loss = sum(losses[:period]) / period

rsi_values = []
for i in range(period, len(gains)):
    avg_gain = (avg_gain * (period - 1) + gains[i]) / period
    avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        rsi_values.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi_values.append(100.0 - (100.0 / (1.0 + rs)))

# --- MACD: EMA12 - EMA26, Signal: EMA9 of MACD ---
ema12 = ema(closes, 12)
ema26 = ema(closes, 26)
macd_line = [ema12[i] - ema26[i] for i in range(len(closes))]
signal_line = ema(macd_line, 9)
histogram = [macd_line[i] - signal_line[i] for i in range(len(macd_line))]

# Latest values
print(f'RSI(14):  {rsi_values[-1]:.1f}')
print(f'MACD:     {macd_line[-1]:.2f}')
print(f'Signal:   {signal_line[-1]:.2f}')
print(f'Histogram:{histogram[-1]:.2f}')
```

## Interpreting Signals

**RSI:**
- RSI > 70 → Overbought (potential pullback)
- RSI < 30 → Oversold (potential bounce)
- RSI 50–70 → Uptrend confirmation
- RSI 30–50 → Downtrend confirmation

**MACD:**
- Histogram flips from negative to positive → **Bullish cross** (buy signal)
- Histogram flips from positive to negative → **Bearish cross** (sell signal)
- MACD above signal, histogram expanding → Trend strengthening
- MACD above signal, histogram shrinking → Momentum fading

## Standard Workflow

1. **Fetch kline** with `--rehab none --num 200 --json` (daily) and `--ktype 1w --num 100` (weekly)
2. **Filter** through `grep '^{"code"'` before piping to Python
3. **Verify** the latest close against `get_snapshot.py --json` of the same ticker
4. **Calculate** indicators on both daily and weekly closes
5. **Compare** timeframes — alignment confirms signal strength
6. **Report** indicator values with interpretation
