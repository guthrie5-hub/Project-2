---
name: edgar-buffett-analysis
description: Retrieve five years of 10-K XBRL facts from SEC EDGAR and evaluate owner earnings and ROE when a business-quality review without price data is requested.
---

# EDGAR Buffett Analysis

Use the shared `edgar_owner_earnings.py` fact engine. Do not use paid-data sources, market prices, estimates, or 10-Q facts.

1. Require a temporary `SEC_USER_AGENT` contact; do not save it in the repository.
2. Keep the latest filed 10-K fact for a repeated fiscal-year end.
3. Do not estimate missing data: show `not found` or `not known`.
4. Apply only ROE at least 15% every year, positive owner earnings every year, and owner-earnings growth from first to last year.
5. Use the shared fact table when the three-investor panel is requested.
6. Write a business-quality memo from printed facts and checks only; do not make a price recommendation.
