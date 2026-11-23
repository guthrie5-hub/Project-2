"""Streamlit learning app for the Project 2 constrained portfolio search."""

from copy import deepcopy
from io import StringIO
from pathlib import Path

import streamlit as st
import pandas as pd

from portfolio import (
    CORRELATION,
    MINIMUM_RESERVE_ELIGIBLE_WEIGHT,
    OBJECTIVE_RETURN,
    SLEEVES,
    covariance_matrix,
    estimate_from_prices,
    expected_return,
    portfolio_volatility,
    reserve_eligible_weight,
    search_lowest_risk_mix,
)


# Recorded Project 2 stress case: one-point-independent input change from the
# historical VTI return estimate to 8.0%; other loaded inputs stay unchanged.
STRESS_RETURN_OVERRIDES = {"VTI": 0.08}
ANNUAL_COST_STRESS = 0.002
CONSTRAINT_STRESS_RESERVE = 0.70
OBJECTIVE_STRESS = 0.07
POINT_IN_TIME_SIGNAL = {
    "series": "BAA — Moody's Seasoned Baa Corporate Bond Yield",
    "decision_date": "2026-09-30",
    "latest_known_month": "2026-08",
    "latest_known_value": 6.32,
    "previous_month_value": 6.19,
}


def reserve_default(name, loaded_value):
    """Preserve Meridian defaults and recognize common cash-like Treasury ETF tickers."""
    return loaded_value or name.upper() in {"BIL", "SGOV", "SHV", "TBIL", "CLIP"}


def show_solution(title, solution, names):
    """Display one search result."""
    st.subheader(title)
    if solution is None:
        st.warning("No mix meets the objective and reserve minimum.")
        return
    st.dataframe(
        {"Asset": names, "Weight": [f"{solution['weights'][name] * 100:.1f}%" for name in names]},
        hide_index=True,
        width="stretch",
    )
    st.write(f"Expected return: **{solution['return'] * 100:.2f}%**")
    st.write(f"Volatility: **{solution['volatility'] * 100:.2f}%**")
    st.write(f"Reserve-eligible weight: **{solution['reserve_eligible_weight'] * 100:.1f}%**")


def allocation_frame(solution, names):
    """Return a chart-ready allocation table, or an empty table for no solution."""
    if solution is None:
        return pd.DataFrame(columns=["Asset", "Weight (%)"])
    return pd.DataFrame(
        {
            "Asset": names,
            "Weight (%)": [solution["weights"][name] * 100 for name in names],
        }
    ).set_index("Asset")


def show_allocation_chart(solution, names, title):
    """Show the allocation as a readable horizontal-style bar chart."""
    frame = allocation_frame(solution, names)
    st.caption(title)
    if frame.empty:
        st.info("No allocation is available for this set of inputs.")
        return
    st.bar_chart(frame, horizontal=True, height=210)


def verdict_label(solution, objective, reserve_minimum):
    """Return a short verdict used consistently in summary tables."""
    if solution is None:
        return "No feasible mix"
    if solution["return"] < objective or solution["reserve_eligible_weight"] < reserve_minimum:
        return "FAIL"
    return "Pass"


def comparison_frame(entries, objective, reserve_minimum):
    """Build one comparison table from calculated portfolio outputs."""
    rows = []
    for label, solution in entries:
        if solution is None:
            rows.append({"Portfolio": label, "Return (%)": None, "Volatility (%)": None,
                         "Reserve eligible (%)": None, "Mandate": "No feasible mix"})
            continue
        rows.append(
            {
                "Portfolio": label,
                "Return (%)": solution["return"] * 100,
                "Volatility (%)": solution["volatility"] * 100,
                "Reserve eligible (%)": solution["reserve_eligible_weight"] * 100,
                "Mandate": verdict_label(solution, objective, reserve_minimum),
            }
        )
    return pd.DataFrame(rows).set_index("Portfolio")


