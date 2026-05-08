---
name: etf-top10-portfolio
description: >
  Given any ETF ticker (e.g. QQQ, SMH, SPY, SOXX, XLK, 510300.SH, 2800.HK), extracts
  the ETF's full constituent holdings, scores every stock across momentum, quality,
  value, growth, and technical factors, selects the top 10 highest-conviction names,
  and produces a portfolio allocation with position-sizing weights, correlation
  analysis, risk budgeting, and a ready-to-act report. Trigger this skill whenever
  the user asks to: pick top stocks from an ETF, find the best holdings inside an ETF,
  build a concentrated portfolio from an index, allocate a bucket across ETF stocks,
  rank constituents, or says anything like "give me the top 10 from [ETF]",
  "which stocks in [ETF] should I hold", or "build me a portfolio from [ETF]".
  Works for US, HK, A-share, and global ETFs. Fully orchestrates etf-analysis,
  multi-factor, factor-research, technical-basic, sector-rotation, asset-allocation,
  options-strategy, macro-analysis, us-etf-flow, and backtest.
---

# ETF Top-10 Portfolio Builder

Given any ETF, this skill runs a full agentic pipeline to identify the 10 highest-
conviction constituent stocks and recommends how to size each position in a portfolio
bucket. Output is a scored leaderboard, a correlation-adjusted allocation table, and
a one-page portfolio brief.

**Execution requirement:** The agent MUST execute every phase below in strict
order. Do not skip, reorder, or shortcut any phase. Do not fabricate data, skip
a phase because data is hard to find, or make up scores without running the named
tools and loading the named skills. Every phase produces mandatory inputs for the
next. If you are tempted to shortcut, log the gap instead — never fake it.

---

## Input

The user provides:
- **ETF ticker** — e.g. `QQQ`, `SMH`, `SOXX`, `SPY`, `XLK`, `GLD`, `510300.SH`, `2800.HK`
- *(Optional)* **Portfolio size** — total capital in USD/HKD/CNY to size positions
- *(Optional)* **Risk appetite** — Conservative / Balanced / Aggressive (default: Balanced)
- *(Optional)* **Horizon** — 1 month / 3 months / 6 months (default: 1 month)

If any optional parameter is missing, use the defaults. Do not ask the user — proceed
and state assumptions inline.

**Data accuracy is mandatory.** Every data point in the report MUST be traceable
to a tool call or web source. If data cannot be found, record it as a data gap in
the generation log (see Generation Log Protocol below) — do not fabricate or infer
without clearly stating the assumption and its justification.

---

## Generation Log Protocol

Every portfolio builder invocation MUST produce a companion generation log that
records exactly how the portfolio was built — what data was found, what tools
were called, what assumptions were made, and what gaps exist. The log is the
audit trail.

**Log file path**: `reports/etf-portfolio/logs/{ETF}_generation_log_{YYYY-MM-DD}.md`

**Log structure**:

```markdown
# {ETF} Portfolio Generation Log — {YYYY-MM-DD}

**Generated at**: {timestamp} | **Total phases**: 8 | **Total tool calls**: N

## Phase Summary

| Phase | Status | Time | Tools Used |
|-------|--------|------|------------|
| 1. ETF Deconstruction | COMPLETE | ~Xm | ... |
| 2. Multi-Factor Scoring | COMPLETE | ~Xm | ... |
| 3. Technical Deep-Dive | COMPLETE | ~Xm | ... |
| 4. Fundamental Validation | COMPLETE | ~Xm | ... |
| 5. Macro & Sector Overlay | COMPLETE | ~Xm | ... |
| 6. Options Flow Sanity Check | COMPLETE | ~Xm | ... |
| 7. Portfolio Construction & Allocation | COMPLETE | ~Xm | ... |
| 8. Report Output | COMPLETE | ~Xm | ... |

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
(Pass/fail for each of the 10 checkboxes)
```

**At the START of each phase**, note the phase number, name, and start time.
**At the END of each phase**, record the log entry following the template above.
Accumulate all entries and write the final log file in Phase 8 (Report Output).

---

## Execution Pipeline

