"""Evaluation utilities for price forecasts."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

PLOT_DIR = Path("plots")
PLOT_DIR.mkdir(exist_ok=True)


def evaluate_forecast(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    return {"MAE": float(mae), "RMSE": float(rmse), "MAPE": float(mape)}


def plot_actual_vs_predicted(y_true: np.ndarray, y_pred: np.ndarray, title: str = "Actual vs Predicted Prices") -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(y_true, label="Actual")
    plt.plot(y_pred, label="Predicted")
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "actual_vs_predicted.png")
    plt.close()
