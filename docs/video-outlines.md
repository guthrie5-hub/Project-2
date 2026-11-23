# Project 2 video outlines

The complete timed scripts, including slide switches and live-app directions, are in [`project2-video-scripts.md`](project2-video-scripts.md). Use `../project2_presentation.html` for the visual slides.

Each video opens: “I used Codex to help write and debug the app and organize documentation; the analysis and decision are mine. Education, not investment advice.”

## Video 1 — how the system and thinking changed (maximum 3 minutes)

Start with the mandate: seven-year horizon, 6.5% gross expected-return objective, VTI/VXUS/BND/SGOV universe, 60/40 VTI/BND benchmark, long-only weights, and at least 3% SGOV. Explain the progression from mandate checks and training baselines to historical monthly-price estimates, then the constrained search. Show one AI-assisted output you checked: the point-in-time BAA rule, where September's later value could not be used on the September 30 decision date. Conclude that the process changed from a potential allocation tool to a zero-capital paper pilot after the cost stress failed the objective.

## Video 2 — technical walkthrough (maximum 5 minutes)

Show `prices.csv`, then `estimate_from_prices` in `portfolio.py`: monthly adjusted-close changes become annualized mean returns, volatility, and correlations. Show `search_lowest_risk_mix`: it enumerates long-only five-point weights, rejects mixes below the objective or reserve floor, and retains the lowest-volatility valid mix. Run `app.py` live. Show equal weight, the 60/40 benchmark, the constrained base mix, the mandate verdicts, the point-in-time signal, and the four stresses. State the key technical result: a 0.20% annual cost stress reduces the base estimated return from 6.54% to 6.34%, below objective.

## Video 3 — committee presentation (maximum 5 minutes)

Open with the live app already running. State the recommendation: paper pilot with 0% funded capital, not live adoption. The reference base mix is 30% VTI / 5% VXUS / 0% BND / 65% SGOV; it meets gross constraints but not the net objective under a 0.20% cost stress. State the monitored items and owner: the portfolio owner monitors implementation cost, historical-return assumptions, the all-month versus trailing-36-month window, BAA vintage compliance, and mandate changes. State reversal triggers: do not fund the process unless net-of-cost evidence supports the objective; stop/reoptimize if the lower return, window, or 70% reserve stress is more relevant.
