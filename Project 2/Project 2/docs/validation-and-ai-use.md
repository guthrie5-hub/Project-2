# Project 2 validation and AI-use record

AI used: Codex helped write and debug the Python app and organize documentation; the analysis and committee decision are the student's. Education, not investment advice.

## Source and as-of boundary

`prices.csv` contains monthly adjusted closes for VTI, VXUS, BND, and SGOV from October 2021 through September 2026. Sources and download date are recorded in `my_portfolio_mandate.md`. The return input is the annualized arithmetic mean of monthly returns (mean × 12), not a compounded return, CAGR, or forecast. The point-in-time signal is Moody's Seasoned Baa Corporate Bond Yield (FRED/ALFRED BAA). On 30 September 2026, the latest knowable month was August 2026 at 6.32%; September's 6.47% value was later information and is not used for that decision date.

## Tests and results

| Test | Result | Limitation / disposition |
|---|---|---|
| Mandate known answer | Lab 13 candidate A passes; B fails three rules; C fails one; E benchmark fails the reserve rule. | Training reconciliation; own mandate has fewer checkable restrictions. |
| Portfolio known answer | Benchmark 6.80% / 10.46%; equal weight 5.20% / 5.21%; inverse volatility 3.77% / 1.05%. | Validates training covariance and return arithmetic. |
| Bad-correlation edge case | Correlation outside −1 to 1 refuses. | Input validity only; not a forecast check. |
| Point-in-time known answer | AAA is +1.98% as-of versus naive +5.83%. | Demonstrates look-ahead-bias control on training data. |
| Base Project 2 result | 30/5/0/65; 6.54% gross return; 5.47% volatility; 65% SGOV reserve. | Historical estimates may not recur. |
| Estimate stress | VTI 12.00% → 8.00% produces 10/40/0/50 and 7.50% volatility. | One-factor sensitivity, not probability. |
| Window stress | Last 36 months produces 5/10/0/85. | Window choice changes the answer. |
| Cost stress | 0.20% annual cost reduces base return to 6.34%, below objective. | Costs are not optimized; funded adoption is withheld. |
| Constraint stress | 70% SGOV reserve floor has no feasible five-point mix at 6.5%. | Feasibility depends on mandate limits. |

## Model-risk challenge

An independent challenger can reject live adoption because the objective is gross of costs, historical return averages are unsupported as forecasts, the selected allocation changes with reasonable estimate/window changes, or a cold reviewer cannot reproduce the result. The process is therefore limited to a zero-capital paper pilot pending evidence that net-of-cost assumptions and the mandate remain defensible.

## AI-use record

| Tool / model | Interaction dates | Material use | Human disposition |
|---|---|---|---|
| Codex, OpenAI coding agent (model version not separately recorded) | October–November 2026 | Drafted/debugged Python, organized Markdown, explained calculations, and generated test ideas. | Accepted code only after known-answer, edge-case, and Streamlit tests; user retains the mandate and decision. |
| FRED/ALFRED public CSV downloads | October 2026 | Retrieved current and vintage BAA observations for the point-in-time exercise. | Accepted only under the documented vintage rule. |
| Yahoo Finance chart data | October 2026 | Provided monthly adjusted-close observations in `prices.csv`. | Used as historical input, not forecast evidence. |

## Locked Changed-Input Record

The complete record is in `docs/locked-changed-input-record.md`. Its human-authored AI-off prediction and immutable pre-run commit are currently **unresolved**; do not claim it is complete until the student supplies them before a new run.
