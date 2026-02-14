"""Preprocessing utilities for stock time-series."""

from __future__ import annotations

from typing import Tuple

import pandas as pd


def preprocess_price_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Clean data and create chronological 80-20 train-test split."""
    work_df = df.copy()

    if "Date" not in work_df.columns:
        raise ValueError("Input dataframe must have a 'Date' column.")

    work_df["Date"] = pd.to_datetime(work_df["Date"])
    work_df = work_df.sort_values("Date")
    work_df = work_df.ffill().bfill()

    split_idx = int(len(work_df) * 0.8)
    train_df = work_df.iloc[:split_idx].copy()
    test_df = work_df.iloc[split_idx:].copy()

    return train_df, test_df