def show_mandate_verdict(solution, objective, reserve_minimum):
    """Show the checkable objective and reserve rules for one returned mix."""
    if solution is None:
        st.warning("Mandate verdict: no mix meets the objective and reserve rules.")
        return
    weights = list(solution["weights"].values())
    rows = [
        {"Rule": "Weights sum to 100%", "Measured": f"{sum(weights) * 100:.1f}%", "Verdict": "pass" if abs(sum(weights) - 1.0) < 1e-9 else "FAIL"},
        {"Rule": "Long-only", "Measured": f"lowest {min(weights) * 100:.1f}%", "Verdict": "pass" if min(weights) >= 0 else "FAIL"},
        {"Rule": "Expected return meets objective", "Measured": f"{solution['return'] * 100:.2f}% vs {objective * 100:.2f}%", "Verdict": "pass" if solution["return"] >= objective else "FAIL"},
        {"Rule": "Reserve-eligible weight meets minimum", "Measured": f"{solution['reserve_eligible_weight'] * 100:.1f}% vs {reserve_minimum * 100:.1f}%", "Verdict": "pass" if solution["reserve_eligible_weight"] >= reserve_minimum else "FAIL"},
    ]
    st.dataframe(rows, hide_index=True, width="stretch")


def solution_from_weights(weights, sleeves, correlation):
    """Calculate the displayed return, volatility, and reserve result for a baseline."""
    covariance = covariance_matrix(sleeves, correlation)
    return {
        "weights": weights,
        "return": expected_return(weights, sleeves),
        "volatility": portfolio_volatility(weights, covariance, sleeves),
        "reserve_eligible_weight": reserve_eligible_weight(weights, sleeves),
    }


def project_benchmark_weights(names):
    """Use the stated transparent 60% VTI / 40% BND benchmark when available."""
    if not {"VTI", "BND"}.issubset(names):
        return None
    return {name: 0.60 if name == "VTI" else 0.40 if name == "BND" else 0.0 for name in names}


st.set_page_config(page_title="Portfolio Search", layout="wide")
st.markdown(
    """<style>
    .block-container {max-width: 1220px; padding-top: 2.25rem; padding-bottom: 3rem;}
    </style>""",
    unsafe_allow_html=True,
)
st.title("Portfolio mandate dashboard")
st.write("Find the lowest estimated-volatility mix that meets the stated return and liquidity rules.")
st.caption("AI used: Codex helped write and debug the app; the analysis and decision are the student's. Education, not investment advice.")

with st.sidebar:
    st.header("Search inputs")
    dataset = st.radio("Dataset", ["Meridian training inputs", "My saved prices.csv"], index=1)
    objective = st.number_input("Objective return (%)", value=OBJECTIVE_RETURN * 100.0, step=0.1) / 100.0
    reserve_minimum = st.number_input(
        "Minimum reserve-eligible weight (%)",
        value=MINIMUM_RESERVE_ELIGIBLE_WEIGHT * 100.0,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
    ) / 100.0
    uploaded = st.file_uploader("Upload a replacement prices.csv", type="csv")
    last_36 = st.checkbox("Use only the last 36 monthly returns")

try:
    saved_prices = Path(__file__).with_name("prices.csv")
    if uploaded is None and dataset == "Meridian training inputs":
        loaded_sleeves = deepcopy(SLEEVES)
        loaded_correlation = deepcopy(CORRELATION)
        all_month_sleeves = deepcopy(SLEEVES)
        all_month_correlation = deepcopy(CORRELATION)
        input_label = "Meridian inputs as loaded"
    else:
        if uploaded is not None:
            csv_text = uploaded.getvalue().decode("utf-8-sig")
            csv_label = "Uploaded CSV estimates on all months"
        else:
            if not saved_prices.exists():
                raise ValueError("Saved prices.csv is missing. Upload a CSV instead.")
            csv_text = saved_prices.read_text(encoding="utf-8-sig")
            csv_label = "My saved prices.csv estimates on all months"
        all_month_sleeves, all_month_correlation = estimate_from_prices(StringIO(csv_text))
        loaded_sleeves, loaded_correlation = estimate_from_prices(StringIO(csv_text), last_36_months=last_36)
        input_label = csv_label
except (UnicodeDecodeError, ValueError) as error:
    st.error(f"Could not use the uploaded CSV: {error}")
    st.stop()

