# Project 2 video scripts

Use the matching slides in `project2_presentation.html`. These are recording scripts, not final transcripts. After recording, create the transcript from the words you actually said and correct finance terms, numbers, and tickers.

## Video 1 — research evolution (about 2:35)

### Slide 1 — 0:00–0:20

“I used Codex to help write and debug the app and organize documentation. The analysis and decision are mine. This is education, not investment advice.

This Project 2 asks whether a committee should adopt a constrained portfolio-selection process. My conclusion is a paper pilot with zero funded capital, not live adoption.”

### Slide 2 — 0:20–1:05

“The mandate has a seven-year horizon and a 6.5% annual gross expected-return objective. The investable universe is VTI, VXUS, BND, and SGOV. I use annualized volatility as the risk measure. The process permits only long positions and requires at least 3% in reserve-eligible SGOV.

The transparent comparison benchmark is 60% VTI and 40% BND. One important limit is that the 6.5% objective is gross of costs, so the app cannot claim that the process achieves a net return objective.”

### Slide 3 — 1:05–2:00

“The process starts with monthly adjusted prices. It converts them to monthly returns, then calculates annualized arithmetic mean returns, volatility, and correlations. It searches long-only weights in five-percentage-point steps and keeps the lowest-volatility mix that meets the return and reserve rules.

This definition matters: arithmetic mean monthly return times twelve is a historical estimate. It is not a CAGR and it is not a forecast. I added the historical price file, two baselines, mandate verdicts, point-in-time evidence, and stresses to the original training engine.”

### Slide 6 — 2:00–2:35

“I also checked one AI-assisted point-in-time rule. On September 30, 2026, August BAA at 6.32% was the latest knowable monthly observation. September’s 6.47% was published later, so using it on September 30 would be look-ahead bias. The process keeps BAA only with the matching vintage date.

The system changed from a possible allocation tool to a paper pilot because the cost stress breaks the stated objective.”

## Video 2 — technical walkthrough and validation (about 4:15)

### Slide 4 — 0:00–0:50

“I used Codex to help write and debug the app and organize documentation. The analysis and decision are mine. This is education, not investment advice.

The core calculation sits in `portfolio.py`. The app reads the price file, calculates monthly returns, and uses the arithmetic mean multiplied by twelve as the expected-return input. It calculates covariance as correlation times the two asset volatilities.”

### Code screen — 0:50–1:45

“Here is `search_lowest_risk_mix`. The function tries each long-only five-point allocation. For each possible mix, it calculates expected return and reserve-eligible weight. It discards a mix below the objective or reserve floor. For valid mixes, it calculates volatility from the covariance matrix. The function keeps the mix with the lowest volatility. If no mix meets both constraints, it returns no solution rather than forcing an answer.”

### Slide 5 — 1:45–2:40

“The model first reproduced the training benchmark at 6.80% return and 10.46% volatility. It also refuses a correlation outside negative one to positive one.

For the company-specific sensitivity, lowering only VTI’s expected return from 12% to 8% changed the answer to 10% VTI, 40% VXUS, zero BND, and 50% SGOV. The last-36-month sample produces a different allocation again. A 70% SGOV reserve floor produces no feasible five-point mix at the 6.5% objective.”

### Live app — 2:40–3:45

“I will now show the app. The Overview tab displays the current allocation and checkable mandate verdict. The Allocations tab shows the portfolio weights. Baselines and stresses compare equal weight, the 60/40 benchmark, the constrained base, and the stress cases. The Evidence tab records the BAA vintage rule and the committee recommendation.

The constrained base is 30% VTI, 5% VXUS, zero BND, and 65% SGOV. It has a 6.54% estimated gross return, 5.47% estimated volatility, and 65% reserve-eligible weight.”

### Slide 7 — 3:45–4:15

“The critical validation result is the cost stress. A 0.20% annual implementation cost reduces the base return from 6.54% gross to 6.34% net. That is below the 6.5% objective. The test does not prove a loss; it shows that the evidence does not support funded adoption.”

## Video 3 — committee presentation (about 3:20)

### Live app first — 0:00–0:45

“I used Codex to help write and debug the app and organize documentation. The analysis and decision are mine. This is education, not investment advice.

This live dashboard shows the committee decision. The constrained base mix passes the gross checkable rules, but the cost stress reduces its estimated return below the objective. My committee action is a paper pilot with zero funded capital. I do not recommend a live allocation today.”

### Slide 7 — 0:45–1:50

“The equal-weight baseline has a 6.26% estimated return and fails the objective. The 60% VTI and 40% BND benchmark reaches 7.02% estimated return but fails the SGOV reserve rule. The constrained base has the lowest modeled volatility of these three and meets the gross checkable rules.

However, the 0.20% cost stress takes the base from 6.54% to 6.34%. Since the mandate sets a 6.5% objective, I withhold a funded recommendation.”

### Slide 8 — 1:50–3:20

“The scenario results span VTI from 5% to 40%, VXUS from zero to 40%, BND at zero, and SGOV from 50% to 85%. That span reflects different inputs and windows. It does not represent one simultaneous recommended allocation range.

The portfolio owner should monitor implementation costs, return estimates, the difference between the full historical sample and the last 36 months, BAA vintage compliance, and changes to the objective or reserve floor.

The committee should stop or reoptimize if costs continue to prevent the net objective, a 70% reserve requirement becomes relevant, or the point-in-time data rule cannot be followed. The decision changes toward adoption only with defensible net-of-cost return evidence and a more stable allocation across reasonable input changes.”
