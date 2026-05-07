---
name: trading-playbook
description: >
  Generates a comprehensive 30-day institutional-grade trading playbook for any stock
  combining macro & industry context, deep fundamental analysis with DCF/PE-band/peer-comps,
  multi-timeframe technical analysis, options flow intelligence, quantitative factor scoring,
  backtested trade setups, and a week-by-week action calendar.
  Use this skill whenever the user asks for a trading plan, playbook, or actionable strategy
  for a specific ticker over the next month — including requests for buy/sell signals, entry/exit levels,
  scenario analysis, or "what to do with {ticker}." Also trigger when the user asks for a
  "full analysis" of a stock or wants to maximize profit over a 30-day window. This skill
  orchestrates all relevant sub-skills (macro, fundamentals, technicals, options, quant factors,
  backtest) and produces a structured, print-ready report.
---

# 30-Day Trading Playbook

A multi-phase agentic pipeline that produces an institutional-grade trading playbook for
a user-specified ticker covering the next 30 calendar days. The output is a structured
report with macro & industry context, fundamental deep dive, composite scorecard, key price
levels map, scenario analysis, week-by-week calendar, specific trade setups, risk event
calendar, and a daily monitoring checklist.

**Required input:** The user must provide a ticker symbol (e.g. AAPL, 700.HK, 000001.SZ).
If the user has not specified a ticker, ask for it before starting the pipeline.

---

## Evidence Weighting Principle

The playbook must be **anchored in fundamentals and macro, refined by technicals**.
Technicals inform entry/exit timing; they do NOT drive the thesis direction.

Approximate evidence weight for the composite scorecard:

| Evidence Layer | Weight | Role |
|----------------|--------|------|
| Fundamental (valuation, financials, earnings quality) | ~30% | Thesis foundation |
| Macro & Industry (cycle, rates, sector trends, competitive moat) | ~25% | Context & risk framing |
| Technical (trend, patterns, wave structure) | ~20% | Entry/exit timing |
| Flow & Sentiment (ETF flows, options positioning, analyst consensus) | ~15% | Confirmation |
| Options Intelligence (IV, max pain, GEX, UOA) | ~10% | Short-term pin/risk levels |

**Scenario probabilities must be justified by fundamental + macro arguments first.**
If a scenario exists only because a technical pattern suggests it, that scenario
needs a fundamental catalyst to justify its probability weight.

---

## Execution Pipeline

Work through each phase in order. Load each named skill before executing that phase.
**Phases 1 and 2 are the foundation — they carry more weight than Phase 3.**
Do not skip or shortchange them.

Throughout all phases, replace `{ticker}` with the user-provided symbol and `{market}`
with the inferred market (US, HK, China-A, crypto) based on the symbol format.

---

### PHASE 1 · Macro & Industry Context

**Skills to load:** `macro-analysis`, `global-macro`, `us-etf-flow`, `hk-connect-flow`,
`data-routing`

This phase establishes the external environment the ticker operates in. Every subsequent
phase should be interpreted through this lens.

1. **Economic cycle positioning** — Via `macro-analysis` + `global-macro`:
   - Current Fed funds rate / PBOC / ECB policy stance with specific dates
   - Latest CPI, core PCE, PMI, GDP readings (cite specific values and dates)
   - Map to Merrill Lynch clock quadrant (recovery / overheat / stagflation / recession)
   - Rate path outlook: what does the dot plot / forward guidance imply for sector multiples?
   - Quantify: a 1pp change in discount rate shifts DCF value by ~15–20% for growth stocks

2. **Industry cycle phase** — Via web research:
   - Is the sector in expansion, peak, digestion, or contraction?
   - Global sector sales/revenue growth trend (cite specific forecasts, e.g. WSTS)
   - Supply/demand balance: tight or glut? Inventory levels at key customers?
   - Relevant sector index performance (SOX for semis, XLF for financials, etc.)

3. **Institutional flow** — Via `us-etf-flow` (US) or `hk-connect-flow` (HK/China-A):
   - ETF/fund flows into the ticker's sector ETFs over the last 60 days
   - Accumulation or distribution signal? Record inflows or outflows?
   - Cite specific dollar amounts (e.g. "SMH +$3.4B in April")

4. **Competitive landscape & moat assessment** — Via web research:
   - Market share position; is the moat widening or narrowing?
   - Key competitors and their recent moves (product launches, pricing, market share shifts)
   - Threat from substitutes or custom/vertical integration by customers
   - Time horizon for competitive threats (12-month vs 3-year view)

