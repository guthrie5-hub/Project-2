---
name: edgar-graham-screen
description: Apply the course-defined Graham liquidity and earnings screen to five years of SEC EDGAR 10-K facts when a three-investor panel is requested.
---

# EDGAR Graham Screen

Use the shared `edgar_owner_earnings.py` fact engine. Do not add market prices, forecasts, or non-10-K data.

- Use `AssetsCurrent / LiabilitiesCurrent` for the latest-year current ratio.
- Apply only: current ratio at least 2.00 in the latest year, positive net income every year, and net-income growth from first to last year.
- Missing inputs remain `not found`; checks depending on them are `not known`.
- Write the Graham memo from displayed shared facts and check outcomes only.
