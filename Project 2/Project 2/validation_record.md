# Project 2 validation record

Built with AI help; education, not investment advice.

## Completed checks

| Evidence | Result | Decision relevance |
|---|---|---|
| Lab 13 mandate engine known answer | Candidates A–C match the published reserve, liquidity, issuer, and long-only outcomes. | Establishes that mandate rules can reject a candidate. |
| Lab 14 portfolio known answer | Benchmark 6.80% / 10.46%, equal weight 5.20% / 5.21%, inverse volatility 3.77% / 1.05%. | Validates covariance-based volatility calculation. |
| Correlation edge case | IG–equity correlation 0.50 raises benchmark volatility to 11.00%; invalid 1.30 correlation refuses. | Checks directional behavior and input validation. |
| Point-in-time training | AAA is +1.98% as of 31 March 2026 versus a naive +5.83% using later information. | Demonstrates removal of look-ahead bias. |
| Project 2 base run | 30/5/0/65 VTI/VXUS/BND/SGOV; 6.54% return, 5.47% volatility, 65% reserve. | Supports a pilot only. |
| Changed-input stress | VTI return 12.00% to 8.00%, other inputs held fixed: 10/40/0/50; 6.57% return, 7.50% volatility. | Shows estimate risk can materially change the mix. |

## R riskiest claim

**Claim:** The all-month historical estimate supports using the 30/5/0/65 mix as a Project 2 starting allocation.

**Strongest challenge:** A different historical window or a lower VTI return estimate produces a materially different mix. The model does not establish future performance, after-cost outperformance, or that the chosen window is economically representative.

## Status requiring human/partner evidence

- `locked_changed_input_record.md`: the student must attest to an AI-off prediction, timestamp/commit, and actual decision effect.
- `cold_run_record.md`: a partner must run the README without coaching and record the first issue and elapsed time.
- Any resulting must-fix items must be frozen before recording videos.