5. **Geopolitical & regulatory risk** — Via web research:
   - Sector-specific regulatory risks (tariffs, export controls, antitrust, data regulation)
   - Supply chain dependencies and geopolitical tail risks (e.g. Taiwan strait, rare earths)
   - Currency exposure and FX impact if revenues are multi-currency
   - Any pending legislation or executive actions in the 30-day window

6. **Upcoming macro events in the 30-day window**:
   - CPI/PCE release dates
   - Central bank meeting dates
   - Major sector conferences or trade shows
   - These go into the Risk Events Calendar (Section 8 of output)

---

### PHASE 2 · Deep Fundamentals & Valuation

**Skills to load:** `yfinance`, `financial-statement`, `edgar-sec-filings`,
`earnings-forecast`, `valuation-model`

This phase establishes whether the ticker is cheap, fair, or expensive on both
absolute and relative bases. **Specific quantitative outputs are mandatory.**

1. **Financial statements** — Via `yfinance` + `financial-statement`:
   - Pull latest 4 quarters + annual data (income statement, balance sheet, cash flow)
   - Key metrics: revenue, gross margin trend, operating margin, net income, EPS, FCF
   - Revenue segment breakdown (which segments are growing/shrinking?)
   - **Cash flow quality check**: CFO/Net Income ratio, FCF margin, capex/revenue ratio
   - Balance sheet: cash, total debt, net cash/debt, goodwill as % of equity

2. **DuPont ROE decomposition** (mandatory):
   - Decompose ROE = Net Margin × Asset Turnover × Equity Multiplier
   - Identify which component drives ROE (margin? leverage? turnover?)
   - Compare to ≥2 direct peers (not just industry averages)
   - Flag: if equity multiplier is the dominant driver, that's lower quality

3. **Revenue concentration analysis** (mandatory):
   - What % of revenue comes from the top segment? Top 2–3 customers?
   - Any single-customer >10% concentration? If indirect (via integrators), estimate.
   - This is a key risk factor — flag prominently if concentration >30% top 2 customers

4. **DCF valuation with sensitivity table** (mandatory — must produce ≥3×3 matrix):
   - Build 3 scenarios: Bull, Base, Bear
   - Vary: revenue CAGR, terminal growth rate, WACC
   - Output a sensitivity table: WACC (rows, at least 3 values) × terminal growth (columns, at least 3 values)
   - Report per-share fair value for each cell
   - State which cell corresponds to current market price (implied expectations)

5. **PE band & relative valuation** (mandatory):
   - Report current TTM PE and forward PE
   - Report 5-year PE range: min, 25th percentile, median, 75th percentile, max
   - State current percentile rank
   - PEG ratio (current PE / earnings growth rate): <1.0 = undervalued on growth basis
   - EV/EBITDA vs 5-year average

6. **Peer comparison table** (mandatory — ≥7 metrics across ≥3 peers):
   - Include: market cap, revenue (TTM), revenue growth (YoY), gross margin, net margin,
     ROE, forward PE, PEG, EV/EBITDA, FCF yield, debt/equity
   - Compare ticker to its closest competitors
   - Highlight where the ticker leads and lags

7. **Earnings analysis** — Via `earnings-forecast`:
   - Next earnings date (flag if within the 30-day window — this is a critical anchor)
   - Consensus EPS and revenue estimates
   - Beat/miss history over the last 8 quarters
   - Analyst consensus (Strong Buy / Buy / Hold / Sell) and average target price

---

### PHASE 3 · Technical Analysis

**Skills to load:** `technical-basic`, `candlestick`, `ichimoku`, `elliott-wave`, `smc`,
`pattern-recognition`

Technicals are used for **entry/exit timing and stop placement**, not thesis direction.
The trend, levels, and patterns identified here should be cross-referenced against the
valuation support/resistance zones found in Phase 2.

1. **Core indicators** (daily timeframe) — Via `technical-basic`:
   - *Trend:* 20/50/200 EMA position; ADX(14) with +DI/-DI
   - *Momentum:* RSI(14), MACD(12,26,9), Stochastic(14,3)
   - *Volatility:* Bollinger Bands(20,2), ATR(14), historical volatility percentile
   - *Volume:* OBV, Volume Profile, VWAP, volume vs 20-day average

