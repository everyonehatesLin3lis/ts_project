# Stock Market Project

This project studies daily stock data and applies three related tasks on the same dataset:

- exploratory data analysis
- statistical inference
- time-series forecasting
- survival analysis
- ranking

The goal is to work with historical stock prices, understand their behavior, test simple statistical claims, and then build shared models that can be applied across multiple stocks.

## Project structure

- [01_notebooks/01_EDA.ipynb](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/01_notebooks/01_EDA.ipynb)
  EDA, anomaly checks, correlations, and regime comparison
- [01_notebooks/02_hypotesis_testing.ipynb](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/01_notebooks/02_hypotesis_testing.ipynb)
  confidence intervals and hypothesis tests
- [02_magic/01_data/download_data.py](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/02_magic/01_data/download_data.py)
  downloads raw stock data with `yfinance`
- [02_magic/01_data/load_data.py](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/02_magic/01_data/load_data.py)
  loads and formats the raw CSV
- [02_magic/03_models/01_baseline.ipynb](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/02_magic/03_models/01_baseline.ipynb)
  simple baseline forecasting model
- [02_magic/03_models/02_forcasting_model.ipynb](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/02_magic/03_models/02_forcasting_model.ipynb)
  shared forecasting model for next-day close price
- [02_magic/03_models/03_survival.ipynb](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/02_magic/03_models/03_survival.ipynb)
  pooled survival model for time until a 5 percent next-day gain
- [02_magic/03_models/04_ranking.ipynb](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/02_magic/03_models/04_ranking.ipynb)
  ranking stocks by predicted next-day gain

## Data

Raw and engineered data are stored in:

- [02_magic/01_data/raw](/abs/c:/Users/Nitro/Desktop/Turing%20College/DS/3rd%20Module/3rd%20project/02_magic/01_data/raw)

Main files:

- `stock_prices.csv`
- `df_eda.csv`

The downloader currently includes 10 tickers:

- `AAPL`
- `MSFT`
- `AMZN`
- `GOOGL`
- `META`
- `JPM`
- `JNJ`
- `XOM`
- `PG`
- `HD`

## How to run

Recommended order:

1. Run `download_data.py` to refresh the raw data.
2. Run the EDA notebook and save the engineered dataset if needed.
3. Run the hypothesis testing notebook.
4. Run the baseline model notebook.
5. Run the forecasting notebook.
6. Run the survival notebook.
7. Run the ranking notebook.

## Notes

- The modeling notebooks use one shared model across all stocks and then evaluate performance by ticker.
- The forecasting notebook predicts next-day closing price directly.
- The ranking notebook ranks stocks by predicted next-day price gain and compares against a simple price-momentum baseline.
- If the ticker list changes, the notebooks should be rerun so the saved outputs and markdown stay aligned with the latest results.
