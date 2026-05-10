---
name: playbook-pulse
description: >
  Takes the pulse of an active 30-day playbook — fetches current price data via
  moomoo API (--rehab none), recalculates all technical indicators on daily and
  weekly timeframes, compares against the original playbook's levels and setups,
  assesses what changed, and produces a week-ahead action plan. Use this skill
  whenever the user asks for a "pulse check," "daily update," "what should I do
  today with {ticker}," "how's my {ticker} playbook looking," "update the
  strategy for {ticker}," or any request to reassess a stock against its existing
  playbook based on current market data.
---

# Playbook Pulse

Takes the vital signs of an active 30-day playbook — recalculates all technicals
from raw moomoo data, compares against the playbook baseline, and produces
actionable guidance for the week ahead.

**Key principle**: Never fabricate data. All indicators must be calculated from
live moomoo API data with `--rehab none`. If data is unavailable, log the gap.

## Workflow (execute in order)

### Phase 1 — Locate the Playbook

Find the most recent playbook for the ticker:
```
reports/playbooks/{TICKER}_30Day_Playbook_*.md
```

Read Sections 4-9 to extract the baseline:
- **Section 4**: Key price levels (supports, resistances, targets, invalidation)
- **Section 5**: Scenario probabilities and triggers
- **Section 6**: Week-by-week calendar — which week are we in?
- **Section 7**: Active trade setups with entry zones, stops, targets
- **Section 8**: Risk events calendar — what's the next binary event?
- **Section 9/10**: Technical snapshot baseline values

Note the playbook date, the price at that time, and which calendar week is current.

### Phase 2 — Fetch Current Data

Always `--rehab none`, always filter with `grep`:

```bash
# Daily kline (250 bars for 200 EMA)
python ~/.claude/skills/moomooapi/scripts/quote/get_kline.py US.{TICKER} \
  --ktype 1d --num 250 --rehab none --json 2>&1 \
  | grep '^{"code"' > /tmp/{ticker}_daily.json

# Weekly kline (100 bars)
python ~/.claude/skills/moomooapi/scripts/quote/get_kline.py US.{TICKER} \
  --ktype 1w --num 100 --rehab none --json 2>&1 \
  | grep '^{"code"' > /tmp/{ticker}_weekly.json

# Snapshot for price verification
python ~/.claude/skills/moomooapi/scripts/quote/get_snapshot.py US.{TICKER} --json 2>&1 \
  | grep '^{"data"'
```

Verify latest kline close matches snapshot price. If they diverge, trust the snapshot.

### Phase 3 — Calculate All Technicals

Run the full indicator suite from `moomoo-technicals/SKILL.md` on both timeframes:

**Daily:**
- EMA 20, 50, 200 — alignment (20 > 50 > 200? price above all?)
- RSI(14) — Wilder's smoothing, check overbought/oversold thresholds
- MACD(12,26,9) — line, signal, histogram, cross detection
- ADX(14) — +DI/-DI spread, trend strength (>25 = strong, <20 = weak)
- ATR(14) — daily range context
- Bollinger Bands (20,2) — %B position, upper/lower band
- Stochastic(14,3) Fast — %K, %D

**Weekly:**
- RSI(14), MACD, EMA 20/50
- Compare against daily for timeframe alignment/divergence

Full code for every indicator is in `.claude/skills/moomoo-technicals/SKILL.md`
under "Calculating Indicators (full working code)".

### Phase 4 — Before/After Comparison

Side-by-side table against the playbook baseline:

| Indicator | Playbook (date, $price) | Now (date, $price) | Delta | Signal |
|-----------|--------------------------|---------------------|-------|--------|

Flag any playbook values that appear wrong when independently recalculated.
The playbook may have used adjusted data — trust the `--rehab none` calculation.

### Phase 5 — Key Levels Check

Every level from playbook Section 4, sorted by price descending:

```
$XXX.XX  +X.X%  Description        RESIST / SUPPORT / BROKEN
```

Identify: levels breached since playbook, next resistance, next support,
and whether the invalidation level is still safe.

### Phase 6 — Trade Setup Assessment

Per-setup status from playbook Section 7:

| Setup | Entry Zone | Status | Action |
|-------|-----------|--------|--------|

For each: is the entry zone still reachable? Stop hit? Target reached? Thesis intact?
If entry zones are missed, suggest alternatives — never recommend chasing.

### Phase 7 — Week-Ahead Action Plan

Day-by-day table for the upcoming trading week, factoring in:
- Playbook Section 6 calendar (which week are we in?)
- Playbook Section 8 risk events (binary events = size down)
- OPEX pinning, gamma effects
- Pre/post earnings posture

### Phase 8 — Options Context

Use `mcp__vibe-trading__analyze_options` to price a few relevant strikes:
- ATM call for near-term expiry (delta context)
- OTM put at key support (hedge cost — is insurance cheap?)

Mention if protective puts are attractively priced for binary event hedging.

### Phase 9 — Bottom Line

One tight paragraph: technical upgrade or downgrade since playbook? Single
highest-conviction action right now? What would flip the thesis?

## Output

Save to:
```
reports/daily-update/{TICKER}_Daily_Update_{YYYY-MM-DD}.md
```

### Report Template

```markdown
# {TICKER} Daily Update — {DATE}

> **Source Playbook**: [link](../playbooks/{file})
> **Playbook Date**: {date} (close ${price})
> **Latest Close**: ${price} ({date}) — **{+/-}X.X% since playbook**
> **Days to Earnings**: {N} ({date})
> **Next Catalyst**: {event} — {date} ({N} trading days)

---

## 1. Price Action Summary
(3-5 lines: direction, volume, levels broken since last check)

## 2. Technical Snapshot

### Daily
(Full indicator table: playbook vs now vs delta vs signal)

### Weekly
(Weekly table, timeframe alignment note)

## 3. Key Levels Check
(Level-by-level, distance from current price, status)

## 4. Trade Setup Assessment
(Per-setup table with status and specific actions)

## 5. {Week} Week Action Plan
(Day-by-day table: events and prescribed actions)

## 6. Risk Considerations
(Bulleted list of specific near-term risks)

## 7. Bottom Line
(One paragraph: what to do, conviction trade, invalidation condition)

---

*Generated {date}. Data: moomoo OpenD API (--rehab none). Not investment advice.*
```

## Cross-Reference

- Indicator implementations: `.claude/skills/moomoo-technicals/SKILL.md`
- Data fetching: `~/.claude/skills/moomooapi/scripts/quote/get_kline.py`
- Snapshot verification: `~/.claude/skills/moomooapi/scripts/quote/get_snapshot.py`
- Options pricing: vibe-trading MCP `analyze_options`