st.write(
    "Return estimates are annualized arithmetic means of monthly returns (mean × 12), "
    "not compounded returns, CAGRs, or forecasts."
)
st.subheader("Expected-return and reserve-eligibility inputs")
edited_sleeves = {}
for name, values in loaded_sleeves.items():
    left, right = st.columns([3, 1])
    with left:
        edited_return = st.number_input(
            f"{name} expected return (%)",
            value=values["return"] * 100.0,
            step=0.1,
            key=f"return_{name}",
        ) / 100.0
    with right:
        eligible = st.checkbox(
            f"{name} reserve-eligible",
            value=reserve_default(name, values["reserve_eligible"]),
            key=f"eligible_{name}",
        )
    edited_sleeves[name] = {"return": edited_return, "volatility": values["volatility"], "reserve_eligible": eligible}

current_solution = search_lowest_risk_mix(
    edited_sleeves, loaded_correlation, objective, reserve_minimum
)
base_sleeves = deepcopy(all_month_sleeves)
for name in base_sleeves:
    base_sleeves[name]["reserve_eligible"] = edited_sleeves[name]["reserve_eligible"]
loaded_solution = search_lowest_risk_mix(
    base_sleeves, all_month_correlation, OBJECTIVE_RETURN, MINIMUM_RESERVE_ELIGIBLE_WEIGHT
)

stress_sleeves = deepcopy(all_month_sleeves)
for name in stress_sleeves:
    stress_sleeves[name]["reserve_eligible"] = edited_sleeves[name]["reserve_eligible"]
for name, value in STRESS_RETURN_OVERRIDES.items():
    if name in stress_sleeves:
        stress_sleeves[name]["return"] = value
stress_solution = search_lowest_risk_mix(
    stress_sleeves, all_month_correlation, OBJECTIVE_RETURN, MINIMUM_RESERVE_ELIGIBLE_WEIGHT
)

# Preserved sensitivity only. It does not replace the separate human-authored
# Locked Changed-Input Record required by the course.
objective_stress_solution = search_lowest_risk_mix(
    base_sleeves, all_month_correlation, OBJECTIVE_STRESS, MINIMUM_RESERVE_ELIGIBLE_WEIGHT
)

window_sleeves, window_correlation = estimate_from_prices(StringIO(csv_text), last_36_months=True) if "csv_text" in locals() else (None, None)
if window_sleeves is not None:
    for name in window_sleeves:
        window_sleeves[name]["reserve_eligible"] = edited_sleeves[name]["reserve_eligible"]
    window_solution = search_lowest_risk_mix(
        window_sleeves, window_correlation, OBJECTIVE_RETURN, MINIMUM_RESERVE_ELIGIBLE_WEIGHT
    )
else:
    window_solution = None

equal_weights = {name: 1.0 / len(base_sleeves) for name in base_sleeves}
equal_solution = solution_from_weights(equal_weights, base_sleeves, all_month_correlation)
benchmark_weights = project_benchmark_weights(base_sleeves)
benchmark_solution = (
    solution_from_weights(benchmark_weights, base_sleeves, all_month_correlation)
    if benchmark_weights is not None else None
)

names = list(edited_sleeves)

st.divider()
st.subheader("Current decision snapshot")
if current_solution is None:
    st.error("No feasible allocation meets the current objective and reserve rule.")
else:
    metric_a, metric_b, metric_c, metric_d = st.columns(4)
    metric_a.metric("Expected return", f"{current_solution['return'] * 100:.2f}%")
    metric_b.metric("Estimated volatility", f"{current_solution['volatility'] * 100:.2f}%")
    metric_c.metric("Reserve eligible", f"{current_solution['reserve_eligible_weight'] * 100:.1f}%")
    metric_d.metric("Mandate verdict", verdict_label(current_solution, objective, reserve_minimum))

overview_tab, allocations_tab, comparisons_tab, evidence_tab = st.tabs(
    ["Overview", "Allocations", "Baselines & stresses", "Evidence & decision"]
)

with overview_tab:
    left, right = st.columns(2)
    with left:
        show_solution("Current edited inputs", current_solution, names)
    with right:
        show_solution(input_label, loaded_solution, list(base_sleeves))
    if current_solution is not None and loaded_solution is not None:
        largest_change = max(
            abs(current_solution["weights"][name] - loaded_solution["weights"][name])
            for name in edited_sleeves
        )
        st.info(f"Largest weight change from loaded answer: {largest_change * 100:.1f} percentage points.")
    else:
        st.info("Largest weight change is unavailable because one search has no valid mix.")

    st.subheader("Checkable mandate verdict: current edited inputs")
    show_mandate_verdict(current_solution, objective, reserve_minimum)

