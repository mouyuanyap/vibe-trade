# vibe-trade

AI-assisted trading research workspace — generates institutional-grade trading playbooks, ETF portfolio allocations, and daily pulse checks using [Claude Code](https://claude.ai/code) with deepseek-v4-pro. Market data via [moomoo OpenAPI](https://openapi.moomoo.com/moomoo-api-doc/en/intro/intro.html). Trading tools (backtest, options analysis, factor scoring, etc.) provided by the [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) MCP server (6.7k stars).

## How It Works

```
Claude Code (deepseek-v4-pro)
  └─ .claude/skills/           # Skill definitions (agentic pipelines)
       └─ vibe-trading MCP      # HKUDS/Vibe-Trading MCP server
            ├── backtest        # Vectorized backtesting engine
            ├── analyze_options # Black-Scholes pricing & Greeks
            ├── factor_analysis # Factor IC/IR & layered backtests
            ├── get_market_data # OHLCV from yfinance/akshare/ccxt
            ├── pattern_recog   # Chart pattern detection
            ├── read_url        # Web content extraction
            └── web_search      # DuckDuckGo search
  └─ moomoo OpenD API           # Raw kline data (--rehab none)
```

1. **Skills** define multi-phase agentic pipelines that Claude Code executes step-by-step — macro research, fundamental deep dives, technical indicator calculation, options flow analysis, factor scoring, and backtest validation
2. **Vibe-Trading MCP** exposes the trading toolchain (backtest engine, options pricing, factor analysis, pattern recognition) as MCP resources callable from skills
3. **Moomoo OpenD API** provides raw OHLCV market data via `get_kline.py` with `--rehab none` (forward-rehab adjustment distorts historical prices, making indicators wrong)
4. **Reports** compile everything into structured markdown with Pine Script v6 reference code, trade setups with position sizing, and week-by-week action calendars

## Skills (`.claude/skills/`)

| Skill | Description |
|-------|-------------|
| [trading-playbook](.claude/skills/trading-playbook/SKILL.md) | 30-day institutional-grade trading playbook for any stock — macro, fundamentals (DCF/PE-band/DuPont), technicals (moomoo `--rehab none`), options flow, quant factors, backtested setups |
| [etf-top10-portfolio](.claude/skills/etf-top10-portfolio/SKILL.md) | Extract ETF holdings, score every constituent, select top 10 with position sizing and risk budgeting |
| [playbook-pulse](.claude/skills/playbook-pulse/SKILL.md) | Daily pulse check on active playbooks — recalculates indicators, compares against original levels, produces week-ahead action plan |
| [moomoo-technicals](.claude/skills/moomoo-technicals/SKILL.md) | Technical indicator calculation (EMA, RSI, MACD, ATR, ADX, BB, OBV) using moomoo OpenD API with verified `--rehab none` data |

## Data Integrity

All technical indicators are computed from **moomoo OpenD API with `--rehab none`**. Moomoo's default forward-rehab adjustment severely distorts historical prices — using it produces EMA values wrong by up to 7.5% and Bollinger Bands wrong by up to 19% (verified in GOOGL audit, May 2026). Every playbook generation log records the rehab mode and snapshot verification.

## Reports (`reports/`)

| Directory | Content |
|-----------|---------|
| [playbooks/](reports/playbooks/) | 30-day trading playbooks for individual stocks (AAPL, GOOGL, NVDA, AMD, AMZN, GRAB) |
| [playbooks/logs/](reports/playbooks/logs/) | Audit trails recording every data source, tool call, and assumption |
| [etf-portfolio/](reports/etf-portfolio/) | ETF top-10 portfolio reports (QQQ) with allocation CSV |
| [daily-update/](reports/daily-update/) | Daily pulse checks comparing current price action against active playbooks |

## Quick Start

```
# Generate a 30-day playbook for a ticker
/trading-playbook NVDA

# Daily pulse check on an existing playbook
/playbook-pulse NVDA

# Top-10 ETF portfolio
/etf-top10-portfolio QQQ
```

## Repository Structure

```
vibe-trade/
├── .claude/skills/          # Claude Code skill definitions
│   ├── trading-playbook/
│   ├── etf-top10-portfolio/
│   ├── playbook-pulse/
│   └── moomoo-technicals/
├── reports/
│   ├── playbooks/           # Generated 30-day playbooks
│   │   └── logs/            # Generation audit trails
│   ├── etf-portfolio/       # ETF portfolio reports
│   └── daily-update/        # Daily pulse check reports
├── backtests/               # Backtest configs & strategy code
└── agent/                   # Agent source code
```

## References

- [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) — MCP server exposing the trading toolchain (backtest, options, factor analysis, screeners, etc.) that this project's skills call via `mcp__vibe-trading__*` tools
- [Moomoo OpenAPI](https://openapi.moomoo.com/moomoo-api-doc/en/intro/intro.html) — market data and trading API used for raw OHLCV kline data

## Disclaimer

All reports in this repository are for **research and educational purposes only**. They do not constitute investment advice. Trading involves substantial risk of loss. Past backtest performance does not guarantee future results.
