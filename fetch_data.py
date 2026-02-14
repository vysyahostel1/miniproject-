"""Data collection module for NSE stock forecasting + DCF valuation pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
import yfinance as yf

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def fetch_price_data(ticker: str = "RELIANCE.NS", period: str = "6y") -> pd.DataFrame:
    """Fetch historical OHLCV data from Yahoo Finance and save to CSV."""
    history = yf.download(ticker, period=period, auto_adjust=False, progress=False)

    if history.empty:
        raise ValueError(f"No historical data returned for ticker: {ticker}")

    history = history.reset_index()
    history.to_csv(DATA_DIR / f"{ticker}_history.csv", index=False)
    return history


def fetch_financial_data(ticker: str = "RELIANCE.NS") -> pd.DataFrame:
    """Fetch annual financial statements; fallback to structured mock data if unavailable."""
    stock = yf.Ticker(ticker)

    financials = stock.financials
    cashflow = stock.cashflow

    if financials is None or cashflow is None or financials.empty or cashflow.empty:
        mock_financials = pd.DataFrame(
            {
                "Year": [2020, 2021, 2022, 2023, 2024],
                "OperatingCashFlow": [72000, 76000, 81000, 84500, 89000],
                "CapitalExpenditure": [-22000, -23500, -25000, -25800, -27000],
                "TotalDebt": [165000, 160500, 155000, 148500, 142000],
                "CashAndEquivalents": [18000, 20500, 24000, 27500, 29500],
                "SharesOutstanding": [6760, 6760, 6760, 6760, 6760],
            }
        )
        mock_financials.to_csv(DATA_DIR / f"{ticker}_financials.csv", index=False)
        return mock_financials

    ocf = cashflow.loc["Operating Cash Flow"] if "Operating Cash Flow" in cashflow.index else None
    capex = cashflow.loc["Capital Expenditure"] if "Capital Expenditure" in cashflow.index else None

    if ocf is None or capex is None:
        raise ValueError("Required financial statement fields unavailable for DCF computation.")

    df = pd.DataFrame(
        {
            "Year": pd.to_datetime(ocf.index).year,
            "OperatingCashFlow": ocf.values,
            "CapitalExpenditure": capex.values,
            "TotalDebt": 0.0,
            "CashAndEquivalents": 0.0,
            "SharesOutstanding": stock.info.get("sharesOutstanding", 0),
        }
    ).sort_values("Year")

    df.to_csv(DATA_DIR / f"{ticker}_financials.csv", index=False)
    return df


def fetch_all(ticker: str = "RELIANCE.NS") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch and persist both market and financial statement data."""
    return fetch_price_data(ticker=ticker), fetch_financial_data(ticker=ticker)


if __name__ == "__main__":
    prices_df, financials_df = fetch_all("RELIANCE.NS")
    print("Saved datasets:")
    print(f"- Price rows: {len(prices_df)}")
    print(f"- Financial rows: {len(financials_df)}")
