"""Get the holdings of the FFTY IBD 50 ETF."""

import polars as pl


def main():
    """Main function to execute the script."""
    # URL to the CSV file containing FFTY holdings
    # https://www.innovatoretfs.com/etf/default.aspx?ticker=ffty
    csv_url = "https://www.innovatoretfs.com/etf/xt_holdings.csv"

    # Read the CSV and get just the FFTY holdings.
    df = pl.read_csv(csv_url)
    ffty_holdings = df.filter(pl.col("Account") == "FFTY")

    # Remove the cash holdings
    ffty_holdings = (
        ffty_holdings.filter(~pl.col("StockTicker").is_in(["Cash&Other", "8AMMF0JA0"]))
        .with_columns(pl.col("Weightings").str.strip_chars("%").cast(pl.Float64))
        .select(["StockTicker", "SecurityName"])
        .sort("StockTicker")
    )

    # Write the holdings to markdown and CSV files
    with open("ffty.md", "w") as f:
        # Write markdown table header
        headers = ffty_holdings.columns
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "|".join([":--"] * len(headers)) + "|\n")
        
        # Write data rows
        for row in ffty_holdings.rows():
            f.write("| " + " | ".join(str(cell) for cell in row) + " |\n")

    ffty_holdings.write_csv("ffty.csv")


if __name__ == "__main__":
    main()
