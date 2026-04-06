from pathlib import Path
from typing import List

import pandas as pd
import yfinance as yf


TICKERS: List[str] = ["AAPL", "MSFT", "AMZN", "GOOGL", "META"]
START_DATE = "2010-01-01"

# This file lives in: 02_magic/01_data/download_data.py
CURRENT_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = CURRENT_DIR / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RAW_DATA_DIR / "stock_prices.csv"


def download_stock_data(
    tickers: List[str] = TICKERS,
    start_date: str = START_DATE,
    output_file: Path = OUTPUT_FILE,
) -> pd.DataFrame:
    """
    Download daily stock data from Yahoo Finance and save it as a CSV file.

    Parameters
    ----------
    tickers : List[str]
        List of stock tickers to download.
    start_date : str
        Start date in YYYY-MM-DD format.
    output_file : Path
        Full path to output CSV file.

    Returns
    -------
    pd.DataFrame
        Combined stock dataset.
    """
    all_data = []

    for ticker in tickers:
        print(f"Downloading data for {ticker}...")

        df = yf.download(
            ticker,
            start=start_date,
            progress=False,
            auto_adjust=False,
        )

        if df.empty:
            print(f"Warning: no data returned for {ticker}")
            continue

        df = df.reset_index()

        # Flatten columns if yfinance returns MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                col[0] if isinstance(col, tuple) else col
                for col in df.columns
            ]

        df["Ticker"] = ticker
        all_data.append(df)

    if not all_data:
        raise ValueError(
            "No data was downloaded. Check ticker names or internet connection."
        )

    combined_df = pd.concat(all_data, ignore_index=True)

    expected_columns = [
        "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "Ticker"
    ]
    existing_columns = [col for col in expected_columns if col in combined_df.columns]
    combined_df = combined_df[existing_columns]

    combined_df["Date"] = pd.to_datetime(combined_df["Date"], errors="coerce")
    combined_df = combined_df.dropna(subset=["Date"])

    combined_df = combined_df.sort_values(["Ticker", "Date"]).reset_index(drop=True)
    combined_df.to_csv(output_file, index=False)

    print(f"\nData saved successfully to:\n{output_file}")
    print(f"Shape: {combined_df.shape}")

    return combined_df


if __name__ == "__main__":
    download_stock_data()