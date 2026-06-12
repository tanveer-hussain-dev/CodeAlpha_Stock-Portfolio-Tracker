# ============================================================
#   STOCK PORTFOLIO TRACKER
#   CodeAlpha Python Internship — Task 2
#   Author  : [Your Name]
#   Version : 1.0
# ============================================================

import csv
import os
from datetime import datetime


# ── Hardcoded stock prices (USD) ─────────────────────────────
STOCK_PRICES: dict = {
    "AAPL":  182.50,   # Apple
    "TSLA":  248.00,   # Tesla
    "GOOGL": 175.30,   # Google
    "MSFT":  415.20,   # Microsoft
    "AMZN":  192.80,   # Amazon
    "META":  530.00,   # Meta
    "NFLX":  680.00,   # Netflix
    "NVDA":  875.00,   # NVIDIA
}

PORTFOLIO_FILE = "portfolio.csv"


# ── Display helpers ──────────────────────────────────────────

def show_available_stocks() -> None:
    """Print the list of available stocks with current prices."""
    print("\n" + "=" * 45)
    print(f"  {'SYMBOL':<8} {'COMPANY':<12} {'PRICE (USD)':>12}")
    print("-" * 45)
    company_names = {
        "AAPL": "Apple", "TSLA": "Tesla", "GOOGL": "Google",
        "MSFT": "Microsoft", "AMZN": "Amazon", "META": "Meta",
        "NFLX": "Netflix", "NVDA": "NVIDIA",
    }
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol:<8} {company_names[symbol]:<12} ${price:>11,.2f}")
    print("=" * 45)


def show_portfolio(portfolio: list) -> None:
    """Display the current portfolio in a formatted table."""
    if not portfolio:
        print("\n  ⚠  Portfolio is empty. Add stocks first.")
        return

    print("\n" + "=" * 60)
    print(f"  {'#':<4} {'SYMBOL':<8} {'QTY':>6} {'PRICE':>12} {'TOTAL VALUE':>14}")
    print("-" * 60)

    grand_total = 0.0
    for idx, entry in enumerate(portfolio, start=1):
        symbol   = entry["symbol"]
        qty      = entry["quantity"]
        price    = STOCK_PRICES[symbol]
        total    = price * qty
        grand_total += total
        print(f"  {idx:<4} {symbol:<8} {qty:>6} ${price:>11,.2f} ${total:>13,.2f}")

    print("-" * 60)
    print(f"  {'TOTAL INVESTMENT':>40} ${grand_total:>13,.2f}")
    print("=" * 60)


# ── Core functions ───────────────────────────────────────────

def add_stock(portfolio: list) -> None:
    """Prompt user to add a stock to the portfolio."""
    show_available_stocks()
    symbol = input("\n  Enter stock symbol (e.g. AAPL): ").strip().upper()

    if symbol not in STOCK_PRICES:
        print(f"  ❌  '{symbol}' is not in our stock list.")
        return

    try:
        qty = int(input(f"  Enter quantity for {symbol}: ").strip())
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  ❌  Quantity must be a positive whole number.")
        return

    # Update existing entry or add new one
    for entry in portfolio:
        if entry["symbol"] == symbol:
            entry["quantity"] += qty
            print(f"  ✅  Updated {symbol}: total {entry['quantity']} shares.")
            return

    portfolio.append({"symbol": symbol, "quantity": qty})
    print(f"  ✅  Added {qty} shares of {symbol}.")


def remove_stock(portfolio: list) -> None:
    """Remove a stock entry from the portfolio."""
    if not portfolio:
        print("\n  ⚠  Portfolio is empty.")
        return

    show_portfolio(portfolio)
    symbol = input("\n  Enter symbol to remove: ").strip().upper()

    for entry in portfolio:
        if entry["symbol"] == symbol:
            portfolio.remove(entry)
            print(f"  ✅  Removed {symbol} from portfolio.")
            return
    print(f"  ❌  {symbol} not found in portfolio.")


def save_portfolio(portfolio: list) -> None:
    """Save the current portfolio to a CSV file."""
    if not portfolio:
        print("\n  ⚠  Nothing to save — portfolio is empty.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PORTFOLIO_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Quantity", "Price (USD)", "Total Value (USD)", "Saved At"])
        grand_total = 0.0
        for entry in portfolio:
            price = STOCK_PRICES[entry["symbol"]]
            total = price * entry["quantity"]
            grand_total += total
            writer.writerow([entry["symbol"], entry["quantity"],
                             f"{price:.2f}", f"{total:.2f}", timestamp])
        writer.writerow([])
        writer.writerow(["", "", "GRAND TOTAL", f"{grand_total:.2f}", timestamp])

    print(f"\n  ✅  Portfolio saved to '{PORTFOLIO_FILE}'")


# ── Main menu ────────────────────────────────────────────────

def main() -> None:
    """Entry point — interactive portfolio tracker menu."""
    portfolio: list = []

    print("\n" + "=" * 45)
    print("   📈  STOCK PORTFOLIO TRACKER  📈")
    print("        CodeAlpha — Task 2")
    print("=" * 45)

    menu = {
        "1": ("Add Stock",          lambda: add_stock(portfolio)),
        "2": ("View Portfolio",     lambda: show_portfolio(portfolio)),
        "3": ("Remove Stock",       lambda: remove_stock(portfolio)),
        "4": ("Save to CSV",        lambda: save_portfolio(portfolio)),
        "5": ("Exit",               None),
    }

    while True:
        print("\n  ── MENU ──────────────────────────────")
        for key, (label, _) in menu.items():
            print(f"  [{key}] {label}")
        print("  ──────────────────────────────────────")

        choice = input("  Choose an option: ").strip()

        if choice == "5":
            print("\n  Goodbye! Happy Investing 💰\n")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("  ❌  Invalid choice. Please enter 1–5.")


# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
