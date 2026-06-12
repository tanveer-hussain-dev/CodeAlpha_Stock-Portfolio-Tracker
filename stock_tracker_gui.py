# ============================================================
#   STOCK PORTFOLIO TRACKER — GUI VERSION
#   CodeAlpha Python Internship — Task 2
#   Author  : [Your Name]
#   Version : 2.0  (Tkinter GUI)
# ============================================================

import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ── Color Palette ─────────────────────────────────────────
BG_DARK      = "#0f0f1a"
BG_CARD      = "#1a1a2e"
BG_PANEL     = "#16213e"
ACCENT_BLUE  = "#4cc9f0"
ACCENT_GREEN = "#4ade80"
ACCENT_RED   = "#f72585"
ACCENT_GOLD  = "#fbbf24"
TEXT_WHITE   = "#e2e8f0"
TEXT_DIM     = "#64748b"
BTN_BG       = "#1e293b"

# ── Stock Data ────────────────────────────────────────────
STOCK_PRICES = {
    "AAPL":  182.50,
    "TSLA":  248.00,
    "GOOGL": 175.30,
    "MSFT":  415.20,
    "AMZN":  192.80,
    "META":  530.00,
    "NFLX":  680.00,
    "NVDA":  875.00,
}
COMPANY_NAMES = {
    "AAPL": "Apple", "TSLA": "Tesla", "GOOGL": "Google",
    "MSFT": "Microsoft", "AMZN": "Amazon", "META": "Meta",
    "NFLX": "Netflix", "NVDA": "NVIDIA",
}


# ════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════

class StockApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.portfolio: list = []
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        self.root.title("Stock Portfolio Tracker — CodeAlpha")
        self.root.geometry("950x700")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 950) // 2
        y = (self.root.winfo_screenheight() - 700) // 2
        self.root.geometry(f"950x700+{x}+{y}")

    # ── UI Builder ────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(fill="x", padx=30, pady=(20, 0))
        tk.Label(hdr, text="📈  STOCK PORTFOLIO TRACKER",
                 font=("Courier New", 22, "bold"),
                 fg=ACCENT_BLUE, bg=BG_DARK).pack(side="left")
        tk.Label(hdr, text="CodeAlpha  •  Task 2",
                 font=("Courier New", 10), fg=TEXT_DIM, bg=BG_DARK).pack(side="right", pady=8)
        tk.Frame(self.root, bg=ACCENT_BLUE, height=2).pack(fill="x", padx=30, pady=(6, 14))

        # ── Two columns ──────────────────────────────────
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=30)

        # LEFT — Add stock panel
        left = tk.Frame(body, bg=BG_CARD, width=290)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)
        self._build_left_panel(left)

        # RIGHT — Portfolio table
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)
        self._build_right_panel(right)

        # Bottom bar
        self._build_bottom_bar()

    def _build_left_panel(self, parent):
        tk.Label(parent, text="ADD STOCK", font=("Courier New", 11, "bold"),
                 fg=ACCENT_GOLD, bg=BG_CARD).pack(anchor="w", padx=16, pady=(18, 12))

        # Available stocks list
        tk.Label(parent, text="Select Stock", font=("Courier New", 9),
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=16)

        self.stock_var = tk.StringVar(value="AAPL")
        stock_frame = tk.Frame(parent, bg=BG_CARD)
        stock_frame.pack(fill="x", padx=16, pady=(4, 12))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TCombobox",
                        fieldbackground=BG_PANEL,
                        background=BG_PANEL,
                        foreground=TEXT_WHITE,
                        selectbackground=ACCENT_BLUE,
                        selectforeground=BG_DARK,
                        arrowcolor=ACCENT_BLUE)

        self.combo = ttk.Combobox(stock_frame, textvariable=self.stock_var,
                                  values=list(STOCK_PRICES.keys()),
                                  state="readonly", width=22,
                                  style="Dark.TCombobox",
                                  font=("Courier New", 11))
        self.combo.pack(fill="x")
        self.combo.bind("<<ComboboxSelected>>", self._on_stock_select)

        # Price preview
        self.price_preview = tk.Label(parent, text="Price: $182.50",
                                      font=("Courier New", 10),
                                      fg=ACCENT_GREEN, bg=BG_CARD)
        self.price_preview.pack(anchor="w", padx=16, pady=(0, 10))

        # Quantity
        tk.Label(parent, text="Quantity", font=("Courier New", 9),
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=16)

        self.qty_var = tk.StringVar(value="1")
        qty_entry = tk.Entry(parent, textvariable=self.qty_var,
                             font=("Courier New", 13, "bold"),
                             bg=BG_PANEL, fg=TEXT_WHITE,
                             insertbackground=ACCENT_BLUE,
                             relief="flat", bd=6, width=22)
        qty_entry.pack(fill="x", padx=16, pady=(4, 6))

        # Total preview
        self.total_preview = tk.Label(parent, text="Total: $182.50",
                                      font=("Courier New", 10, "bold"),
                                      fg=ACCENT_GOLD, bg=BG_CARD)
        self.total_preview.pack(anchor="w", padx=16, pady=(0, 14))
        self.qty_var.trace_add("write", self._update_preview)

        # Add button
        tk.Button(parent, text="＋  ADD TO PORTFOLIO",
                  font=("Courier New", 10, "bold"),
                  bg=ACCENT_BLUE, fg=BG_DARK,
                  relief="flat", pady=8, cursor="hand2",
                  command=self._add_stock).pack(fill="x", padx=16, pady=(0, 6))

        # Remove button
        tk.Button(parent, text="✕  REMOVE SELECTED",
                  font=("Courier New", 10, "bold"),
                  bg=BTN_BG, fg=ACCENT_RED,
                  relief="flat", pady=8, cursor="hand2",
                  command=self._remove_stock).pack(fill="x", padx=16, pady=(0, 20))

        # Divider
        tk.Frame(parent, bg=TEXT_DIM, height=1).pack(fill="x", padx=16, pady=(0, 14))

        # Available stocks reference
        tk.Label(parent, text="MARKET PRICES",
                 font=("Courier New", 9, "bold"),
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", padx=16, pady=(0, 6))

        for sym, price in STOCK_PRICES.items():
            row = tk.Frame(parent, bg=BG_CARD)
            row.pack(fill="x", padx=16, pady=1)
            tk.Label(row, text=sym, font=("Courier New", 9, "bold"),
                     fg=ACCENT_BLUE, bg=BG_CARD, width=6, anchor="w").pack(side="left")
            tk.Label(row, text=f"${price:,.2f}", font=("Courier New", 9),
                     fg=TEXT_WHITE, bg=BG_CARD).pack(side="right")

    def _build_right_panel(self, parent):
        tk.Label(parent, text="MY PORTFOLIO", font=("Courier New", 11, "bold"),
                 fg=ACCENT_GOLD, bg=BG_DARK).pack(anchor="w", pady=(0, 8))

        # Table
        table_frame = tk.Frame(parent, bg=BG_DARK)
        table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=BG_CARD,
                        foreground=TEXT_WHITE,
                        fieldbackground=BG_CARD,
                        rowheight=34,
                        font=("Courier New", 10))
        style.configure("Dark.Treeview.Heading",
                        background=BG_PANEL,
                        foreground=ACCENT_BLUE,
                        font=("Courier New", 10, "bold"),
                        relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", ACCENT_BLUE)],
                  foreground=[("selected", BG_DARK)])

        cols = ("Symbol", "Company", "Qty", "Price", "Total Value")
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                 show="headings", style="Dark.Treeview",
                                 height=14)

        widths = [80, 130, 70, 110, 130]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=w, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Summary row
        summary = tk.Frame(parent, bg=BG_PANEL)
        summary.pack(fill="x", pady=(10, 0))

        tk.Label(summary, text="TOTAL INVESTMENT",
                 font=("Courier New", 10, "bold"),
                 fg=TEXT_DIM, bg=BG_PANEL).pack(side="left", padx=16, pady=10)

        self.total_label = tk.Label(summary, text="$0.00",
                                    font=("Courier New", 18, "bold"),
                                    fg=ACCENT_GREEN, bg=BG_PANEL)
        self.total_label.pack(side="right", padx=16, pady=10)

    def _build_bottom_bar(self):
        bar = tk.Frame(self.root, bg=BG_PANEL)
        bar.pack(fill="x", padx=30, pady=(12, 16))

        tk.Button(bar, text="💾  SAVE TO CSV",
                  font=("Courier New", 10, "bold"),
                  bg=ACCENT_GREEN, fg=BG_DARK,
                  relief="flat", padx=18, pady=7,
                  cursor="hand2",
                  command=self._save_csv).pack(side="left", padx=(12, 6), pady=8)

        tk.Button(bar, text="🗑  CLEAR ALL",
                  font=("Courier New", 10, "bold"),
                  bg=BTN_BG, fg=ACCENT_RED,
                  relief="flat", padx=18, pady=7,
                  cursor="hand2",
                  command=self._clear_all).pack(side="left", padx=6, pady=8)

        self.status_bar = tk.Label(bar, text="Ready — Add stocks to your portfolio.",
                                   font=("Courier New", 9, "italic"),
                                   fg=TEXT_DIM, bg=BG_PANEL)
        self.status_bar.pack(side="right", padx=16)

    # ── Event Handlers ────────────────────────────────────
    def _on_stock_select(self, event=None):
        sym = self.stock_var.get()
        self.price_preview.config(text=f"Price: ${STOCK_PRICES[sym]:,.2f}")
        self._update_preview()

    def _update_preview(self, *args):
        try:
            qty = int(self.qty_var.get())
            sym = self.stock_var.get()
            total = qty * STOCK_PRICES[sym]
            self.total_preview.config(text=f"Total: ${total:,.2f}")
        except (ValueError, KeyError):
            self.total_preview.config(text="Total: —")

    def _add_stock(self):
        sym = self.stock_var.get()
        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive quantity.")
            return

        # Update or add
        for entry in self.portfolio:
            if entry["symbol"] == sym:
                entry["quantity"] += qty
                self._refresh_table()
                self._set_status(f"Updated {sym}: +{qty} shares added.")
                return

        self.portfolio.append({"symbol": sym, "quantity": qty})
        self._refresh_table()
        self._set_status(f"Added {qty} × {sym} ({COMPANY_NAMES[sym]}) to portfolio.")

    def _remove_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Row", "Please click a stock row to select it first.")
            return
        item  = self.tree.item(selected[0])
        sym   = item["values"][0]
        self.portfolio = [e for e in self.portfolio if e["symbol"] != sym]
        self._refresh_table()
        self._set_status(f"Removed {sym} from portfolio.")

    def _clear_all(self):
        if not self.portfolio:
            return
        if messagebox.askyesno("Clear Portfolio", "Remove all stocks from portfolio?"):
            self.portfolio.clear()
            self._refresh_table()
            self._set_status("Portfolio cleared.")

    def _save_csv(self):
        if not self.portfolio:
            messagebox.showinfo("Empty", "Portfolio is empty. Add stocks first.")
            return
        filename = "portfolio.csv"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Company", "Quantity",
                             "Price (USD)", "Total Value (USD)", "Saved At"])
            grand = 0.0
            for e in self.portfolio:
                price = STOCK_PRICES[e["symbol"]]
                total = price * e["quantity"]
                grand += total
                writer.writerow([e["symbol"], COMPANY_NAMES[e["symbol"]],
                                 e["quantity"], f"{price:.2f}",
                                 f"{total:.2f}", timestamp])
            writer.writerow([])
            writer.writerow(["", "", "", "GRAND TOTAL",
                             f"{grand:.2f}", timestamp])
        self._set_status(f"✔ Saved to '{filename}' successfully!")
        messagebox.showinfo("Saved", f"Portfolio saved to '{filename}'")

    # ── Refresh table ──────────────────────────────────────
    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        grand = 0.0
        for e in self.portfolio:
            sym   = e["symbol"]
            qty   = e["quantity"]
            price = STOCK_PRICES[sym]
            total = price * qty
            grand += total
            self.tree.insert("", "end", values=(
                sym,
                COMPANY_NAMES[sym],
                qty,
                f"${price:,.2f}",
                f"${total:,.2f}",
            ))

        self.total_label.config(text=f"${grand:,.2f}")

    def _set_status(self, msg: str):
        self.status_bar.config(text=msg)


# ════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = StockApp(root)
    root.mainloop()
