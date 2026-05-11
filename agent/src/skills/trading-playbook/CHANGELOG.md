# Changelog

## 0.2.0 — 2026-05-11

### Added

- **Red Flags & Override Protocol**: 9 objective thresholds (RSI >80, price >BB upper, DCF gap >50%, ADX >45, ATR 3× expansion, insider selling at ATH, macro data staleness, etc.) with mandatory actions. Two+ flags trigger probability caps; three+ require a "Risks Outweigh Rewards" warning at the report introduction.
- **DCF reconciliation rule** (Phase 2): when DCF fair value vs market price gap exceeds 50%, the agent must either adjust assumptions with documented justification, reconcile via reverse DCF, or reject DCF entirely. Presenting a DCF that implies severe overvaluation and then dismissing it in one sentence is explicitly prohibited.
- **Historical cycle parallels** (Phase 1, step 7): mandatory 1-2 historical analogs for the sector, compared to current conditions. Each scenario in Section 5 must reference its closest historical analog.
- **Insider transaction analysis** (Phase 2, step 8): last 3 months buy/sell data mandatory for all tickers. Flag if insiders selling at ATH with >3:1 ratio, or if CEO/CFO sold in last 30 days.
- **Non-GAAP ROE requirement** (Phase 2): both GAAP and non-GAAP ROE must be presented when GAAP is distorted by acquisition amortization or one-time items.
- **PEG transparency** (Phase 2): exact numerator and denominator must be stated with data sources. Same growth rate definition required across all peers.
- **Extreme reading protocol** (Phase 3): mandatory flagging when RSI daily >80, weekly >85, ADX >45, or price >BB upper. Flags must propagate to Sections 3, 5, 8, and 10.
- **IV term structure and skew analysis** (Phase 4): contango vs backwardation check, OTM put vs call IV comparison.
- **Data staleness check** (Phase 1): any macro indicator >2 months old must carry a "⚠ Stale" flag in the dashboard.
- **Portfolio concentration warning** (Section 7): flag when single-position notional exceeds 10% of portfolio, especially for high-beta names.
- **Post-earnings analyst revision tracking** (Phase 2): flag when analyst targets are stale (pre-earnings).

### Changed

- **Balance gate**: expanded from 11 to **15 checkboxes** (added: DCF reconciliation, PEG formula transparency, insider transactions, historical cycle parallels, position concentration warning).
- **Output structure**: Section 10 no longer duplicates the macro dashboard from Section 1 (was padding). Added insider transaction summary to Section 10.
- **Notes for the Agent**: reorganized into 5 subsections (Process & Data Integrity, Valuation & DCF, Scenarios & Probabilities, Position Sizing & Risk, Consistency & Quality) with 15 new rules.
- **Phase 1 logging**: added data staleness check, historical cycle research logging.
- **Phase 2 logging**: added non-GAAP ROE, DCF reconciliation method, PEG formula components, insider transaction data.
- **Delivery checklist**: added DCF reconciliation check, Red Flags explicit-address check, no-duplicate-content check.
- Evidence weighting now subject to Red Flags override — technical extremes and valuation disconnects can override the normal fundamental-first weighting.

### Fixed

- Phase 2 step numbering properly reflects the 9 steps (was previously inconsistent).
- All balance gate count references synced (template, phase instructions, delivery checklist).
- Agent skill definition now matches the `.claude` user-facing skill definition exactly (previously `agent/src` was stale, missing `moomoo-technicals` data integrity rules and using `technical-basic`).

---

## 0.1.0 — 2026-05-10

### Added

- Initial 7-phase pipeline: Macro & Industry, Deep Fundamentals & Valuation, Technical Analysis, Options & Flow Intelligence, Multi-Factor & Quant Scoring, Backtest Signal Validation, Synthesis & Report.
- 10-section output structure: Macro Context, Fundamental Deep Dive, Composite Scorecard, Key Price Levels, Scenario Analysis, Week-by-Week Calendar, Trade Setups, Risk Events Calendar, Daily Monitoring Checklist, Data Appendix.
- Generation log protocol with audit trail (data found, assumptions, gaps, tool calls).
- ATR-based position sizing with 1% default account risk.
- Dual-confirmation level annotation (technical + fundamental confluence).
- Pine Script export for key levels.
- Moomoo `--rehab none` data integrity rules (audited against GOOGL playbook where EMA 20 was off by 27 when this rule was not followed).
