# Stock Price Forecasting + DCF Valuation (NSE)

This project provides an end-to-end implementation for:

- Historical stock data collection for Indian NSE stocks (default `RELIANCE.NS`)
- Feature engineering and LSTM-based next-price forecasting
- Forecast evaluation (`MAE`, `RMSE`, `MAPE`)
- Intrinsic value estimation with a DCF model
- Automated retraining when model RMSE exceeds a threshold

## Project Structure

- `fetch_data.py` - Collects stock history and financial data from `yfinance` (with mock fallback)
- `preprocessing.py` - Cleans and splits data into train/test chronologically (80/20)
- `features.py` - Creates lag features, moving averages, RSI, and daily returns
- `lstm_model.py` - Trains LSTM, saves loss plot, predicts next 7 days, and saves model
- `evaluate.py` - Calculates metrics and plots actual vs predicted
- `dcf_model.py` - Calculates WACC, FCF forecasts, terminal value, and intrinsic price
- `retrain.py` - Runs full pipeline, retrains on RMSE threshold breach, saves `metrics.json`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python retrain.py
```

Artifacts generated:
- `data/*.csv`
- `plots/stock_history.png`
- `plots/training_validation_loss.png`
- `plots/actual_vs_predicted.png`
- `models/lstm_stock_model.h5`
- `metrics.json`
