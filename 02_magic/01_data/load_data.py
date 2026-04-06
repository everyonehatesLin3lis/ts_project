from pathlib import Path
import pandas as pd


# This file lives in: 02_magic/01_data/load_data.py
CURRENT_DIR = Path(__file__).resolve().parent
INPUT_FILE = CURRENT_DIR / "raw" / "stock_prices.csv"


def load_stock_data(file_path: Path = INPUT_FILE) -> pd.DataFrame:
    """
    Load stock data from the raw CSV file.

    Parameters
    ----------
    file_path : Path
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded and formatted stock dataframe.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}\n"
            f"Run download_data.py first."
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("Loaded file is empty.")

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df.dropna(subset=["Date"])

    numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    existing_numeric_cols = [col for col in numeric_cols if col in df.columns]

    for col in existing_numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if {"Ticker", "Date"}.issubset(df.columns):
        df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)
    else:
        df = df.sort_values("Date").reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = load_stock_data()

    print("Data loaded successfully.")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nHead:")
    print(df.head())