Work through each phase in strict order. Load each named skill before executing
that phase. Complete each phase fully before moving on. Do not skip, reorder, or
shortcut any phase — the output is only as reliable as the weakest phase.

### PHASE 1 · ETF Deconstruction

**Skills:** `etf-analysis`, `data-routing`, `yfinance`, `us-etf-flow`

1. **Holdings extraction** — Via `etf-analysis`:
   - MUST fetch the ETF's full constituent list with weights (use `yfinance` or `akshare`
     for A-share ETFs, or `web_search` + `read_url` to scrape the fund provider's
     holdings page if the API doesn't cover it)
   - Record each holding's: ticker, name, sector, current weight (%), market cap
   - If the ETF has >50 holdings, pre-filter to the top 40 by ETF weight before
     running the full scoring pipeline — log this filter clearly

2. **ETF flow intelligence** — Via `us-etf-flow`:
   - Net ETF fund flows (30-day): is smart money adding or redeeming?
   - Premium/discount to NAV: is the ETF itself trading rich or cheap?
   - Identify if any single sector is dominating inflows within the ETF

3. **Peer context** — Fetch 30-day price return for the ETF itself vs. its benchmark
   index (e.g. QQQ vs. Nasdaq-100). Record the ETF's current momentum regime
   (trending up / ranging / trending down).

---

### PHASE 2 · Multi-Factor Scoring of All Constituents

**Skills:** `multi-factor`, `factor-research`, `technical-basic`

Score EVERY constituent on the following five factors. This is mandatory — do not
skip any factor or any stock. Use `get_market_data` to pull
the underlying data. For each stock, produce a score from 0–100 per factor.

#### Factor Definitions

| Factor | Weight | What to Measure |
|--------|--------|-----------------|
| **Momentum** | 25% | 3M, 6M, 12M-1M price return; RS rank within ETF universe |
| **Quality** | 20% | ROE, ROIC, gross margin, interest coverage, revenue stability |
| **Growth** | 20% | Revenue growth YoY, EPS revision trend (up/flat/down), forward EPS CAGR |
| **Value** | 15% | P/E, P/FCF, EV/EBITDA vs. sector median; discount to fair value |
| **Technical** | 20% | Price vs. 20/50/200 EMA; RSI(14) zone; MACD signal; ADX trend strength |

#### Scoring Method

- Rank each constituent within the ETF universe on each factor (percentile rank)
- Compute **Composite Score** = weighted sum of 5 factor percentile ranks
- Flag any stock where ≥3 factors are top-quartile → **High Conviction**
- Flag any stock where ≥2 factors are bottom-quartile → **Avoid**

Via `factor-research`: run a quick IC (Information Coefficient) check — which factors
have been most predictive of next-month returns in this ETF's sector historically?
Upweight those factors by +5% and rebalance the weights accordingly before finalising
scores. Document the adjusted weights used.

---

### PHASE 3 · Technical Deep-Dive on Top 15 Candidates

**Skills:** `technical-basic`, `candlestick`, `smc`

After Phase 2, MUST take the top 15 by Composite Score. For each, run ALL of:

1. **Trend check** — Is price above 20 EMA, 50 EMA, 200 EMA? (1 point each → max 3)
2. **Momentum check** — RSI(14) between 45–70 (healthy trend, not overbought)? MACD histogram rising?
3. **Structure check** — Via `smc`: any nearby Order Block acting as support?
   Any unfilled Fair Value Gap below current price (magnet risk)?
4. **Pattern check** — Via `candlestick`: any high-reliability bullish pattern on
   the daily in the last 10 sessions?

Assign a **Technical Bonus Score** (0–10) per stock. Add to Composite Score (scaled).

Final ranked list → select **Top 10** by adjusted composite score.

---

### PHASE 4 · Fundamental Validation of Top 10

**Skills:** `financial-statement`, `edgar-sec-filings`, `earnings-forecast`,
`valuation-model`

For each of the 10 selected stocks, you MUST run ALL of these fundamental checks:

