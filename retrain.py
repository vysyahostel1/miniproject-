"""Automated retraining pipeline based on RMSE threshold."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from dcf_model import dcf_valuation
from evaluate import evaluate_forecast, plot_actual_vs_predicted
from features import create_features
from fetch_data import fetch_all
from lstm_model import predict_next_7_days, save_model, train_lstm
from preprocessing import preprocess_price_data

METRICS_PATH = Path("metrics.json")
MODEL_PATH = Path("models/lstm_stock_model.h5")
PLOT_DIR = Path("plots")
PLOT_DIR.mkdir(exist_ok=True)


def plot_stock_history(df: pd.DataFrame, ticker: str) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df["Close"], label=f"{ticker} Close")
    plt.title(f"{ticker} Historical Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "stock_history.png")
    plt.close()


def run_pipeline(ticker: str = "RELIANCE.NS", rmse_threshold: float = 50.0) -> dict:
    prices_df, financial_df = fetch_all(ticker=ticker)
    plot_stock_history(prices_df, ticker)

    features_df = create_features(prices_df)
    train_df, test_df = preprocess_price_data(features_df)

    artifacts, y_test, y_pred = train_lstm(train_df, test_df, epochs=30)
    metrics = evaluate_forecast(y_test, y_pred)
    plot_actual_vs_predicted(y_test, y_pred)

    next_7_day_forecast = predict_next_7_days(artifacts, features_df)

    latest_market_price = float(prices_df["Close"].iloc[-1])
    dcf_result = dcf_valuation(financial_df=financial_df, latest_market_price=latest_market_price)

    retrained = False
    if metrics["RMSE"] > rmse_threshold:
        artifacts, y_test, y_pred = train_lstm(train_df, test_df, epochs=50)
        metrics = evaluate_forecast(y_test, y_pred)
        save_model(artifacts, str(MODEL_PATH))
        retrained = True
    else:
        save_model(artifacts, str(MODEL_PATH))

    result = {
        "ticker": ticker,
        "metrics": metrics,
        "retrained": retrained,
        "rmse_threshold": rmse_threshold,
        "next_7_day_forecast": [float(x) for x in next_7_day_forecast],
        "dcf": dcf_result,
    }

    METRICS_PATH.write_text(json.dumps(result, indent=2))

    print("\n=== Forecast Metrics ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    print("\n=== Next 7 Day Forecast ===")
    for i, value in enumerate(next_7_day_forecast, start=1):
        print(f"Day {i}: {value:.2f}")

    print("\n=== DCF Valuation Breakdown ===")
    print(f"WACC: {dcf_result['WACC']:.4f}")
    print(f"Base FCF: {dcf_result['BaseFCF']:.2f}")
    print(f"Intrinsic Share Price: {dcf_result['IntrinsicSharePrice']:.2f}")
    print(f"Latest Market Price: {dcf_result['LatestMarketPrice']:.2f}")
    print(f"Difference %: {dcf_result['DifferencePct']:.2f}")
    print(f"Decision: {dcf_result['Decision']}")

    return result


if __name__ == "__main__":
    run_pipeline()
