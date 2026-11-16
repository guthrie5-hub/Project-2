# Visible Project 2 output

Built with AI help; education, not investment advice.

## Project 2 portfolio result

All-month monthly-price estimates, October 2021–September 2026:

| Result | VTI | VXUS | BND | SGOV | Estimated return | Estimated volatility | Reserve-eligible |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base constrained mix | 30% | 5% | 0% | 65% | 6.54% | 5.47% | 65% |
| VTI stress: 12.00% → 8.00% | 10% | 40% | 0% | 50% | 6.57% | 7.50% | 50% |
| Objective stress: 6.50% → 7.00% | 40% | 0% | 0% | 60% | 7.07% | 6.42% | 60% |
| Last-36-month estimate | 5% | 10% | 0% | 85% | 6.75% | 1.74% | 85% |

Base mandate checks: weights sum to 100%, lowest weight is 0%, estimated return exceeds 6.50%, and reserve-eligible weight exceeds 3%.

## Training validations

| Check | Result |
|---|---|
| Lab 14 benchmark return / volatility | 6.80% / 10.46% |
| Lab 14 equal-weight return / volatility | 5.20% / 5.21% |
| Lab 14 inverse-volatility return / volatility | 3.77% / 1.05% |
| Lab 13 candidate A | Passes every checkable rule |
| Lab 13 candidate E benchmark | Fails reserve rule at 0.0% |
| Point-in-time training, AAA as-of signal | +1.98% versus naive +5.83% |

The reported values are model outputs from the included scripts and inputs. They are not investment-performance claims.
