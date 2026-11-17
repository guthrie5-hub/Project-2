# Superseded draft — use `docs/video-outlines.md`

The final video outlines are [`docs/video-outlines.md`](docs/video-outlines.md). The text below is archived and is not the submission record.

---

# Archived video outlines

Built with AI help; education, not investment advice.

## Video 1 — evolution

Open: “Built with AI help; education, not investment advice.” Explain the original mandate: a 6.5% expected-return objective and at least 3% in SGOV. Show how the system moved from Meridian training inputs to VTI, VXUS, BND, and SGOV monthly data, and explain that historical returns are estimates rather than forecasts. Identify the checked AI-assisted output: the point-in-time rule, where the as-of AAA signal was +1.98% rather than the naive +5.83%. End with the change in your judgment: the output is a pilot input, not an adoption recommendation.

## Video 2 — technical walkthrough

Open: “Built with AI help; education, not investment advice.” Show `prices.csv`, then `estimate_from_prices` in `portfolio.py`: monthly price changes become annualized mean returns, volatility, and correlations. Show `search_lowest_risk_mix`: it tries long-only five-point mixes, rejects those below the 6.5% objective or 3% reserve rule, and retains the lowest-volatility valid mix. Run `app.py`; show the base 30/5/0/65 result, the mandate verdict, and the VTI 8% stress result. State the highest-risk test: changing only VTI's expected return to 8% shifts the mix to 10/40/0/50.

## Video 3 — committee decision

Open: “Built with AI help; education, not investment advice.” Recommend pilot, not adoption, of the all-month 30% VTI / 5% VXUS / 0% BND / 65% SGOV starting mix. State the condition: use it only while the historical-return assumptions and 6.5% objective remain appropriate. State the monitor and owner: the portfolio owner monitors VTI assumptions and the all-month versus trailing-36-month regime. State the reversal trigger: reoptimize or defer if lower VTI assumptions or the trailing window remain better supported. Conclude that the model cannot establish future, after-cost outperformance.
