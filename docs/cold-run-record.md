# README-only cold-run record

AI used: Codex helped create this record; the cold review must be performed by an independent human. Education, not investment advice.

**Status: partner review found a reproducibility failure; source layout was repaired and an automated clean-room rerun passed.** An independent partner received the repository and followed the README without coaching. Their 23 November 2026 review is recorded below. The repository layout, not the portfolio calculations, caused the first failure. The later automated check is documented separately and is not represented as a partner review.

| Field | Reviewer record |
|---|---|
| Repository URL and commit | Reviewer cloned the submitted `Project-2` repository. Student must add the final repository URL and commit ID after the folder-layout repair. |
| Command run from README | `python3 -m pip install -r requirements.txt`, then `python3 -m streamlit run app.py`; optional terminal commands and `python3 -m unittest discover -s tests -v`. |
| First failure, or “none” | From the clone root, `requirements.txt`, `app.py`, the terminal scripts, and `tests/` were not found because the runnable package was nested at `Project 2/Project 2/`. |
| Resolution or limitation | The reviewer entered `Project 2/Project 2/`, which was a deviation from the README. There, install, three terminal scripts, three tests, and Streamlit all passed. The final repository must flatten the runnable package or correct the root README commands. |
| Elapsed time to visible result | About 19 seconds from dependency install to served app; about 0.95 seconds to render the page. Streamlit server became healthy in 0.58 seconds. |
| Where the visible result appeared | App Overview tab: constrained mix, mandate verdict, cost-stress failure, and paper-pilot warning. Written result: README decision section, `docs/decision-memo.md`, and `docs/visible-output.md`. |
| Did it match `docs/visible-output.md`? | Yes. Base mix 30/5/0/65 at 6.54% return and 5.47% volatility; cost stress 6.34%; VTI 12%→8% stress 10/40/0/50; last-36-month mix 5/10/0/85; and 70% reserve floor had no feasible mix. |
| Reviewer and date | Independent partner reviewer, 23 November 2026. |

## Post-repair automated clean-room rerun

| Field | Result |
|---|---|
| Repository URL and commit | `https://github.com/guthrie5-hub/Project-2`, `1e7f088` (23 November 2026) |
| Environment | Fresh clone; Python 3.13.16; new virtual environment; pinned `requirements.txt` dependencies. |
| README commands | Dependency install, the three optional terminal scripts, and `python3 -m unittest discover -s tests -v` all passed from the clone root. |
| App check | Streamlit `AppTest` loaded `app.py` with no exception. This is a technical app-load test, not a substitute for a human browser review. |
| First failure | None after the root-layout repair. |
| Result location | App Overview tab and `docs/visible-output.md` show the committee result. |

## Partner observations retained for repair

- The clone root needs one canonical runnable package. Do not rely on a reviewer finding a nested `Project 2/Project 2/` folder.
- The root README previously linked `visible_output.md`, which was an archived draft. The current package links `docs/visible-output.md`.
- The reviewer independently recomputed the price-file results and confirmed 60 price observations, 59 returns, October 2021 through September 2026, and sample standard deviation (`ddof=1`).
- The reviewer noted that the 7.0% objective sensitivity supplies the 40% VTI and 0% VXUS endpoints in the scenario span. It is reported as a non-locked sensitivity, not as the required Locked Changed-Input Record.
