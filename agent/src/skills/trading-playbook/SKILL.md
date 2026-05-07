---
name: trading-playbook
description: >
  Generates a comprehensive 30-day institutional-grade trading playbook for any stock
  combining fundamental analysis, multi-timeframe technical analysis, options flow intelligence,
  quantitative factor scoring, backtested trade setups, and a week-by-week action calendar.
  Use this skill whenever the user asks for a trading plan, playbook, or actionable strategy
  for a specific ticker over the next month — including requests for buy/sell signals, entry/exit levels,
  scenario analysis, or "what to do with {ticker}." Also trigger when the user asks for a
  "full analysis" of a stock or wants to maximize profit over a 30-day window. This skill
  orchestrates all relevant sub-skills (fundamentals, technicals, options, quant factors,
  backtest and produces a structured, print-ready report.
---

# 30-Day Trading Playbook

A multi-phase agentic pipeline that produces an institutional-grade trading playbook for
a user-specified ticker covering the next 30 calendar days. The output is a structured
report with a scorecard, key price levels map, scenario analysis, week-by-week calendar,
specific trade setups, risk event calendar, and a daily monitoring checklist.

**Required input:** The user must provide a ticker symbol (e.g. AAPL, 700.HK, 000001.SZ).
If the user has not specified a ticker, ask for it before starting the pipeline.

---

## Execution Pipeline

Work through each phase in order. Load each named skill before executing that phase.
Do not skip phases — every phase feeds the final synthesis.

Throughout all phases, replace `{ticker}` with the user-provided symbol and `{market}`
with the inferred market (US, HK, China-A, crypto) based on the symbol format.

---

### PHASE 1 · Data & Fundamentals

**Skills to load:** `yfinance`, `data-routing`, `financial-statement`, `edgar-sec-filings`,
`earnings-forecast`, `valuation-model`, `macro-analysis`, `global-macro`,
`us-etf-flow`, `hk-connect-flow`

1. **Market data** — Fetch `{ticker}` daily OHLCV for the last 6 months and last 30 trading days
   via `yfinance`. Also pull comparable data for 2–3 sector peers or direct competitors
   for relative strength context.

2. **SEC filings** — Via `edgar-sec-filings`, retrieve `{ticker}`'s latest 10-Q/10-K. Extract:
   - Revenue growth QoQ and YoY
   - Gross margin trend
   - Core business segment revenue (absolute + % of total)
   - Free cash flow trajectory
   - P/E vs. 5-year historical average; PEG ratio
   - Forward EPS consensus estimates

3. **Earnings & valuation** — Via `earnings-forecast` + `valuation-model`:
   - Next earnings date, consensus EPS estimate, whisper number
   - Beat/miss history over the last 8 quarters
   - DCF fair value range (base / bull / bear assumptions)
   - Relative valuation: P/S, EV/EBITDA vs. sector median
   - Summarise: current premium or discount to fair value (%)

4. **Macro context** — Via `macro-analysis` + `global-macro`:
   - Sector-specific regulatory and policy risks (tariffs, export controls, antitrust)
   - Central bank rate path impact on sector multiples
   - Currency exposure and FX impact on revenues
   - Supply chain dependencies and geopolitical tail risks relevant to the sector

5. **Institutional flow** — Via `us-etf-flow` (US) or `hk-connect-flow` (HK/China-A):
   - ETF/fund flows into `{ticker}`-heavy funds over the last 30 days
   - Identify accumulation vs. distribution pattern

---

### PHASE 2 · Technical Analysis

**Skills to load:** `technical-basic`, `candlestick`, `ichimoku`, `elliott-wave`, `smc`,
`pattern-recognition`

6. **Core indicators** (daily timeframe) — Via `technical-basic`:
   - *Trend:* 20/50/200 EMA position; ADX(14)
   - *Momentum:* RSI(14), MACD(12,26,9), Stochastic(14,3)
   - *Volatility:* Bollinger Bands(20,2), ATR(14), historical vs. implied vol comparison
   - *Volume:* OBV, Volume Profile (identify HVN/LVN nodes), VWAP
   - *S/R levels:* Key horizontal levels + Fibonacci retracement from the last major swing high/low

7. **Candlestick patterns** — Via `candlestick`:
   Scan the last 60 daily candles. Flag high-probability patterns
   (engulfing, doji, hammer, morning/evening star, three white soldiers, etc.)
   at key S/R zones. Rate each pattern's reliability and note the directional bias.

8. **Ichimoku** — Via `ichimoku`:
   Full daily cloud analysis: Tenkan/Kijun cross signals, price vs. Kumo, Chikou span,
   Senkou spans A & B. Identify upcoming cloud twist dates and projected S/R zones.

9. **Elliott Wave** — Via `elliott-wave`:
   Count from the most recent major swing low. Identify current wave position (impulsive or
   corrective). Project wave targets using 1.618 and 2.618 extensions of Wave 1.
   Define the price level that would invalidate the primary count.

10. **Smart Money Concepts** — Via `smc`:
    Identify on weekly (HTF) and daily (LTF):
    - Order Blocks (OB) — both bullish and bearish
    - Fair Value Gaps (FVG) — unfilled imbalances
    - Break of Structure (BoS) and Change of Character (ChoCH)
    - Liquidity pools (equal highs/lows, stop-hunt zones)
    - Premium vs. discount zone positioning

11. **Classical patterns** — Via `pattern-recognition`:
    Scan for: H&S, Cup & Handle, Double Top/Bottom, triangles, wedges, flags/pennants.
    For any active patterns: provide the measured-move price target and the stop level.

---

### PHASE 3 · Options & Flow Intelligence

**Skills to load:** `options-strategy`, `options-advanced`

12. Pull `{ticker}` options chain for the nearest two monthly expiries. Analyse and report:
    - IV Rank and IV Percentile (30-day window)
    - Put/Call ratio by open interest and by volume
    - Max pain level for each expiry
    - Unusual options activity (UOA): large block trades, sweeps
    - Gamma exposure (GEX) by strike — identify the gamma flip level
    - Dealer positioning: are dealers long or short gamma at current spot?
    - Strike magnets: large OI clusters likely to pin price near expiry

---

### PHASE 4 · Multi-Factor & Quant Scoring

**Skills to load:** `multi-factor`, `factor-research`

13. **Factor model** — Via `multi-factor`:
    Score `{ticker}` on four factors vs. sector percentile:
    - Momentum: 3M, 6M, and (12M–1M) price return
    - Quality: ROE, ROIC, gross margin stability
    - Value: P/E, P/FCF, EV/Sales vs. sector median
    - Growth: revenue acceleration, EPS revision trend (up/flat/down)
    Output a composite score and per-factor percentile rank.

14. **IC/IR analysis** — Via `factor-research`:
    Which individual factors have had the highest predictive power
    for `{ticker}`'s next-month returns historically? Rank and weight accordingly.
    Highlight any factor that is currently giving a contrarian signal.

---

### PHASE 5 · Backtest Signal Validation

**Skills to load:** `strategy-generate`
**Tools:** `backtest`

15. Generate and backtest three strategies on `{ticker}` over the past 2 years:

    | ID | Strategy | Rules |
    |----|----------|-------|
    | A  | RSI Mean-Reversion | Buy RSI(14) < 35; sell RSI > 70; 3% hard stop |
    | B  | EMA Crossover | Buy 20 EMA crosses above 50 EMA with above-average volume; 5% trailing stop |
    | C  | Earnings Drift | Enter 5 trading days pre-earnings; exit 2 trading days post-earnings |

    Report for each: win rate (%), profit factor, max drawdown (%), Sharpe ratio,
    average holding period (days). Flag the strategy with the best risk-adjusted return
    for inclusion in the playbook setups.

---

### PHASE 6 · Playbook Report Output

**Skills to load:** `report-generate`, `pine-script`

Compile all phase outputs into the following structured playbook.
Use `report-generate` to produce a polished HTML/PDF report.
Export all indicators to Pine Script via `pine-script`.

---

## Output Structure

### SECTION 1 — {ticker} Scorecard

| Dimension | Signal | Confidence | Key Driver |
|-----------|--------|------------|------------|
| Fundamental | Bullish / Neutral / Bearish | % | e.g. "Core segment revenue +X% YoY, trading at Y% premium to DCF" |
| Technical | Bullish / Neutral / Bearish | % | e.g. "Price above 20/50/200 EMA, RSI mid-range, MACD bullish cross" |
| Options Flow | Bullish / Neutral / Bearish | % | e.g. "Dealer short gamma, call sweep UOA, max pain $X" |
| **Composite Bias** | **Long / Neutral / Short** | **%** | |

---

### SECTION 2 — Key Price Levels Map

Produce a table:

| Level ($) | Type | Source | Significance | Action Trigger |
|-----------|------|---------|--------------|----------------|
| ... | Support / Resistance / Target / Stop | Elliott / Fib / OB / FVG / Max Pain / GEX Flip | High / Medium / Low | e.g. "Long entry on reclaim with volume" |

Include at minimum: 3 support zones, 3 resistance zones, gamma flip, max pain,
Elliott primary target, top FVG(s), highest-confluence Order Block(s).

---

### SECTION 3 — 30-Day Scenario Analysis

For each scenario provide: probability (%), narrative, entry trigger, target, stop,
and risk/reward ratio.

- **Bull Scenario** (~X%): [Describe catalyst + breakout target]
- **Base Scenario** (~X%): [Describe range + mean-reversion setups]
- **Bear Scenario** (~X%): [Describe breakdown trigger + downside target]

---

### SECTION 4 — Week-by-Week Trading Calendar

| Week | Dates | Key Events / Catalysts | Bias / Watch-For | Preferred Action |
|------|-------|------------------------|------------------|------------------|
| 1 | ... | | | |
| 2 | ... | | | |
| 3 | ... | | | |
| 4 | ... | | | |
| 5 | ... | | | |

Calculate week dates dynamically from today. Flag earnings date, central bank decisions,
CPI/PPI prints, sector conferences, product events, and options expiry dates.

---

### SECTION 5 — Specific Trade Setups

For each setup (aim for 3–5 setups):

```
Setup Name:          [e.g. "Post-Earnings Momentum Long"]
Type:                [Swing / Momentum / Mean-Reversion / Event-Driven]
Timeframe:           [Daily / 4H]
Entry Condition:     [Exact price trigger or indicator signal]
Entry Zone:          $X.XX – $X.XX
Stop Loss:           $X.XX  (X% from entry)
Target 1:            $X.XX  (conservative, R:R X:1)
Target 2:            $X.XX  (extended, R:R X:1)
Position Size:       X% of portfolio (based on ATR-based volatility sizing)
Invalidation:        [Price/signal condition that cancels the setup]
Best Week to Enter:  Week N (from Section 4 calendar)
```

---

### SECTION 6 — Risk Events Calendar

List all known `{ticker}`-relevant catalysts in the next 30 days:

| Date | Event | Expected Impact | Playbook Adjustment |
|------|-------|----------------|---------------------|
| ... | e.g. {ticker} Earnings | High | Reduce size 2 days prior; re-enter post-print |
| ... | Central Bank Decision | Medium | Watch sector multiple sensitivity |
| ... | CPI/Inflation Print | Medium | FX and rates reaction |
| ... | Sector ETF Options Expiry | Low-Medium | Watch gamma pin effect |

---

### SECTION 7 — Daily Monitoring Checklist

**Pre-market (before open):**
- [ ] `{ticker}` pre-market price vs. prior close — any gap fill risk?
- [ ] Overnight futures / major index directional bias
- [ ] Any news / analyst upgrades-downgrades / filings overnight
- [ ] Options unusual activity scan (check unusual whales or similar)
- [ ] Check if price is near a key level from Section 2

**At close:**
- [ ] Did price respect or break the key level it was testing?
- [ ] RSI and MACD — any crossover or divergence developing?
- [ ] Volume vs. 20-day average — conviction or chop?
- [ ] OBV — confirming price direction?
- [ ] Thesis still intact? If not, note the condition that broke it.

**Thesis flip conditions (short → long or long → short):**
Document the specific price closes or indicator signals that would change the
composite bias from Section 1. Review weekly.

---

## Delivery Checklist

Before finishing, confirm all of the following are complete:

- [ ] `report-generate` — HTML/PDF playbook report saved
- [ ] `pine-script` — TradingView Pine Script v6 exported with all indicators
- [ ] Strategy code from Phase 5 saved via `write_file`
- [ ] All key levels from Section 2 are in the Pine Script as horizontal lines

---

## Notes for the Agent

- **Ticker required.** If the user has not specified a ticker, ask before starting.
- **Market inference.** Determine `{market}` from the ticker format:
  `.US` suffix → US, `.HK` → Hong Kong, `.SZ`/`.SH` → China A-share, `-USDT` → crypto.
  This drives data source selection, macro analysis focus, and flow tools.
- **Data freshness matters.** Always use the most recent available data. If `yfinance`
  returns data more than 1 trading day stale, warn the user.
- **Probability weights must sum to 100%.** Adjust scenario probabilities based on the
  composite scorecard from Section 1.
- **Sizing guidance** should use ATR(14)-based volatility sizing:
  `position_size = (account_risk_per_trade) / (ATR × 1.5)`. Default to 1% account risk
  per setup unless the user specifies otherwise.
- **If earnings fall within the 30-day window**, flag this prominently in every section —
  it is the single highest-impact event and should anchor the Week-by-Week calendar.
- **Disclaimer:** Append to the final report — *"This playbook is for research and
  educational purposes only. It does not constitute investment advice. Past backtest
  performance does not guarantee future results."*