| Check | Pass Condition | Action if Fail |
|-------|---------------|----------------|
| Earnings trend | EPS growing for ≥2 consecutive quarters | Flag; reduce weight by 30% |
| Balance sheet | Debt/Equity < sector 75th percentile | Flag; reduce weight by 20% |
| Upcoming earnings | Next earnings date > 7 days away | Flag as "earnings risk"; add warning |
| Analyst consensus | ≥60% Buy ratings | Flag if below |
| Valuation | Not trading >50% above DCF fair value | Flag as "expensive"; reduce weight by 20% |

Record pass/fail for each check. Any stock that fails 3+ checks → replace with
rank #11 from Phase 3, and run Phase 4 on it.

---

### PHASE 5 · Macro & Sector Overlay

**Skills:** `macro-analysis`, `sector-rotation`, `global-macro`

1. **Sector rotation check** — Via `sector-rotation`:
   - Which sectors are in early/late expansion or contraction right now?
   - Does the sector composition of the Top 10 align with the current regime?
   - If a sector is in contraction: flag all stocks from that sector;
     consider capping their weight at 8% regardless of score

2. **Macro tailwinds/headwinds** — Via `macro-analysis`:
   - Fed rate path: does current trajectory favour growth or value tilt?
   - USD strength: impact on international-revenue-heavy names in the Top 10?
   - Any sector-specific regulatory or macro risk (e.g. AI chip export controls,
     energy policy, rate sensitivity for financials)?

3. Apply a **Macro Adjustment** (+/- 0 to 10 points) to each stock's final score
   based on macro alignment. Document each adjustment.

---

### PHASE 6 · Options Flow Sanity Check

**Skills:** `options-strategy`

For each of the Top 10, you MUST pull a full options snapshot:
- Put/Call ratio (volume): is it >1.3? (bearish signal — flag)
- Any unusual bearish sweep in the last 5 trading days? (flag)
- IV Rank: if >80, the market is pricing in elevated risk — flag and note

Stocks with bearish options flags are not removed but their position weight is
capped at **8%** as a risk control.

---

### PHASE 7 · Portfolio Construction & Allocation

**Skills:** `asset-allocation`, `multi-factor`

#### Step 1 — Base Weights (Score-Proportional)

MUST compute:
```
raw_weight[i] = composite_score[i] / sum(composite_score[1..10])
```

#### Step 2 — Correlation Adjustment

Use `get_market_data` to fetch 90-day daily returns for all 10 stocks.
Compute pairwise correlation matrix.

- If any pair has correlation > 0.85: reduce both to 75% of their raw weight
  (cap concentration in highly correlated pairs)
- Group by sector: no sector should exceed **35%** of total portfolio weight

#### Step 3 — Volatility Scaling (Risk Parity Overlay)

Compute ATR(14) as a proxy for volatility.
Apply inverse-volatility tilt:

```
vol_adj_weight[i] = raw_weight[i] × (1 / ATR_pct[i])
renormalize so weights sum to 100%
```

This ensures lower-volatility names are not under-weighted vs. high-flyers.

#### Step 4 — Apply Caps & Floors

- **Maximum weight** per stock: 20% (Aggressive), 15% (Balanced), 12% (Conservative)
- **Minimum weight** per stock: 5% (drop below this → remove and redistribute)
- Re-normalise after applying caps and floors

#### Step 5 — Dollar Sizing (if capital provided)

```
dollar_allocation[i] = total_capital × final_weight[i]
shares[i] = floor(dollar_allocation[i] / current_price[i])
```

Round down to whole shares. Report residual cash.

---

### PHASE 8 · Report Output

**Skills:** `report-generate`

**Balance gate — verify BEFORE compiling the report:**

- [ ] ETF holdings extracted with full weight table (Phase 1)
- [ ] All 5 factors scored for each constituent with percentile ranks (Phase 2)
- [ ] Technical deep-dive run on top 15 candidates with Technical Bonus Score applied (Phase 3)
- [ ] Fundamental checks completed for top 10; replacements made for any stock failing 3+ checks (Phase 4)
- [ ] Macro & sector overlay applied with documented adjustments per stock (Phase 5)
- [ ] Options flow checked for all top 10; bearish flags applied as weight caps (Phase 6)
- [ ] Correlation-adjusted allocation computed with caps, floors, and volatility scaling (Phase 7)
- [ ] Risk budgeting complete: HHI reported, largest risk contributor identified (Phase 7)
- [ ] Portfolio weights respect sector 35% cap and individual caps per risk profile (Phase 7)
- [ ] Generation log compiled with all 8 phases documented (see Generation Log Protocol)

