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

**Execution requirement:** The agent MUST execute every phase below in strict
order. Do not skip, reorder, or shortcut any phase. Do not fabricate data, skip
a phase because data is hard to find, or make up scores without running the named
tools and loading the named skills. Every phase produces mandatory inputs for the
next. If you are tempted to shortcut, log the gap instead — never fake it.

**Required input:** The user must provide a ticker symbol (e.g. AAPL, 700.HK, 000001.SZ).
If the user has not specified a ticker, ask for it before starting the pipeline.

**Data accuracy is mandatory.** Every data point in the report MUST be traceable
to a tool call or web source. If data cannot be found, record it as a data gap in
the generation log (see Generation Log Protocol below) — do not fabricate or infer
without clearly stating the assumption and its justification.

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

## Red Flags & Override Protocol

Some signals are strong enough to override the normal evidence weighting. When
any of these fire, the report MUST explicitly address them — ignoring them without
comment is the cardinal sin of confirmation bias.

| Red Flag | Threshold | Required Action |
|----------|-----------|-----------------|
| RSI(14) Daily > 80 | Extreme overbought | Bear scenario probability floor rises to **20%**; require explicit justification if Bull > 30%. Flag in Section 3, Section 5, and Section 8. |
| RSI(14) Daily < 20 | Extreme oversold | Bull scenario probability floor rises to **20%**; require explicit justification if Bear > 30%. |
| RSI(14) Weekly > 85 | Extreme overbought (longer timeframe) | Same as daily but higher severity — weekly RSI this high has historically preceded significant corrections. |
| Price > BB Upper (2σ) on daily | Parabolic extension beyond +2σ | Flag "mean-reversion risk elevated" in Section 3 and Section 8. Mean-reversion to BB Mid (SMA20) within 10 bars is the statistical base case. New entries should be pullback entries, not breakout chases. |
| DCF base fair value vs market price > 50% gap | Valuation model disconnect | MUST reconcile or remove DCF (see DCF reconciliation rule in Phase 2, Step 4). Presenting a DCF that screams SELL and then pivoting to "but forward PE is fine" is prohibited. |
| ADX(14) > 45 | Extreme trend strength | Trend continuation is fully priced in; discuss exhaustion risk in Section 5. |
| ATR expansion > 3× within 60 days | Volatility regime change | Flag prominently. Historical backtests using pre-expansion data are invalid — note this in Phase 6. |
| Insider selling at ATH with > 3:1 sell/buy ratio | Distribution signal | Downgrade Flow/Sentiment by at least one tier. Flag prominently in Section 2. |
| Macro indicator > 2 months stale | Data reliability | Flag with "⚠ Stale" in the macro dashboard table. Stale macro data undermines the Section 1 thesis. |

**How these flags interact with the composite scorecard:**
- A single red flag does not flip the thesis — but it must visibly modify the risk/reward
  assessment in the relevant sections.
- **Two or more red flags simultaneously** → scenario probabilities MUST be re-weighted
  (e.g., Bull no higher than 30%, Bear no lower than 20%).
- **Three or more red flags** → the report MUST include an explicit "Risks Outweigh
  Rewards" warning at the top of the introduction.

---

## Generation Log Protocol

Every playbook invocation MUST produce a companion generation log that records
exactly how the playbook was built — what data was found, what tools were called,
what assumptions were made, and what gaps exist. The log is the audit trail.

**Log file path**: `reports/playbooks/logs/{TICKER}_generation_log_{YYYY-MM-DD}.md`

**Log structure**:

```markdown
# {TICKER} Playbook Generation Log — {YYYY-MM-DD}

**Generated at**: {timestamp} | **Total phases**: 7 | **Total tool calls**: N

## Phase Summary

| Phase | Status | Time | Tools Used |
|-------|--------|------|------------|
| 1. Macro & Industry | COMPLETE | ~Xm | ... |
| ... | ... | ... | ... |

## Detailed Phase Logs

### Phase N: [Name] — [COMPLETE / PARTIAL]

**Time**: approx X minutes
**Skills loaded**: skill1, skill2
**Tools used**: tool1 (N calls), tool2 (M calls)

**Key data found**:
| Data Point | Value | Source |
|------------|-------|--------|
| ... | ... | ... |

**Assumptions made**:
- Assumption — justification

**Data gaps** (searched but not found):
- Gap — proxy used

**Decisions**:
- Decision — rationale

## Assumptions Register
(All assumptions from all phases, consolidated)

## Data Gaps Register
(All gaps from all phases, consolidated)

## Tool Call Summary
| Tool | Count | Phases |
|------|-------|--------|
| ... | ... | ... |

## Balance Gate Results
(Pass/fail for each of the 15 checkboxes)
```

