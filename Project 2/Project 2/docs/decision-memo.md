# Project 2 decision memo

AI used: Codex helped write and debug the Python app and organize documentation; the analysis and committee decision are the student's. Education, not investment advice.

## Committee ask and mandate

Decide whether to adopt, allocate to, rebalance, pilot, or reject a lowest-volatility portfolio-selection process. The mandate uses a seven-year horizon, a 6.5% annual gross expected-return objective, VTI/VXUS/BND/SGOV as the investable universe, a 60% VTI / 40% BND transparent benchmark, annualized volatility as risk measure, long-only weights, and at least 3% in reserve-eligible SGOV.

## Recommendation: paper pilot, no funded allocation

Run a paper pilot with **0% funded capital**. Do not adopt the process for live allocation. The model's all-month base mix is 30% VTI / 5% VXUS / 0% BND / 65% SGOV, with 6.54% estimated gross return, 5.47% estimated volatility, and 65% reserve-eligible weight. It passes the checkable gross objective and reserve rules.

The funded recommendation stops at the cost stress. A 0.20% annual implementation-cost assumption reduces the base estimated return to 6.34%, below the 6.5% objective. This does not prove a loss; it establishes that the current process cannot support an after-cost adoption claim.

## Baselines and stress evidence

The equal-weight baseline produces 6.26% estimated return and 8.70% volatility, so it fails the gross objective. The 60% VTI / 40% BND benchmark produces 7.02% estimated return and 11.37% volatility, but fails the 3% SGOV reserve rule. The constrained base mix therefore has lower modeled volatility than both while meeting the gross, checkable mandate rules.

The process is estimate-sensitive. Lowering only VTI's expected return from 12.00% to 8.00% shifts the mix to 10% VTI / 40% VXUS / 0% BND / 50% SGOV and raises volatility to 7.50%. Using the last 36 months produces 5% VTI / 10% VXUS / 0% BND / 85% SGOV. Raising the reserve minimum to 70% produces no feasible five-point mix at the 6.5% objective.

## Conditions, monitoring, and reversal

During the paper pilot, use the scenario span as a reference range: VTI 5–40%, VXUS 0–40%, BND 0%, SGOV 50–85%. It is a sensitivity range, not a recommended set of simultaneous live weights. The portfolio owner monitors return assumptions, the all-month versus trailing-36-month window, the BAA point-in-time credit signal, actual implementation costs, and changes to the objective or reserve rule.

Stop the process or reoptimize if costs prevent the net objective from being met, a different return window remains better supported, a 70% reserve floor becomes required, or the point-in-time data rule cannot be followed. The app cannot establish future, after-cost outperformance.