2. **Candlestick patterns** — Via `candlestick`:
   - Scan the last 60 daily candles for high-probability patterns
   - Only flag patterns at key S/R zones (not in no-man's-land)
   - Rate directional bias and note which patterns have confluence with fundamental levels

3. **Ichimoku** — Via `ichimoku`:
   - Full daily cloud analysis: Tenkan/Kijun cross, price vs Kumo, Chikou span
   - Future cloud twist dates and projected S/R
   - Signal only when all three filters align; otherwise note "mixed"

4. **Elliott Wave** — Via `elliott-wave`:
   - Identify primary wave count from most recent major swing low
   - Project targets: W5 = W1, W5 = W1 × 1.618, W5 = W1 × 2.618
   - Define the invalidation level that breaks the count
   - Validate against the 3 iron rules; note if any are violated

5. **Smart Money Concepts** — Via `smc`:
   - Order Blocks (OB), Fair Value Gaps (FVG), Break of Structure (BoS/ChoCH)
   - Liquidity pools (equal highs/lows), premium vs discount zone

6. **Classical patterns** — Via `pattern-recognition`:
   - Scan for H&S, Cup & Handle, Double Top/Bottom, triangles, wedges
   - For active patterns: measured-move target + stop level

---

### PHASE 4 · Options & Flow Intelligence

**Skills to load:** `options-strategy`, `options-advanced`

1. Pull `{ticker}` options chain for the nearest two monthly expiries. Report:
   - IV Rank and IV Percentile (30-day window)
   - Put/Call ratio by open interest and by volume
   - Max pain level for each expiry
   - Unusual options activity (UOA): large block trades, sweeps
   - Gamma exposure (GEX) by strike — identify the gamma flip level
   - Dealer positioning: are dealers long or short gamma at current spot?
   - Strike magnets: large OI clusters likely to pin price near expiry

2. Cross-reference options levels with fundamental valuation zones from Phase 2.
   For example: max pain at $X that also sits near DCF fair value → higher significance.

---

### PHASE 5 · Multi-Factor & Quant Scoring

**Skills to load:** `multi-factor`, `factor-research`

1. **Factor model** — Via `multi-factor`:
   - Score `{ticker}` on four factors vs sector percentile:
     - Momentum: 3M, 6M, (12M–1M) price return
     - Quality: ROE, ROIC, gross margin stability
     - Value: P/E, P/FCF, EV/Sales vs sector median
     - Growth: revenue acceleration, EPS revision trend
   - Output composite score and per-factor percentile rank

2. **IC/IR analysis** — Via `factor-research`:
   - Which factors have had the highest predictive power for `{ticker}`'s
     next-month returns historically? Rank and weight accordingly.
   - Highlight any factor currently giving a contrarian signal vs the composite

---

### PHASE 6 · Backtest Signal Validation

**Skills to load:** `strategy-generate`
**Tools:** `backtest`

1. Generate and backtest three strategies on `{ticker}` over the past 2 years:

   | ID | Strategy | Rules |
   |----|----------|-------|
   | A  | RSI Mean-Reversion | Buy RSI(14) < 35; sell RSI > 70; 3% hard stop |
   | B  | EMA Crossover | Buy 20 EMA crosses above 50 EMA with above-average volume; 5% trailing stop |
   | C  | Earnings Drift | Enter 5 trading days pre-earnings; exit 2 trading days post-earnings |

2. Report for each: win rate (%), profit factor, max drawdown (%), Sharpe ratio,
   average holding period (days). Flag the strategy with the best risk-adjusted return
   for inclusion in the playbook setups.

3. Note whether the best backtested strategy aligns with the 30-day catalyst calendar.
   (e.g., Earnings Drift strategy + upcoming earnings date = high relevance)

---

### PHASE 7 · Synthesis & Playbook Report

**Skills to load:** `report-generate`, `pine-script`

Compile all phase outputs into the structured playbook below.
Use `report-generate` to produce a polished Markdown report.
Export all indicators to Pine Script via `pine-script`.

**Balance gate — verify BEFORE writing the final report:**

- [ ] DCF sensitivity table present (≥3×3 WACC/growth matrix)
- [ ] PE band: current percentile vs 5-year min/25th/50th/75th/max explicitly stated
- [ ] Peer comparison table: ≥7 metrics across ≥3 peers
- [ ] DuPont ROE decomposition with ≥2 peer comparisons
- [ ] Macro section references ≥3 specific indicators with dates (e.g. "core PCE 3.2% YoY, Mar 2026")
- [ ] Competitive landscape / moat assessment present
- [ ] Revenue concentration analysis present
- [ ] Scenario probabilities justified by ≥1 fundamental or macro argument each (not just technicals)
- [ ] Position sizing formula: `position_size = account_risk / (ATR × 1.5)` with default 1% risk
- [ ] Earnings date prominently flagged in every section if within the 30-day window

If any checkbox fails, return to the relevant phase and gather the missing data before outputting.

---

## Output Structure

### SECTION 1 — Macro & Industry Context

Summarize Phase 1 findings in 2–3 paragraphs with a macro dashboard table:

| Indicator | Latest | Date | Trend |
|-----------|--------|------|-------|
| e.g. Core PCE | 3.2% YoY | Mar 2026 | ↑ |
| ... | ... | ... | ... |

Include: economic cycle position, rate path implication, industry phase, competitive moat
assessment, institutional flow direction, and geopolitical risk summary.

### SECTION 2 — Fundamental Deep Dive

From Phase 2:
- Revenue & earnings summary table (latest quarter + fiscal year)
- DuPont ROE decomposition with peer comparison
- Cash flow quality assessment
- Revenue concentration analysis
- **DCF sensitivity table** (≥3×3 matrix: WACC rows × terminal growth columns)
- **PE band summary**: current TTM PE, forward PE, 5-year range with percentiles, PEG ratio
- **Peer comparison table** (≥7 metrics, ≥3 peers)
- Upcoming earnings: date, consensus, beat history

### SECTION 3 — Composite Scorecard

| Dimension | Signal | Confidence | Key Driver |
|-----------|--------|------------|------------|
| Macro | Bullish / Neutral / Bearish | % | e.g. "Mid-expansion, core PCE 3.2%, rates on hold" |
| Industry | Bullish / Neutral / Bearish | % | e.g. "Record sector ETF inflows, WSTS 26% growth forecast" |
| Fundamental | Bullish / Neutral / Bearish | % | e.g. "Forward PE 24.9x vs 74.6x median, PEG 0.64, DCF fair value $X" |
| Competitive Moat | Bullish / Neutral / Bearish | % | e.g. "~80% share, CUDA lock-in; ASICs narrowing at edges" |
| Technical | Bullish / Neutral / Bearish | % | e.g. "Price above 20/50/200 EMA, RSI mid-range, Wave 5 in progress" |
| Flow / Sentiment | Bullish / Neutral / Bearish | % | e.g. "Record ETF inflows, unanimous Strong Buy consensus" |
| **Composite Bias** | **Long / Neutral / Short** | **%** | |

The composite confidence is the weighted average using the weights from the
Evidence Weighting Principle section. Fundamental + Macro dimensions carry ~55% of the weight.

### SECTION 4 — Key Price Levels Map

| Level ($) | Type | Source | Significance | Action Trigger |
|-----------|------|---------|--------------|----------------|
| ... | Support / Resistance / Target / Stop | Elliott / Fib / OB / FVG / Max Pain / GEX Flip / DCF Fair Value | High / Medium / Low | e.g. "Long entry on reclaim with volume" |

Include: 3 support zones, 3 resistance zones, gamma flip, max pain, Elliott primary target,
top FVG(s), highest-confluence Order Block(s). Annotate which levels have both technical AND
fundamental significance (dual-confirmation levels carry higher weight).

### SECTION 5 — 30-Day Scenario Analysis

For each scenario: probability (%), fundamental catalyst, macro backdrop, entry trigger,
target, stop, and risk/reward ratio.

- **Bull Scenario** (~X%): Fundamental catalyst + macro backdrop + technical breakout target
- **Base Scenario** (~X%): Fundamental anchor + range-bound technical structure
- **Bear Scenario** (~X%): Macro shock or fundamental disappointment + breakdown level

Probabilities must sum to 100%. Each scenario's probability must be justified by at least
one fundamental or macro argument. (The Bull scenario should not exist solely because
"Elliott Wave says Wave 5 extends.")

### SECTION 6 — Week-by-Week Trading Calendar

| Week | Dates | Key Events / Catalysts | Bias / Watch-For | Preferred Action |
|------|-------|------------------------|------------------|------------------|
| 1 | ... | | | |
| 2 | ... | | | |
| 3 | ... | | | |
| 4 | ... | | | |
| 5 | ... | | | |

Calculate week dates dynamically from today. Flag: earnings date, CPI/PCE releases, central
bank decisions, sector conferences, product events, and options expiry dates.
**Earnings within the window must be flagged as the anchor event.**

### SECTION 7 — Specific Trade Setups

3–5 setups. Each setup now includes a **Fundamental Basis** field:

```
Setup Name:          [e.g. "Post-Earnings Momentum Long"]
Type:                [Swing / Momentum / Mean-Reversion / Event-Driven]
Fundamental Basis:   [e.g. "Forward PE 24.9x at historic low; 7/8 quarter beat history"]
Timeframe:           [Daily / 4H]
Entry Condition:     [Exact price trigger or indicator signal]
Entry Zone:          $X.XX – $X.XX
Stop Loss:           $X.XX  (X% from entry)
Target 1:            $X.XX  (conservative, R:R X:1)
Target 2:            $X.XX  (extended, R:R X:1)
Position Size:       X% of portfolio (ATR $X.XX × 1.5 = $X.XX stop width;
                     1% account risk default)
Invalidation:        [Price/signal condition that cancels the setup + fundamental trigger if applicable]
Best Week to Enter:  Week N (from Section 6 calendar)
```

### SECTION 8 — Risk Events Calendar

| Date | Event | Expected Impact | Mechanism | Playbook Adjustment |
|------|-------|----------------|-----------|---------------------|
| ... | e.g. CPI Release | High / Medium / Low | e.g. "Hot print → rate hike fears → growth multiple compression" | e.g. "Delay new entries until after 8:30 AM print" |
| ... | {ticker} Earnings | Critical | Revenue/GM/guidance | Reduce size 50% 2 days prior |
| ... | FOMC Decision | Medium | Rate path signal | Monitor; no change expected |

Include both ticker-specific events AND macro events from Phase 1.

### SECTION 9 — Daily Monitoring Checklist

**Pre-market:**
- [ ] `{ticker}` pre-market price vs. prior close — gap fill risk?
- [ ] Overnight futures / major index directional bias
- [ ] Any macro data prints today? (CPI, PCE, PMI dates from Section 8)
- [ ] Any news / analyst upgrades-downgrades / filings overnight
- [ ] Options unusual activity scan
- [ ] Check if price is near a key level from Section 4

**At close:**
- [ ] Did price respect or break the key level it was testing?
- [ ] RSI and MACD — any crossover or divergence developing?
- [ ] Volume vs. 20-day average — conviction or chop?
- [ ] OBV — confirming price direction?
- [ ] Thesis still intact? If not, note the fundamental or macro condition that broke it.

**Thesis flip conditions (LONG → FLAT/SHORT):**
List 3–5 specific conditions spanning fundamental, macro, technical, and industry triggers.
Each must be a specific, observable event (not a vague "sentiment changes").

### SECTION 10 — Data Appendix

- Financial summary table
- Valuation summary (DCF range, PE band percentiles, peer comparison)
- Backtest summary table
- Technical snapshot table
- Macro dashboard table
- Pine Script reference code

---

## Delivery Checklist

Before finishing, confirm all of the following are complete:

- [ ] **Balance gate passed** (all 10 checkboxes from Phase 7)
- [ ] `report-generate` — Markdown playbook report saved
- [ ] `pine-script` — TradingView Pine Script v6 exported with all indicators
- [ ] Strategy code from Phase 6 saved via `write_file`
- [ ] All key levels from Section 4 are in the Pine Script as horizontal lines
- [ ] Fundamental + Macro sections comprise at least 40% of the total report length
  (not including appendix/data tables). If technical sections dominate, re-expand
  Phases 1 and 2.

---

## Notes for the Agent

- **Ticker required.** If the user has not specified a ticker, ask before starting.
- **Market inference.** Determine `{market}` from the ticker format:
  `.US` suffix → US, `.HK` → Hong Kong, `.SZ`/`.SH` → China A-share, `-USDT` → crypto.
  This drives data source selection, macro analysis focus, and flow tools.
- **Phases 1 and 2 come first for a reason.** They are the foundation. A playbook
  that has a detailed Elliott Wave count but no DCF sensitivity table is unbalanced.
  If you find yourself spending more time on Phase 3 than Phases 1+2 combined, stop
  and rebalance.
- **Data freshness matters.** Always use the most recent available data. If `yfinance`
  returns data more than 1 trading day stale, warn the user.
- **Probability weights must sum to 100%.** Adjust scenario probabilities based on
  the composite scorecard. Each scenario must have at least one fundamental or macro
  justification — not purely technical.
- **Sizing guidance** uses ATR(14)-based volatility sizing:
  `position_size = (account_risk_per_trade) / (ATR × 1.5)`. Default to 1% account risk
  per setup unless the user specifies otherwise.
- **If earnings fall within the 30-day window**, flag this prominently in every section —
  it is the single highest-impact event and should anchor the Week-by-Week calendar.
- **Peer selection**: Use direct competitors in the same industry and of comparable scale.
  Do not compare a $50B company to a $5T company as a "peer."
- **Disclaimer:** Append to the final report — *"This playbook is for research and
  educational purposes only. It does not constitute investment advice. Past backtest
  performance does not guarantee future results."*