If any checkbox fails, return to the relevant phase and complete it before assembling the report.

Compile into a structured report with these sections:

---

## Output Structure

### SECTION 1 — ETF Snapshot

| Field | Value |
|-------|-------|
| ETF Ticker | |
| ETF Name | |
| # of Holdings | |
| 30-Day ETF Return | |
| 30-Day Flow (Net) | Inflow / Outflow $Xm |
| Premium/Discount to NAV | |
| Macro Regime | Risk-On / Risk-Off / Neutral |
| Dominant Sector | |

---

### SECTION 2 — Full Constituent Scorecard (Top 15)

| Rank | Ticker | Name | Sector | Momentum | Quality | Growth | Value | Technical | Composite | Selected |
|------|--------|------|--------|----------|---------|--------|-------|-----------|-----------|----------|
| 1 | | | | | | | | | | ✅ |
| 2 | | | | | | | | | | ✅ |
| ... | | | | | | | | | | |
| 15 | | | | | | | | | | ❌ |

Scores out of 100. Green = top quartile. Red = bottom quartile.

---

### SECTION 3 — Top 10 Deep Profiles

For each selected stock (one block per stock):

```
Ticker:           [e.g. NVDA]
Name:             NVIDIA Corporation
Sector:           Technology — Semiconductors
ETF Weight:       X.X%
---
WHY SELECTED
Momentum:         [1-line summary — e.g. "Top decile 6M return, RS rank #2 in ETF"]
Quality:          [1-line — e.g. "ROIC 42%, gross margin 74%, no debt concerns"]
Growth:           [1-line — e.g. "Revenue +78% YoY, EPS revised up 3x in 90 days"]
Value:            [1-line — e.g. "Premium to sector but justified by growth rate"]
Technical:        [1-line — e.g. "Price above all EMAs, RSI 58, MACD bullish cross"]
Options Flow:     [1-line — e.g. "P/C 0.7, call sweep $12M last week — bullish"]
Macro Fit:        [1-line — e.g. "AI capex supercycle intact, no export risk to this SKU"]
---
KEY RISKS:        [2-3 bullet risks]
WATCH LEVEL:      Stop idea invalidated if price closes below $XXX
```

---

### SECTION 4 — Portfolio Allocation Table

| # | Ticker | Sector | Score | Base Wt% | Vol-Adj Wt% | Final Wt% | $ Amount | # Shares |
|---|--------|--------|-------|----------|-------------|-----------|----------|----------|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| ... | | | | | | | |
| | **TOTAL** | | | 100% | 100% | **100%** | **$X** | — |

Residual cash: $X (X%)

---

### SECTION 5 — Correlation Heatmap (Text)

List the 5 highest-correlation pairs in the portfolio and how weights were adjusted:

| Pair | Correlation | Action Taken |
|------|-------------|-------------|
| NVDA ↔ AMD | 0.91 | Both capped; combined weight ≤ 25% |
| ... | | |

Overall portfolio average pairwise correlation: X.XX (target: < 0.65)

---

### SECTION 6 — Sector Allocation Summary

| Sector | Stocks | Combined Weight | Regime Signal | Cap Applied? |
|--------|--------|----------------|---------------|-------------|
| Technology | 4 | 48% | Expansion | No |
| ... | | | | |

---

### SECTION 7 — Risk Budget

| Stock | Final Weight | Volatility (ATR%) | Risk Contribution | % of Portfolio Risk |
|-------|-------------|-------------------|-------------------|---------------------|
| | | | | |
| **Total** | 100% | — | — | 100% |

Largest single risk contributor: [ticker] at X% of portfolio risk.
Herfindahl-Hirschman Index (HHI) of weights: X (< 1500 = well diversified).

---

### SECTION 8 — Bull / Bear Scenarios

