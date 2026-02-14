"""Discounted Cash Flow (DCF) valuation module."""

from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd


def calculate_wacc(risk_free_rate: float = 0.07, market_return: float = 0.12, beta: float = 1.1) -> float:
    """Calculate cost of equity via CAPM and use it as WACC (simplified)."""
    return risk_free_rate + beta * (market_return - risk_free_rate)


def calculate_fcf(financial_df: pd.DataFrame) -> pd.Series:
    """FCF = Operating Cash Flow + Capital Expenditure (capex is usually negative)."""
    if "OperatingCashFlow" not in financial_df.columns or "CapitalExpenditure" not in financial_df.columns:
        raise ValueError("Financial dataframe needs OperatingCashFlow and CapitalExpenditure columns.")

    return financial_df["OperatingCashFlow"] + financial_df["CapitalExpenditure"]


def dcf_valuation(
    financial_df: pd.DataFrame,
    latest_market_price: float,
    growth_rate: float = 0.05,
    terminal_growth_rate: float = 0.03,
) -> Dict[str, float | str | List[float]]:
    """Compute DCF intrinsic value per share and valuation signal."""
    wacc = calculate_wacc()
    fcfs = calculate_fcf(financial_df)

    base_fcf = float(fcfs.iloc[-1])
    projected_fcfs = [base_fcf * ((1 + growth_rate) ** i) for i in range(1, 6)]

    discounted_fcfs = [fcf / ((1 + wacc) ** i) for i, fcf in enumerate(projected_fcfs, start=1)]

    terminal_value = projected_fcfs[-1] * (1 + terminal_growth_rate) / (wacc - terminal_growth_rate)
    discounted_terminal_value = terminal_value / ((1 + wacc) ** 5)

    enterprise_value = float(np.sum(discounted_fcfs) + discounted_terminal_value)

    total_debt = float(financial_df["TotalDebt"].iloc[-1]) if "TotalDebt" in financial_df.columns else 0.0
    cash = float(financial_df["CashAndEquivalents"].iloc[-1]) if "CashAndEquivalents" in financial_df.columns else 0.0
    equity_value = enterprise_value - total_debt + cash

    shares = float(financial_df["SharesOutstanding"].iloc[-1]) if "SharesOutstanding" in financial_df.columns else 1.0
    shares = shares if shares > 0 else 1.0

    intrinsic_price = equity_value / shares

    diff_pct = ((intrinsic_price - latest_market_price) / latest_market_price) * 100
    if diff_pct > 10:
        decision = "Undervalued"
    elif diff_pct < -10:
        decision = "Overvalued"
    else:
        decision = "Fairly Valued"

    return {
        "WACC": wacc,
        "BaseFCF": base_fcf,
        "ProjectedFCF5Y": projected_fcfs,
        "DiscountedFCF5Y": discounted_fcfs,
        "TerminalValue": terminal_value,
        "EnterpriseValue": enterprise_value,
        "IntrinsicSharePrice": intrinsic_price,
        "LatestMarketPrice": latest_market_price,
        "DifferencePct": diff_pct,
        "Decision": decision,
    }