**At the START of each phase**, note the phase number, name, and start time.
**At the END of each phase**, record the log entry following the template above.
Accumulate all entries and write the final log file in Phase 7.

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

7. **Historical cycle parallels** — Via web research (mandatory):
   - Find 1-2 prior cycles for this sector or company where similar macro + industry
     conditions existed (e.g. "semiconductor cycle peak 2000," "crude oil supercycle 2008,"
     "biotech IPO window 2020-21")
   - Compare: valuation multiples at the prior cycle peak vs now, duration of the prior
     run, what specifically ended the prior cycle (rate hike? supply glut? demand exhaustion?)
   - If "this time is different" is the thesis, state it explicitly and provide the
     concrete structural difference (e.g. "AI inference TAM is a new demand driver that
     didn't exist in 2000; hyperscaler CapEx is contracted 3+ years out")
   - This historical reference MUST appear in Section 5 (Scenario Analysis) — each
     scenario should reference the closest historical analog
   - This prevents buying the narrative at the cycle top by providing an anchor
     outside the current euphoria

8. **Log this phase** — record:
   - Web search queries executed and URLs consulted
   - All specific indicator values found (Fed rate, CPI, PCE, PMI, GDP — with dates)
   - **Data staleness check**: for each macro indicator, note the date. If any indicator
     is >2 months old, flag it with "⚠ STALE" in the log and in the report's macro dashboard
   - Exchange rates used with dates
   - Industry growth forecasts and their sources (e.g. "WSTS: +26.3% in 2026")
   - ETF flow data: specific dollar amounts and date ranges
   - Competitive landscape data: market share percentages, competitor financials
   - Regulatory/political findings: specific laws, dates, impact estimates
   - Historical cycle research: the 1-2 historical parallels found, key data points
     compared (valuation then vs now, duration, what ended the cycle)
   - Any macro data that was searched for but NOT found (data gaps)
   - Assumptions made about rate path, FX trajectory, or sector growth

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
   - **Non-GAAP adjustment**: If GAAP ROE is distorted by acquisition amortization,
     goodwill impairments, or one-time charges, compute non-GAAP adjusted ROE and
     present BOTH GAAP and non-GAAP values in the table. Large divergence between
     GAAP and non-GAAP ROE is itself a signal about accounting quality — cite the
     specific adjustments made (e.g. "excluded $2.2B/year Xilinx amortization")

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

   **DCF reconciliation rule (CRITICAL — enforced at balance gate):**
   After producing the DCF sensitivity table, compare the base-case fair value to
   the current market price. If the gap exceeds 50% (either direction), you MUST
   choose one of the following and document it in the report:
   
   - **Option A — Adjust DCF**: Modify DCF assumptions with documented justification
     (e.g. "terminal growth raised to 6% from 4% because AI TAM expansion extends
     the growth runway beyond a typical 5-year DCF horizon"). The adjustment must
     be defensible — do not reverse-engineer assumptions to match the market price.
   - **Option B — Reconcile the gap**: State the implied growth rate or terminal
     value embedded in the current market price (reverse DCF). Example: "At $455,
     the market is pricing ~25% revenue CAGR for 8 years with 22% terminal FCF
     margin — this is the AI bull case, not the base case."
   - **Option C — Reject DCF**: State that DCF cannot meaningfully value this
     company at its current stage and explain why (e.g. "pre-revenue biotech,"
     "hypergrowth where terminal value assumptions dominate at unrealistic levels").
     If you reject DCF, remove the sensitivity table and rely on PE band + peer
     comps + PEG as the primary valuation anchors.
   
   **PROHIBITED**: Including a DCF that implies 70%+ overvaluation, dismissing it
   in one sentence, and pivoting to "but forward PE is reasonable." If DCF and
   market price fundamentally disagree, either fix the DCF, explain what the market
   is pricing that DCF misses, or admit DCF can't value this company. The DCF
   section must either be useful or absent — never decorative.

5. **PE band & relative valuation** (mandatory):
   - Report current TTM PE and forward PE
   - Report 5-year PE range: min, 25th percentile, median, 75th percentile, max
   - State current percentile rank
   - PEG ratio: explicitly state the formula used — numerator (forward PE or TTM PE)
     AND denominator (EPS growth rate or revenue growth rate). Use the SAME growth
     rate definition for all peers in the comparison table. Example: "Forward PE
     35.3x / consensus EPS growth 32% = PEG 1.10." If you cannot find a reliable
     EPS growth estimate, state what proxy you used.
   - PEG <1.0 = undervalued on growth basis; PEG 1.0-2.0 = fairly valued;
     PEG >2.0 = growth is priced in, high expectations burden
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
   - Post-earnings analyst revisions: are targets being raised or cut? Stale targets
     (pre-earnings) should be flagged

8. **Insider transaction analysis** (mandatory) — Via web research:
   - Pull last 3 months of insider buying and selling for {ticker}
   - Report: aggregate buy/sell ratio by value, number of insider sellers vs buyers,
     any cluster selling by C-suite or directors
   - **Flag prominently if**: (a) insiders are selling into ATH strength,
     (b) sell/buy ratio exceeds 3:1 by value, (c) CEO or CFO sold in the last 30 days,
     (d) no insider buys in the last 6 months despite price pullbacks
   - Context matters: note whether sales were pre-scheduled 10b5-1 plans or
     opportunistic. But even planned sales at ATH are a signal — the insider
     chose not to cancel the plan.
   - If insider data is unavailable for this market (e.g. some HK/China-A stocks),
     note explicitly: "Insider transaction data not available for {market}"

9. **Log this phase** — record:
   - Data sources used (yfinance ticker calls, web search queries with specific URLs)
   - All financial metrics found (revenue, gross margin, op income, net income, EPS, FCF, EBITDA — with exact values and fiscal periods)
   - Balance sheet data: cash, debt, net cash, shares outstanding, book value
   - **Non-GAAP adjusted ROE**: both GAAP and non-GAAP values, and the specific adjustments made (e.g. "excluded $2.2B/year Xilinx amortization")
   - DCF assumptions chosen and WHY (e.g. "WACC 15%: beta 2.40 × ERP 5.0% + Rf 4.5%")
   - **DCF reconciliation**: if market price vs DCF base value gap >50%, which option (A/B/C) was chosen and the full reasoning
   - PE band source data: 5-year PE values (min/25th/50th/75th/max) and data source
   - **PEG formula**: exact numerator (forward/TTM PE) and denominator (EPS/revenue growth rate) with data sources
   - Peer comparison raw data for each peer before formatting into table
   - Analyst ratings: number of analysts, rating distribution, individual PTs with dates (flag stale targets)
   - **Insider transactions**: last 3 months buy/sell count and value, notable individual transactions, 10b5-1 context if applicable
   - Segment breakdown: revenue by business line and geography with percentages
   - Any data searched for but NOT found (e.g. "insider transaction data not available for 700.HK")
   - Estimated time spent on this phase

---

### PHASE 3 · Technical Analysis

**Skills to load:** `moomoo-technicals` (PRIMARY — all indicator calculations),
`candlestick`, `ichimoku`, `elliott-wave`, `smc`, `pattern-recognition`

Technicals are used for **entry/exit timing and stop placement**, not thesis direction.
The trend, levels, and patterns identified here should be cross-referenced against the
valuation support/resistance zones found in Phase 2.

> **CRITICAL — Data Accuracy:** The `moomoo-technicals` skill documents that moomoo's
> default `--rehab forward` adjustment severely distorts historical prices (e.g. NVDA
> $215 close → $173), rendering EMA/RSI/MACD calculations wrong. **Every kline fetch
> in this phase MUST use `--rehab none`** and the latest close MUST be verified against
> `get_snapshot.py`. Skipping this step produces a playbook with incorrect support/resistance
> levels — as verified by the GOOGL audit where EMA 20 was off by $27 (7.5%) and BB Lower
> was off by $57 (19%).

1. **Core indicators** (daily + weekly timeframes) — Via `moomoo-technicals`:
   - **Fetch data** with explicit `--rehab none`:
     ```bash
     # Daily (200 bars)
     python3 ~/.claude/skills/moomooapi/scripts/quote/get_kline.py US.{TICKER} \
       --ktype 1d --num 200 --rehab none --json 2>&1 \
       | grep '^{"code"' > /tmp/{ticker}_daily.json

     # Weekly (100 bars)
     python3 ~/.claude/skills/moomooapi/scripts/quote/get_kline.py US.{TICKER} \
       --ktype 1w --num 100 --rehab none --json 2>&1 \
       | grep '^{"code"' > /tmp/{ticker}_weekly.json
     ```
   - **Verify** latest close against snapshot before calculating:
     ```bash
     python3 ~/.claude/skills/moomooapi/scripts/quote/get_snapshot.py US.{TICKER} --json
     ```
   - **Calculate** using the exact Python code from `moomoo-technicals` (EMA, RSI with
     Wilder's smoothing, MACD, ATR, ADX, Bollinger Bands, OBV). The code is provided
     in the skill — do not substitute your own implementations.
   - *Trend:* 20/50/200 EMA position (daily AND weekly); ADX(14) with +DI/-DI
   - *Momentum:* RSI(14), MACD(12,26,9); compare daily vs weekly alignment
   - *Volatility:* Bollinger Bands(20,2), ATR(14)
   - *Volume:* OBV trend; volume vs 20-day average (ratio)
   - **Cross-reference timeframes**: daily + weekly alignment gives stronger signals.
     Divergence between timeframes is a caution flag.
   - **Extreme reading protocol (mandatory flagging):**
     If RSI(14) daily > 80 or weekly > 85, you MUST add a prominent "⚠ Extreme Overbought"
     flag to the report. This flag must appear in: (a) the technical snapshot table (Section 10),
     (b) the composite scorecard as a risk note (Section 3), (c) the scenario analysis where
     bear scenario probability floor rises to 20% (Section 5), and (d) the risk events calendar
     as a near-term risk (Section 8).
     If ADX(14) > 45, flag "⚠ Extreme Trend Strength" and discuss exhaustion risk in Section 5.
     If price has broken above the daily BB Upper, note that mean-reversion to the BB Mid
     (SMA20) within 10 bars is the statistical base case — this should inform entry strategy
     (pullback entries, not breakout chases).
     If ATR has expanded >3× over the past 60 days, flag "⚠ Volatility Regime Change" —
     historical backtests from Phase 6 using pre-expansion data are invalid and must be
     qualified prominently.
     These flags do not mean "sell" — but they mean "the easy money has been made,"
     new entries carry elevated risk, and the report must reflect this honestly.

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

7. **Log this phase** — record:
   - **Moomoo data verification:**
     - Rehab mode used: `--rehab none` (MUST be confirmed in log)
     - Snapshot verification: latest close from `get_snapshot.py` vs kline last bar close (must match)
     - Kline date range: first bar date to last bar date, number of bars (daily AND weekly)
   - All indicator values computed (EMA 20/50/200 daily AND weekly, RSI, MACD, ADX +DI/-DI, BB Upper/Mid/Lower, ATR, OBV — with exact values)
   - Key price levels identified: support/resistance with sources (Fib, swing points, volume profile)
   - Ichimoku: Tenkan/Kijun/Senkou values, cloud status, signal verdict
   - Elliott Wave: wave count, projection targets, invalidation level, rule violations
   - Candlestick patterns found (dates, types, prices)
   - SMC: FVGs identified (price ranges and dates), OB zones, BoS/ChoCH signals
   - Volume analysis: 20-day avg volume, latest volume ratio
   - Data range: how many candles were analyzed (e.g. "200 daily bars, 2025-07-24 to 2026-05-08")
   - Any indicators that were NOT computed (e.g. "EMA200 not available — only 123 days of data")
   - **Cross-verification**: were the actual computed EMA/BB levels cross-checked against the key levels in Section 4? Record any discrepancies found.

---

### PHASE 4 · Options & Flow Intelligence

**Skills to load:** `options-strategy`, `options-advanced`

1. Pull `{ticker}` options chain for the nearest two monthly expiries. Report:
   - IV Rank and IV Percentile (30-day window)
   - **IV term structure**: compare near-month IV vs far-month IV for ATM strikes.
     Contango (near < far) = normal; backwardation (near > far) = event risk or
     elevated near-term uncertainty is priced in
   - **Skew analysis**: compare OTM put IV vs OTM call IV (e.g. 25-delta) for the
     nearest monthly expiry. Elevated put skew indicates hedging demand / bearish
     sentiment. Inverted skew (calls > puts) indicates speculative upside demand
   - Put/Call ratio by open interest and by volume
   - Max pain level for each expiry
   - Unusual options activity (UOA): large block trades, sweeps above ask, unusual
     volume relative to open interest
   - Gamma exposure (GEX) by strike — identify the gamma flip level where dealer
     hedging flips from stabilizing to destabilizing
   - Dealer positioning: are dealers long or short gamma at current spot? Long gamma
     = stabilizing (dealers buy low, sell high); short gamma = destabilizing
   - Strike magnets: large OI clusters likely to pin price near expiry

2. Cross-reference options levels with fundamental valuation zones from Phase 2.
   For example: max pain at $X that also sits near DCF fair value → higher significance.

3. **Log this phase** — record:
   - Options data retrieved: expiry dates checked, IV values found
   - Max Pain levels for each expiry with source
   - Put/Call ratios (volume and OI) with values
   - IV Rank / IV Percentile with source
   - Any UOA or block trades detected (strike, size, direction)
   - Dealer gamma positioning (long/short, gamma flip level if available)
   - Key OI clusters at strikes
   - If options data is limited or unavailable for this ticker (common for smaller caps), note this explicitly and explain what was used as proxy (e.g. "GRAB has limited options market; used BS model pricing as approximation")

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

3. **Log this phase** — record:
   - Factor scores computed (momentum, quality, value, growth) with exact values and percentiles
   - Peer universe used for cross-sectional comparison (which stocks, how many)
   - IC/IR results: which factor had highest IC, IC values, IR values
   - Any factors that could NOT be computed and why (e.g. "P/E factor skipped — negative earnings")
   - Contrarian signals identified

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

4. **Log this phase** — record:
   - Backtest config: date range, initial capital, commission, data source used
   - Signal engine code paths (which files were written)
   - Metrics for EACH strategy (A/B/C): total return, Sharpe, max DD, win rate, profit factor, trade count, avg holding days
   - Benchmark return over the same period
   - Which strategy was selected as "best" and why
   - Any backtest failures or errors and how they were resolved
   - Earnings dates hardcoded in the earnings drift strategy
   - Whether the best backtested strategy aligns with the 30-day window

---

### PHASE 7 · Synthesis & Playbook Report

**Skills to load:** `report-generate`, `pine-script`

Compile all phase outputs into the structured playbook below.
Use `report-generate` to produce a polished Markdown report.
Export all indicators to Pine Script via `pine-script`.

**Balance gate — verify BEFORE writing the final report (15 checks):**

- [ ] **Moomoo data integrity**: ALL technical indicators (EMA, RSI, MACD, ATR, ADX, BB, OBV)
  computed from moomoo kline data fetched with `--rehab none`; latest close verified against
  `get_snapshot.py`; daily AND weekly timeframes both calculated
- [ ] DCF sensitivity table present (≥3×3 WACC/growth matrix)
- [ ] **DCF reconciliation**: if base DCF fair value vs market price gap >50%, one of the three
  reconciliation options (A/B/C) is present and credible; DCF is not "decorative"
- [ ] PE band: current percentile vs 5-year min/25th/50th/75th/max explicitly stated
- [ ] PEG formula: numerator (forward/TTM PE) and denominator (EPS/revenue growth rate)
  explicitly stated with data sources
- [ ] Peer comparison table: ≥7 metrics across ≥3 peers
- [ ] DuPont ROE decomposition with ≥2 peer comparisons; non-GAAP adjusted ROE provided
  if GAAP ROE is distorted by acquisition amortization or one-time items
- [ ] Macro section references ≥3 specific indicators with dates (e.g. "core PCE 3.2% YoY, Mar 2026");
  no macro indicator is >2 months stale without a "⚠ Stale" flag
- [ ] Competitive landscape / moat assessment present
- [ ] Revenue concentration analysis present
- [ ] **Insider transaction analysis** present (last 3 months buy/sell data; or explicit
  note that data is unavailable for this market)
- [ ] Scenario probabilities justified by ≥1 fundamental or macro argument each (not just
  technicals); if any Red Flag from the Override Protocol triggered, probabilities
  reflect the adjusted floors
- [ ] **Historical cycle parallels** present in Section 5 — each scenario references the
  closest historical analog
- [ ] Position sizing formula: `position_size = account_risk / (ATR × 1.5)` with default 1% risk;
  **position concentration warning** if single-position notional exceeds 10% of portfolio
- [ ] Earnings date prominently flagged in every section if within the 30-day window

If any checkbox fails, return to the relevant phase and gather the missing data before outputting.

**Compile generation log — after balance gate passes:**

1. Collect the per-phase log entries accumulated during Phases 1–7.
2. Build the consolidated log file at `reports/playbooks/logs/{TICKER}_generation_log_{YYYY-MM-DD}.md`
   following the template in the Generation Log Protocol section.
3. The log MUST include:
   - Phase Summary table with status, time, and tools for all 7 phases
   - Detailed Phase Logs for each phase (all data found, assumptions, gaps)
   - Assumptions Register: every assumption across all phases, consolidated with justifications
   - Data Gaps Register: everything searched for but not found, with proxy values used
   - Tool Call Summary: count of each tool type, which phases used them
   - Balance Gate Results: each of the 15 checkboxes with PASS/FAIL status
4. Save the log file alongside the playbook report.
5. If a phase was skipped or produced PARTIAL results, flag it prominently in the log
   and explain what was missing and why.

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
  - **Historical Parallel**: Closest historical analog where this scenario played out
- **Base Scenario** (~X%): Fundamental anchor + range-bound technical structure
  - **Historical Parallel**: Closest historical analog
- **Bear Scenario** (~X%): Macro shock or fundamental disappointment + breakdown level
  - **Historical Parallel**: Closest historical analog (e.g. "2000 semis: AI hype cycle deflated by rate hikes")

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
Position Size:       X shares at $Y.YY = $Z,ZZZ notional (XX% of $100K portfolio)
                     ATR $X.XX × 1.5 = $X.XX stop width; 1% account risk default
                     ⚠ CONCENTRATION: flag if single-position notional > 10% of portfolio
Portfolio Risk:      {X}% of portfolio at risk (flag if > 10% — single-stock concentration 
                     with beta {B} in a {sector} name is elevated)
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
- Valuation summary (DCF range, PE band percentiles, PEG formula, peer comparison)
- Backtest summary table
- Technical snapshot table (all values from `moomoo-technicals` with `--rehab none`;
  include both daily AND weekly readings; flag any extreme readings per Red Flags Protocol)
- Insider transaction summary (last 3 months; or explicit note if unavailable)
- Pine Script reference code (key levels must match moomoo-computed EMA/BB values)
- **Do NOT duplicate the macro dashboard here** — it is already in Section 1. No section
  should copy another section's content verbatim.

---

## Delivery Checklist

Before finishing, confirm all of the following are complete:

- [ ] **Balance gate passed** (all 15 checkboxes from Phase 7)
- [ ] `report-generate` — Markdown playbook report saved to `reports/playbooks/{TICKER}_30Day_Playbook_{DATE}.md`
- [ ] **Generation log compiled and saved** to `reports/playbooks/logs/{TICKER}_generation_log_{DATE}.md`
  - [ ] Phase Summary table complete for all 7 phases
  - [ ] Assumptions Register consolidated
  - [ ] Data Gaps Register consolidated
  - [ ] Tool Call Summary complete
  - [ ] Balance Gate Results (15 checkboxes) recorded
- [ ] `pine-script` — TradingView Pine Script v6 exported with all indicators
- [ ] Strategy code from Phase 6 saved via `write_file`
- [ ] All key levels from Section 4 are in the Pine Script as horizontal lines
- [ ] **No section duplicates another section's content verbatim** (e.g. macro dashboard
  in Section 1 only, not repeated in Section 10)
- [ ] **DCF reconciliation present** if market price vs base DCF gap >50%
- [ ] Fundamental + Macro sections comprise at least 40% of the total report length
  (not including appendix/data tables). If technical sections dominate, re-expand
  Phases 1 and 2.
- [ ] **Red Flags from the Override Protocol are explicitly addressed** in the report
  — not ignored or minimized

---

## Notes for the Agent

### Process & Data Integrity

- **Ticker required.** If the user has not specified a ticker, ask before starting.
- **Market inference.** Determine `{market}` from the ticker format:
  `.US` suffix → US, `.HK` → Hong Kong, `.SZ`/`.SH` → China A-share, `-USDT` → crypto.
  This drives data source selection, macro analysis focus, and flow tools.
- **Phases 1 and 2 come first for a reason.** They are the foundation. A playbook
  that has a detailed Elliott Wave count but no DCF sensitivity table is unbalanced.
  If you find yourself spending more time on Phase 3 than Phases 1+2 combined, stop
  and rebalance.
- **Technical data MUST come from moomoo with `--rehab none`.** The `moomoo-technicals`
  skill documents a critical bug: moomoo's default forward-rehab adjustment distorts
  historical prices, making EMA/RSI/MACD/BB/ATR calculations wrong. The GOOGL playbook
  audit found EMA 20 off by $27 (7.5%), BB Lower off by $57 (19%), and ATR off by 21%
  when this rule was not followed. Every kline fetch must use `--rehab none`, and the
  latest close must be verified against `get_snapshot.py`. Do NOT use yfinance or any
  other data source for technical indicators — only moomoo with `--rehab none`.
- **Data freshness matters.** Always use the most recent available data. If `yfinance`
  returns data more than 1 trading day stale, warn the user. If any macro indicator
  is >2 months old, flag it with "⚠ Stale" in the dashboard.

### Valuation & DCF

- **DCF reconciliation is mandatory when the gap exceeds 50%.** The AMD playbook audit
  found a DCF base fair value of $96 vs a market price of $455 — a 79% overvaluation
  signal that was hand-waved away in one sentence. This is forbidden. If DCF and the
  market fundamentally disagree, you MUST either fix the DCF assumptions (with documented
  justification), explain via reverse DCF what the market is pricing, or admit DCF
  cannot value this company and remove it. The DCF section must be useful or absent —
  never decorative.
- **Non-GAAP ROE is required when GAAP is distorted.** If the company has large
  acquisition-related amortization (e.g. AMD Xilinx, Salesforce acquisitions), compute
  and present both GAAP and non-GAAP ROE. Large GAAP/non-GAAP divergence is itself a
  signal about accounting quality.
- **PEG must be transparent.** Always state the exact numerator (forward PE or TTM PE)
  and denominator (EPS growth or revenue growth). Use the same definition for all peers
  in the comparison table.

### Scenarios & Probabilities

- **Probability weights must sum to 100%.** Each scenario must have at least one
  fundamental or macro justification — not purely technical.
- **Red Flags from the Override Protocol override scenario probability defaults.**
  When RSI daily > 80 or weekly > 85, the Bear scenario floor rises to 20%. When two
  or more Red Flags fire simultaneously, Bull is capped at 30% and Bear floor is 20%.
  When three or more fire, the report must open with a "Risks Outweigh Rewards" warning.
- **Each scenario must include a historical parallel.** If "this time is different"
  is the thesis, state it explicitly with the concrete structural difference.

### Position Sizing & Risk

- **Sizing guidance** uses ATR(14)-based volatility sizing:
  `position_size = (account_risk_per_trade) / (ATR × 1.5)`. Default to 1% account risk
  per setup unless the user specifies otherwise. Use the ATR value computed from
  moomoo `--rehab none` data — not estimated or pulled from another source.
- **Flag concentration risk.** If a single trade setup's notional exceeds 10% of the
  assumed portfolio ($100K default), add a ⚠ concentration warning. High-beta names
  (β > 2.0) compound this risk.
- **ATR expansion >3× in 60 days invalidates historical backtests.** When volatility
  regime changes, note this prominently in Phase 6. Backtests using pre-expansion data
  no longer represent the current trading environment.

### Consistency & Quality

- **If earnings fall within the 30-day window**, flag this prominently in every section —
  it is the single highest-impact event and should anchor the Week-by-Week calendar.
- **Peer selection**: Use direct competitors in the same industry and of comparable scale.
  Do not compare a $50B company to a $5T company as a "peer."
- **No duplicate content.** The macro dashboard belongs in Section 1 only — do not
  repeat it verbatim in Section 10. Duplication reads as padding and undermines trust.
- **Insider transactions must be checked.** When a stock is at ATH, insider selling
  is one of the most reliable sentiment signals available. Do not skip this check.
- **The report is not a marketing document for your thesis.** If the evidence is
  mixed, the report should be mixed. If the risks outweigh the rewards, say so.
  A playbook that advises no action because risk/reward is unfavorable is a valid
  and honest playbook.
- **Disclaimer:** Append to the final report — *"This playbook is for research and
  educational purposes only. It does not constitute investment advice. Past backtest
  performance does not guarantee future results."*