**Bull case (X% probability):**
- Trigger: [macro/sector catalyst]
- Expected portfolio return vs. ETF: +X% vs. +X%
- Top contributor: [ticker]

**Base case (X% probability):**
- Expected portfolio return vs. ETF: +X% vs. +X%

**Bear case (X% probability):**
- Trigger: [risk event]
- Expected portfolio drawdown: -X%
- Hedge suggestion: [options put on ETF itself / reduce highest-beta name]

---

### SECTION 9 — Monitoring Checklist

Weekly review triggers (re-run scoring if any of these occur):
- [ ] Any Top-10 stock reports earnings → validate thesis post-print
- [ ] ETF flow turns negative for 2 consecutive weeks → reassess
- [ ] Portfolio drawdown exceeds 8% → invoke risk committee review
- [ ] Any stock drops below its Watch Level (from Section 3) → exit
- [ ] Sector rotation signal flips for a dominant sector → rebalance

**Compile generation log — after balance gate passes:**

1. Collect the per-phase log entries accumulated during Phases 1–8.
2. Build the consolidated log file at `reports/etf-portfolio/logs/{ETF}_generation_log_{YYYY-MM-DD}.md`
   following the template in the Generation Log Protocol section.
3. The log MUST include:
   - Phase Summary table with status, time, and tools for all 8 phases
   - Detailed Phase Logs for each phase (all data found, assumptions, gaps)
   - Assumptions Register: every assumption across all phases, consolidated with justifications
   - Data Gaps Register: everything searched for but not found, with proxy values used
   - Tool Call Summary: count of each tool type, which phases used them
   - Balance Gate Results: each of the 10 checkboxes with PASS/FAIL status
4. Save the log file alongside the portfolio report.
5. If a phase was skipped or produced PARTIAL results, flag it prominently in the log
   and explain what was missing and why.

---

## Delivery Checklist

- [ ] `report-generate` — Markdown report saved to `reports/etf-portfolio/{ETF}_Top10_Report_{YYYY-MM-DD}.md`
- [ ] Allocation table exported via `write_file` as CSV
- [ ] All 10 tickers + weights ready to paste into any broker interface
- [ ] **Generation log compiled and saved** to `reports/etf-portfolio/logs/{ETF}_generation_log_{YYYY-MM-DD}.md`
  - [ ] Phase Summary table complete for all 8 phases
  - [ ] Assumptions Register consolidated
  - [ ] Data Gaps Register consolidated
  - [ ] Tool Call Summary complete
  - [ ] Balance Gate Results recorded

---

## Notes for the Agent

- **ETF holdings freshness**: If `etf-analysis` or `yfinance` cannot fetch constituents
  directly, use `web_search` + `read_url` to scrape from etf.com, ishares.com,
  invesco.com, or the relevant fund provider page. Always state the data date.

- **A-share ETFs** (e.g. `510300.SH`, `510500.SH`): route through `akshare` for
  holdings data. Apply `ashare-pre-st-filter` before scoring to remove ST/\*ST
  candidates from the universe automatically.

- **HK ETFs** (e.g. `2800.HK`, `3033.HK`): route through `akshare` or `futu` loader.

- **Small ETFs** (<20 holdings): skip the pre-filter in Phase 1 and score all holdings.

- **If capital is not provided**: present allocation as percentages only.
  Add a note: "To get dollar amounts and share counts, tell me your total capital."

- **Output paths**: Save the report to `reports/etf-portfolio/{ETF}_Top10_Report_{YYYY-MM-DD}.md`
  and the generation log to `reports/etf-portfolio/logs/{ETF}_generation_log_{YYYY-MM-DD}.md`.
  Do not use any other output directory.

- **Rebalancing cadence**: recommend monthly rebalance for Aggressive,
  quarterly for Balanced/Conservative.

- **Enforcement:** This skill is a mandatory sequential pipeline. Skipping a phase,
  fabricating data, or shortcutting the process produces an invalid report. If you
  are tempted to skip a phase because data is hard to get, log the gap and use the
  best available proxy — do not omit the phase.

- **Disclaimer**: append to all reports — *"This output is for research and educational
  purposes only. It does not constitute investment advice. Past factor performance
  does not guarantee future results."*
