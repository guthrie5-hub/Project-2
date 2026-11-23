# Project 2 — Constrained portfolio search

AI used: Codex helped write and debug the Python app and organize documentation; the analysis and committee decision are the student's. Education, not investment advice.

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
python3 -m unittest discover -s tests -v
```

## Decision

**Pilot the process with 0% funded capital; do not adopt a live allocation yet.** The all-month historical estimate produces 30% VTI / 5% VXUS / 0% BND / 65% SGOV, with 6.54% estimated gross return, 5.47% estimated volatility, and 65% reserve-eligible weight. A 0.20% annual-cost stress reduces the estimated net return to 6.34%, below the 6.5% objective. The reference scenario span across the reported base, return-estimate, window, and 7.0%-objective sensitivities is VTI 5–40%, VXUS 0–40%, BND 0%, and SGOV 50–85%; the breadth of that span is why it is not a live allocation recommendation.

## Data and boundaries

- `prices.csv` has monthly adjusted closes for VTI, VXUS, BND, and SGOV, October 2021 through September 2026, oldest first.
- Source and download details are in `my_portfolio_mandate.md`. Historical mean returns are estimates, not forecasts.
- The app calculates return estimates as an **annualized arithmetic mean of monthly returns** (monthly mean × 12). That is not a compounded return or CAGR.
- The model searches long-only allocations in five-percentage-point increments. It does not optimize taxes or a calendar-year loss limit; the 0.20% implementation-cost case is a stress display, not an optimization input.
- The BAA rate series may be used only with its matching ALFRED vintage date, as documented in `my_portfolio_mandate.md`.

## Repository map

| File | Purpose |
|---|---|
| `app.py` | Project 2 Streamlit product: constrained search, mandate verdict, and stress run. |
| `portfolio.py` | Reusable return, covariance, volatility, price-estimation, and search functions. |
| `prices.csv` | Five years of monthly adjusted-close inputs. |
| `my_portfolio_mandate.md` | Mandate, data card, base/trailing results, and decision. |
| `docs/visible-output.md` | Results a reviewer can inspect without running code. |
| `docs/decision-memo.md` | Committee recommendation and conditions. |
| `docs/validation-and-ai-use.md` | Known-answer, stress, point-in-time, AI-use, and open validation evidence. |
| `docs/locked-changed-input-record.md` | Human-authored prediction record; completion status is explicit. |
| `docs/cold-run-record.md` | Partner cold-run record; completion status is explicit. |
| `project2_presentation.html` | Browser-based, screen-capture-ready presentation for the three Project 2 videos. |
| `docs/project2-video-scripts.md` | Timed recording scripts and slide-switch instructions. |
| `mandate.py`, `meridian_mandate.md` | Lab 13 mandate training engine and written classification. |
| `asof.py`, `asof_app.py` | Point-in-time training and FRED/ALFRED evidence. |
| `skills/` | Inspection copies of the three local Codex skill instructions used for the SEC panel. |
| `tests/` | Small automated checks for the course known-answer arithmetic and a no-feasible-mix edge case. |

## Known limitations and ownership

The mandate is a 6.5% annual gross expected-return objective over a seven-year horizon; the universe is VTI, VXUS, BND, and SGOV; the transparent benchmark is 60% VTI / 40% BND; the risk measure is annualized volatility; limits are long-only weights and at least 3% SGOV reserve-eligible weight. The portfolio owner—not the optimizer—owns these choices. A cold reviewer may reject or restrict use if the price data are unsupported, the historical estimates are used as forecasts, the mandate changes, a check fails, or the cold run cannot reproduce the visible output.

The root-level records marked **“Superseded draft”** are retained only as archival Lab history. The current submission records live in `docs/`.
