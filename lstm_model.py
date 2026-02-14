"""LSTM model creation, training, and 7-day forecasting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

MODEL_DIR = Path("models")
PLOT_DIR = Path("plots")
MODEL_DIR.mkdir(exist_ok=True)
PLOT_DIR.mkdir(exist_ok=True)


@dataclass
class LSTMArtifacts:
    model: Sequential
    scaler_x: MinMaxScaler
    scaler_y: MinMaxScaler
    history: Dict[str, list]


def _reshape_lstm(X: np.ndarray) -> np.ndarray:
    return X.reshape(X.shape[0], 1, X.shape[1])


def train_lstm(train_df: pd.DataFrame, test_df: pd.DataFrame, epochs: int = 30) -> Tuple[LSTMArtifacts, np.ndarray, np.ndarray]:
    feature_cols = ["Lag_1", "Lag_3", "Lag_7", "MA_20", "MA_50", "RSI_14", "Daily_Return"]

    X_train = train_df[feature_cols].values
    y_train = train_df[["Close"]].values
    X_test = test_df[feature_cols].values
    y_test = test_df[["Close"]].values

    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_train_scaled = scaler_x.fit_transform(X_train)
    X_test_scaled = scaler_x.transform(X_test)
    y_train_scaled = scaler_y.fit_transform(y_train)

    X_train_lstm = _reshape_lstm(X_train_scaled)
    X_test_lstm = _reshape_lstm(X_test_scaled)

    model = Sequential(
        [
            LSTM(64, activation="tanh", input_shape=(X_train_lstm.shape[1], X_train_lstm.shape[2])),
            Dropout(0.2),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse")

    history = model.fit(
        X_train_lstm,
        y_train_scaled,
        epochs=epochs,
        batch_size=32,
        validation_split=0.1,
        verbose=0,
    )

    y_pred_scaled = model.predict(X_test_lstm, verbose=0)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    plt.figure(figsize=(8, 4))
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.title("LSTM Training vs Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "training_validation_loss.png")
    plt.close()

    artifacts = LSTMArtifacts(
        model=model,
        scaler_x=scaler_x,
        scaler_y=scaler_y,
        history=history.history,
    )
    return artifacts, y_test, y_pred


def predict_next_7_days(model_artifacts: LSTMArtifacts, latest_feature_rows: pd.DataFrame) -> np.ndarray:
    """Predict next 7 closing prices by recursively using latest feature rows."""
    feature_cols = ["Lag_1", "Lag_3", "Lag_7", "MA_20", "MA_50", "RSI_14", "Daily_Return"]
    sequence = latest_feature_rows[feature_cols].copy().tail(7)

    if len(sequence) < 7:
        raise ValueError("Need at least 7 rows of engineered features for 7-day forecast.")

    preds = []
    for i in range(7):
        row = sequence.iloc[i : i + 1].values
        row_scaled = model_artifacts.scaler_x.transform(row)
        row_lstm = row_scaled.reshape(1, 1, row_scaled.shape[1])
        pred_scaled = model_artifacts.model.predict(row_lstm, verbose=0)
        pred = model_artifacts.scaler_y.inverse_transform(pred_scaled)[0, 0]
        preds.append(pred)

    return np.array(preds)


def save_model(model_artifacts: LSTMArtifacts, path: str = "models/lstm_stock_model.h5") -> None:
    model_artifacts.model.save(path)
