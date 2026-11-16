"""Streamlit learning app for the Meridian portfolio search."""

from copy import deepcopy
from io import StringIO
from pathlib import Path

import streamlit as st

from portfolio import (
    CORRELATION,
    MINIMUM_RESERVE_ELIGIBLE_WEIGHT,
    OBJECTIVE_RETURN,
    SLEEVES,
    estimate_from_prices,
    search_lowest_risk_mix,
)


# Recorded Project 2 stress case: one-point-independent input change from the
# historical VTI return estimate to 8.0%; other loaded inputs stay unchanged.
STRESS_RETURN_OVERRIDES = {"VTI": 0.08}


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


st.set_page_config(page_title="Portfolio Search", layout="wide")
st.title("Lowest-risk portfolio search")
st.caption("Built with AI help; education, not investment advice.")

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

st.write("Historical price estimates are estimates from past returns, not forecasts.")
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

left, right = st.columns(2)
with left:
    show_solution("Current edited inputs", current_solution, list(edited_sleeves))
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

if "VTI" in stress_sleeves:
    st.subheader("Recorded stress run")
    st.write("Change only VTI's expected return to **8.0%**; use all-month price estimates and the base objective and reserve minimum.")
    show_solution("Stress result", stress_solution, list(stress_sleeves))
else:
    st.info("Recorded VTI stress run is unavailable because VTI is not in this dataset.")
