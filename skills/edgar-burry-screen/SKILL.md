---
name: edgar-burry-screen
description: Apply the course-defined Burry cash-flow and leverage screen to five years of SEC EDGAR 10-K facts when a three-investor panel is requested.
---

# EDGAR Burry Screen

Use the shared `edgar_owner_earnings.py` fact engine. Do not add market prices, forecasts, or non-10-K data.

- Compare operating cash flow with net income in every year.
- Use `Liabilities / StockholdersEquity` for the latest-year leverage check.
- Apply only: operating cash flow at least net income every year, and liabilities no more than twice equity in the latest year.
- Missing inputs remain `not found`; checks depending on them are `not known`.
- Write the Burry memo from displayed shared facts and check outcomes only.
