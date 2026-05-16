from datetime import datetime, date
from colors import C, clr
from config import CATEGORIES, DATA_FILE, BUDGET_FILE
import json

# Persistence
def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def dump_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_expenses()  : return load_json(DATA_FILE,   [])
def save_expenses(e) : dump_json(DATA_FILE, e)
def load_budget()    : return load_json(BUDGET_FILE, {"limit": 50000})
def save_budget(b)   : dump_json(BUDGET_FILE, b)


# Utility Helpers
def today()           : return date.today().isoformat()
def fmt(n)            : return f"PKR {n:,.2f}"
def next_id(expenses) : return max((e["id"] for e in expenses), default=0) + 1

def hr(title=""):
    print(f"\n{clr('─' * 54, C.CYAN)}")
    if title:
        print(clr(f"  {title}", C.BOLD, C.CYAN))
        print(clr('─' * 54, C.CYAN))

def ask(label, default=None):
    hint = f" [{default}]" if default else ""
    val  = input(f"  {label}{hint}: ").strip()
    return val if val else default

def parse_date(s):
    for fmt_str in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt_str).date().isoformat()
        except (ValueError, TypeError):
            continue
    return today()

def pick_category():
    print("\n  " + "  ".join(f"{i}.{c}" for i, c in enumerate(CATEGORIES, 1)))
    try:
        return CATEGORIES[int(ask("Category #", "7")) - 1]
    except (ValueError, TypeError, IndexError):
        return "Other"

def progress_bar(pct, width=20):
    filled = int(pct / 100 * width)
    color  = C.GREEN if pct < 70 else C.YELLOW if pct < 90 else C.RED
    return clr("█" * filled, color) + clr("░" * (width - filled), C.RESET)
