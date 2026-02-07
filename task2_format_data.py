
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUT_FILE = Path("formatted_output.csv")


def load_all_csvs(data_dir: Path) -> pd.DataFrame:
    files = sorted(data_dir.glob("daily_sales_data_*.csv"))
    if not files:
        raise FileNotFoundError(f"No daily_sales_data_*.csv files found in: {data_dir.resolve()}")
    return pd.concat((pd.read_csv(f) for f in files), ignore_index=True)  # combine CSVs [web:357]


def main() -> None:
    df = load_all_csvs(DATA_DIR)

    # Clean product names and filter to Pink Morsels (your data shows "pink morsel")
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df = df[df["product"].eq("pink morsel")]  # exact match after cleaning [web:423]

    # Clean price like "$3.00" -> 3.00
    df["price"] = (
        df["price"]
        .astype(str)
        .str.strip()
        .replace(r"[\$,]", "", regex=True)
        .astype(float)
    )  # remove $ and commas then convert [web:417]

    # Ensure quantity is numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Sales
    df["Sales"] = df["quantity"] * df["price"]

    # Output required columns only
    out = df[["Sales", "date", "region"]].rename(columns={"date": "Date", "region": "Region"})
    out["Date"] = pd.to_datetime(out["Date"], errors="coerce")
    out = out.dropna(subset=["Sales", "Date", "Region"])

    out.to_csv(OUT_FILE, index=False)
    print(f"Wrote {len(out)} rows to {OUT_FILE}")


if __name__ == "__main__":
    main()