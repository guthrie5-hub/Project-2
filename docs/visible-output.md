# Visible Project 2 output

AI used: Codex helped write and debug the app; the analysis and decision are the student's. Education, not investment advice.

| Portfolio / scenario | VTI | VXUS | BND | SGOV | Estimated arithmetic annual return | Estimated volatility | Reserve verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| Equal-weight baseline | 25% | 25% | 25% | 25% | 6.26% | 8.70% | Pass; objective fails |
| 60% VTI / 40% BND benchmark | 60% | 0% | 40% | 0% | 7.02% | 11.37% | Objective passes; SGOV reserve fails |
| Constrained base | 30% | 5% | 0% | 65% | 6.54% | 5.47% | Pass |
| VTI estimate stress | 10% | 40% | 0% | 50% | 6.57% | 7.50% | Pass |
| Last-36-month window | 5% | 10% | 0% | 85% | 6.75% | 1.74% | Pass |
| 7.0% objective sensitivity (non-locked) | 40% | 0% | 0% | 60% | 7.07% | 6.42% | Pass at the higher objective |
| Cost stress | — | — | — | — | 6.34% net after 0.20% cost | — | Objective fails |
| 70% SGOV reserve constraint | — | — | — | — | No feasible five-point mix | — | Fails feasibility |

As-of data boundary: monthly price inputs end September 2026. Point-in-time BAA signal: as of 30 September 2026, August 2026 at 6.32% was the latest knowable value; September was published later.

Return definition: estimated return is the arithmetic mean of monthly returns × 12; it is not a compounded return, CAGR, or forecast.

The 7.0% objective sensitivity is a reported non-locked sensitivity. It does not substitute for the required human-authored Locked Changed-Input Record.
