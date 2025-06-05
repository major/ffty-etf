"""Get the holdings of the FFTY IBD 50 ETF."""

import pandas as pd


def main():
    """Main function to execute the script."""
    # URL to the CSV file containing FFTY holdings
    # https://www.innovatoretfs.com/etf/default.aspx?ticker=ffty
    csv_url = "https://www.innovatoretfs.com/etf/xt_holdings.csv"

    # Read the CSV and get just the FFTY holdings.
    df = pd.read_csv(csv_url)
    ffty_holdings = df[df["Account"] == "FFTY"].sort_values("StockTicker")

    # Remove the cash holdings
    ffty_holdings = ffty_holdings[
        ~ffty_holdings["StockTicker"].isin(["Cash&Other", "8AMMF0JA0"])
    ]

    # Select the relevant columns
    ffty_holdings = ffty_holdings[
        ["StockTicker", "CUSIP", "SecurityName", "Weightings", "Shares", "Price"]
    ]

    # Write the holdings to markdown and CSV files
    ffty_holdings.to_markdown("ffty.md", index=False)
    ffty_holdings.to_csv("ffty.csv", index=False)


if __name__ == "__main__":
    main()
