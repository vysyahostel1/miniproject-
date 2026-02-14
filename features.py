"""Feature engineering functions for stock forecasting."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Compute Relative Strength Index (RSI)."""
    delta = close.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)

    gain_series = pd.Series(gain, index=close.index).rolling(window=period).mean()
    loss_series = pd.Series(loss, index=close.index).rolling(window=period).mean()

    rs = gain_series / loss_series.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create lag, moving averages, RSI, and return based features."""
    feat_df = df.copy()

    if "Close" not in feat_df.columns:
        raise ValueError("Input dataframe must include 'Close' column.")

    feat_df["Lag_1"] = feat_df["Close"].shift(1)
    feat_df["Lag_3"] = feat_df["Close"].shift(3)
    feat_df["Lag_7"] = feat_df["Close"].shift(7)

    feat_df["MA_20"] = feat_df["Close"].rolling(window=20).mean()
    feat_df["MA_50"] = feat_df["Close"].rolling(window=50).mean()

    feat_df["RSI_14"] = compute_rsi(feat_df["Close"], period=14)
    feat_df["Daily_Return"] = feat_df["Close"].pct_change()

    feat_df = feat_df.dropna().reset_index(drop=True)
    return feat_df
