# Project-2 — Constrained portfolio search

Built with AI help; education, not investment advice.

## Committee question

For a seven-year portfolio horizon, which long-only mix of VTI, VXUS, BND, and SGOV has the lowest estimated volatility while meeting a 6.5% annual expected-return objective and maintaining at least 3% in the reserve-eligible SGOV sleeve?

## Cold run

Requires Python 3.13+ and the packages in `requirements.txt`.

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Open the local URL printed by Streamlit. The default **My saved prices.csv** selection produces the Project 2 result. The app displays the historical-return estimates, the constrained lowest-risk mix, the checkable mandate verdict, and the recorded VTI stress case.

Optional terminal checks:

```bash
python3 portfolio.py
python3 mandate.py
python3 asof.py
```

## Decision

**Pilot, not adopt.** The all-month historical estimate produces 30% VTI / 5% VXUS / 0% BND / 65% SGOV, with 6.54% estimated return, 5.47% estimated volatility, and 65% reserve-eligible weight. Adopt only after the portfolio owner confirms that the five-year history and the 6.5% objective remain suitable; monitor the return assumptions, especially VTI. Reconsider the pilot if a lower VTI return estimate or the trailing-36-month window continues to produce a materially different allocation.

## Data and boundaries

- `prices.csv` has monthly adjusted closes for VTI, VXUS, BND, and SGOV, October 2021 through September 2026, oldest first.
- Source and download details are in `my_portfolio_mandate.md`. Historical mean returns are estimates, not forecasts.
- The model searches long-only allocations in five-percentage-point increments. It does not optimize taxes, trading costs, or a calendar-year loss limit.
- The BAA rate series may be used only with its matching ALFRED vintage date, as documented in `my_portfolio_mandate.md`.

## Repository map

| File | Purpose |
|---|---|
| `app.py` | Project 2 Streamlit product: constrained search, mandate verdict, and stress run. |
| `portfolio.py` | Reusable return, covariance, volatility, price-estimation, and search functions. |
| `prices.csv` | Five years of monthly adjusted-close inputs. |
| `my_portfolio_mandate.md` | Mandate, data card, base/trailing results, and decision. |
| `visible_output.md` | Results a reviewer can inspect without running code. |
| `committee_memo.md` | Committee recommendation and conditions. |
| `validation_record.md` | Known-answer, stress, point-in-time, and open validation evidence. |
| `locked_changed_input_record.md` | Human-authored prediction record; completion status is explicit. |
| `cold_run_record.md` | Partner cold-run record; completion status is explicit. |
| `mandate.py`, `meridian_mandate.md` | Lab 13 mandate training engine and written classification. |
| `asof.py`, `asof_app.py` | Point-in-time training and FRED/ALFRED evidence. |
| `skills/` | Inspection copies of the three local Codex skill instructions used for the SEC panel. |

## Known limitations and ownership

The portfolio owner—not the optimizer—owns the return objective, reserve classification, and adoption decision. A cold reviewer may reject or restrict use if the price data are unsupported, the historical estimates are used as forecasts, the mandate changes, a check fails, or the cold run cannot reproduce the visible output.
