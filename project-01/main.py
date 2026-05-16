"""
AI Expense Tracker
A smart console-based expense management system using core Python.
Author: Mahad (https://github.com/Mahad-lab)
"""

from colors import C, clr
from functions import add_expense, view_expenses, category_analysis, search_expense, delete_expense, ai_suggestions, monthly_summary, export_csv, set_budget
from utility import load_budget, load_expenses, hr, ask

# Menu
MENU = [
    ("Add Expense",        add_expense),
    ("View All Expenses",  view_expenses),
    ("Category Analysis",  category_analysis),
    ("Search Expense",     search_expense),
    ("Delete Expense",     delete_expense),
    ("AI Insights",        ai_suggestions),
    ("Monthly Summary",    monthly_summary),
    ("Export to CSV",      export_csv),
    ("Set Monthly Budget", set_budget),
    ("Exit",               None),
]

# Entry Point
def main():
    expenses = load_expenses()
    budget   = load_budget()

    print(clr("\n  ╔══════════════════════════════════╗", C.CYAN, C.BOLD))
    print(clr("  ║      AI  EXPENSE  TRACKER        ║", C.CYAN, C.BOLD))
    print(clr("  ╚══════════════════════════════════╝", C.CYAN, C.BOLD))

    while True:
        hr("Main Menu")
        for i, (label, _) in enumerate(MENU, 1):
            marker = clr(f"{i:2}.", C.CYAN)
            last   = clr(label, C.RED) if label == "Exit" else label
            print(f"  {marker} {last}")

        try:
            idx = int(ask("\n  Option")) - 1
            if not 0 <= idx < len(MENU):
                raise ValueError
        except (ValueError, TypeError):
            print(clr(f"  Enter 1-{len(MENU)}.", C.RED))
            continue

        label, fn = MENU[idx]
        if fn is None:
            print(clr("\n  Goodbye! Stay financially smart. 💰\n", C.GREEN))
            break

        try:
            fn(expenses, budget)
        except KeyboardInterrupt:
            print(clr("\n  Cancelled.", C.YELLOW))
        except Exception as ex:
            print(clr(f"  Unexpected error: {ex}", C.RED))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(clr("\n\n  Exiting. Goodbye!\n", C.YELLOW))