with allocations_tab:
    allocation_left, allocation_right = st.columns(2)
    with allocation_left:
        show_allocation_chart(current_solution, names, "Current edited allocation")
    with allocation_right:
        show_allocation_chart(loaded_solution, list(base_sleeves), "Saved base allocation")
    st.caption("Weights are displayed in percent. A zero bar means the five-point search did not select that sleeve.")

with comparisons_tab:
    st.subheader("Required baselines beside the constrained portfolio")
    portfolio_comparison = comparison_frame(
        [
            ("Equal weight", equal_solution),
            ("60/40 VTI/BND benchmark", benchmark_solution),
            ("Constrained portfolio", loaded_solution),
        ],
        OBJECTIVE_RETURN,
        MINIMUM_RESERVE_ELIGIBLE_WEIGHT,
    )
    st.dataframe(
        portfolio_comparison.style.format(
            {"Return (%)": "{:.2f}", "Volatility (%)": "{:.2f}", "Reserve eligible (%)": "{:.1f}"}
        ),
        width="stretch",
    )
    graph_left, graph_right = st.columns(2)
    with graph_left:
        st.caption("Expected return comparison")
        st.bar_chart(portfolio_comparison[["Return (%)"]], horizontal=True, height=220)
    with graph_right:
        st.caption("Volatility comparison")
        st.bar_chart(portfolio_comparison[["Volatility (%)"]], horizontal=True, height=220)

    st.divider()
    st.subheader("Stress runs")
    stress_left, stress_middle, stress_right = st.columns(3)
    with stress_left:
        st.caption("VTI expected-return stress: 12.0% → 8.0%")
        show_solution("Recorded estimate stress", stress_solution, list(stress_sleeves))
    with stress_middle:
        show_solution("Last-36-month window", window_solution, list(window_sleeves) if window_sleeves else [])
    with stress_right:
        if loaded_solution is None:
            st.warning("Cost stress unavailable because the base portfolio has no solution.")
        else:
            net_return = loaded_solution["return"] - ANNUAL_COST_STRESS
            st.metric("Net return after 0.20% cost", f"{net_return * 100:.2f}%")
            st.write(f"Objective verdict: **{'pass' if net_return >= OBJECTIVE_RETURN else 'FAIL'}**")
            st.caption("Costs are a stress display only; they are not optimized in the search.")

    constraint_solution = search_lowest_risk_mix(
        base_sleeves, all_month_correlation, OBJECTIVE_RETURN, CONSTRAINT_STRESS_RESERVE
    )
    if constraint_solution is None:
        st.warning("70% SGOV reserve stress: no five-point mix meets both the 6.5% objective and the higher reserve floor.")
    else:
        show_solution("70% reserve-constraint stress", constraint_solution, list(base_sleeves))

    st.divider()
    st.caption("Objective-return sensitivity: 6.5% → 7.0% with other base inputs fixed")
    show_solution("7.0% objective sensitivity", objective_stress_solution, list(base_sleeves))
    st.caption("This is a reported sensitivity only. It does not substitute for the required Locked Changed-Input Record.")

with evidence_tab:
    st.subheader("Point-in-time signal and data card")
    change_bp = (POINT_IN_TIME_SIGNAL["latest_known_value"] - POINT_IN_TIME_SIGNAL["previous_month_value"]) * 100
    st.info(
        f"As of {POINT_IN_TIME_SIGNAL['decision_date']}, the latest knowable {POINT_IN_TIME_SIGNAL['series']} "
        f"observation was {POINT_IN_TIME_SIGNAL['latest_known_month']} at {POINT_IN_TIME_SIGNAL['latest_known_value']:.2f}%, "
        f"up {change_bp:.0f} basis points from the previous month."
    )
    st.caption("Source: FRED/ALFRED BAA. The data card and vintage rule are documented in my_portfolio_mandate.md; this signal does not automatically override the allocation.")

    st.subheader("Committee recommendation")
    st.warning(
        "**Paper pilot only — 0% funded capital.** The gross-return base passes the mandate, but a 0.20% annual-cost stress "
        "drops the result below the 6.5% objective. Do not adopt a live allocation until net-of-cost return assumptions and mandate limits are defended."
    )
    st.write("**Monitor:** return estimates, the all-month versus trailing-36-month mix, implementation costs, and the point-in-time data rule.")
