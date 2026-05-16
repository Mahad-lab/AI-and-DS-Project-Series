from utility import hr, ask, C, clr, pick_category, fmt, parse_date, today, next_id, progress_bar, save_budget, save_expenses
from datetime import date
from collections import defaultdict
import csv

# Feature: Add ──────────────────────────────────────────────────────────────
def add_expense(expenses, _budget):
    hr("Add New Expense")
    title = ask("Title")
    if not title:
        print(clr("  Title is required.", C.RED)); return

    try:
        amount = float(ask("Amount (PKR)"))
        if amount <= 0: raise ValueError
    except (ValueError, TypeError):
        print(clr("  Invalid amount.", C.RED)); return

    category = pick_category()
    date_str = parse_date(ask("Date (YYYY-MM-DD)", today()))
    note     = ask("Note (optional)", "") or ""

    expenses.append({
        "id": next_id(expenses), "title": title, "amount": amount,
        "category": category,   "date": date_str, "note": note
    })
    save_expenses(expenses)
    print(clr(f"\n  ✓ '{title}' added ({fmt(amount)}).", C.GREEN))

# Feature: View ─────────────────────────────────────────────────────────────
def view_expenses(expenses, _budget, subset=None):
    data = subset if subset is not None else expenses
    hr(f"Expenses  [{len(data)} records]")
    if not data:
        print(clr("  No records found.", C.YELLOW)); return

    print(f"  {'ID':<4} {'Date':<12} {'Category':<15} {'Amount':>12}  Title")
    print(clr("  " + "─" * 60, C.CYAN))
    for e in sorted(data, key=lambda x: x["date"], reverse=True):
        note = f"  ({e['note']})" if e.get("note") else ""
        print(f"  {e['id']:<4} {e['date']:<12} {e['category']:<15} "
              f"{fmt(e['amount']):>12}  {e['title']}{note}")

    total = sum(e["amount"] for e in data)
    print(clr("  " + "─" * 60, C.CYAN))
    print(clr(f"  {'TOTAL':>45} {fmt(total):>12}", C.BOLD))

# Feature: Category Analysis ────────────────────────────────────────────────
def category_analysis(expenses, _budget):
    hr("Category Analysis")
    if not expenses:
        print(clr("  No data available.", C.YELLOW)); return

    totals = defaultdict(float)
    counts = defaultdict(int)
    for e in expenses:
        totals[e["category"]] += e["amount"]
        counts[e["category"]] += 1

    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    grand  = sum(totals.values())

    print(f"  {'Category':<16} {'Txns':>5} {'Amount':>14} {'Share':>7}  Chart")
    print(clr("  " + "─" * 60, C.CYAN))
    for i, (cat, amt) in enumerate(ranked):
        pct  = (amt / grand) * 100
        bar  = progress_bar(pct, width=12)
        flag = clr(" ◀ HIGHEST", C.RED)  if i == 0          else \
               clr(" ◀ LOWEST",  C.GREEN) if i == len(ranked)-1 else ""
        print(f"  {cat:<16} {counts[cat]:>5} {fmt(amt):>14} {pct:>6.1f}%  {bar}{flag}")

# Feature: Search ───────────────────────────────────────────────────────────
def search_expense(expenses, budget):
    hr("Search")
    print("  1. By Category  2. By Date  3. By Title")
    choice = ask("Option", "1")

    if choice == "1":
        cat     = pick_category()
        results = [e for e in expenses if e["category"] == cat]
    elif choice == "2":
        d       = parse_date(ask("Date (YYYY-MM-DD)", today()))
        results = [e for e in expenses if e["date"] == d]
    else:
        term    = (ask("Keyword") or "").lower()
        results = [e for e in expenses if term in e["title"].lower()]

    view_expenses(expenses, budget, subset=results)

# Feature: Delete ───────────────────────────────────────────────────────────
def delete_expense(expenses, budget):
    view_expenses(expenses, budget)
    try:
        eid = int(ask("\n  ID to delete"))
        idx = next((i for i, e in enumerate(expenses) if e["id"] == eid), None)
        if idx is None:
            print(clr("  ID not found.", C.RED)); return
        title = expenses.pop(idx)["title"]
        save_expenses(expenses)
        print(clr(f"  ✓ '{title}' deleted.", C.GREEN))
    except (ValueError, TypeError):
        print(clr("  Invalid ID.", C.RED))

# Feature: AI Insights ──────────────────────────────────────────────────────
def ai_suggestions(expenses, budget):
    hr("AI Spending Insights")
    if not expenses:
        print(clr("  Add expenses to unlock insights.", C.YELLOW)); return

    limit     = budget["limit"]
    now       = date.today()
    prefix    = f"{now.year}-{now.month:02d}"
    monthly   = [e for e in expenses if e["date"].startswith(prefix)]
    total_m   = sum(e["amount"] for e in monthly)
    pct_used  = min((total_m / limit) * 100, 100)

    print(f"\n  📅 {now.strftime('%B %Y')} — {len(monthly)} transactions\n")

    # Budget bar
    print(f"  Budget:  {progress_bar(pct_used)}  {pct_used:.1f}%  ({fmt(total_m)} / {fmt(limit)})")
    if total_m > limit:
        print(clr(f"\n  ⚠️  Over budget by {fmt(total_m - limit)}! Cut discretionary spending.", C.RED))
    elif pct_used >= 80:
        print(clr(f"\n  ⚠️  {fmt(limit - total_m)} left — spend carefully.", C.YELLOW))
    else:
        print(clr(f"\n  ✅  {fmt(limit - total_m)} remaining. You're on track!", C.GREEN))

    # Category insights
    cat_totals = defaultdict(float)
    for e in expenses:
        cat_totals[e["category"]] += e["amount"]

    if cat_totals:
        top, top_amt = max(cat_totals.items(), key=lambda x: x[1])
        tips = {
            "Food":          "🍱 Meal-prep can cut food costs by up to 40%.",
            "Entertainment": "🎮 Entertainment dominates. Try free/low-cost alternatives.",
            "Shopping":      "🛍️  Delay non-essential purchases 48 hrs before buying.",
            "Transport":     "🚌 Carpooling or public transit can save significantly.",
        }
        if top in tips:
            print(clr(f"\n  💡 Top Category [{top}]: {tips[top]}", C.YELLOW))

    # Daily average & projection
    days_passed = max(now.day, 1)
    daily_avg   = total_m / days_passed
    projected   = daily_avg * 30
    save_target = projected * 0.20

    print(f"\n  📊 Daily Avg:   {fmt(daily_avg)}")
    print(f"  🔮 Projection:  {fmt(projected)}  (this month)")
    print(clr(f"  💰 Save Target: {fmt(save_target)}  (20% rule)", C.CYAN))

    if projected > limit:
        print(clr(f"\n  🚨 Projected to exceed budget by {fmt(projected - limit)}.", C.RED))

# Feature: Export CSV ───────────────────────────────────────────────────────
def export_csv(expenses, _budget):
    filename = f"expenses_{today()}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "category", "amount", "title", "note"])
        writer.writeheader()
        writer.writerows(expenses)
    print(clr(f"\n  ✓ Exported → {filename}", C.GREEN))

# Feature: Set Budget ───────────────────────────────────────────────────────
def set_budget(expenses, budget):
    hr("Monthly Budget")
    print(f"  Current: {fmt(budget['limit'])}")
    try:
        val = float(ask("New limit (PKR)"))
        if val <= 0: raise ValueError
        budget["limit"] = val
        save_budget(budget)
        print(clr(f"  ✓ Budget set to {fmt(val)}", C.GREEN))
    except (ValueError, TypeError):
        print(clr("  Invalid amount.", C.RED))

# Feature: Monthly Summary ──────────────────────────────────────────────────
def monthly_summary(expenses, _budget):
    hr("Monthly Summary")
    if not expenses:
        print(clr("  No data.", C.YELLOW)); return

    monthly = defaultdict(list)
    for e in expenses:
        key = e["date"][:7]  # YYYY-MM
        monthly[key].append(e["amount"])

    print(f"  {'Month':<10} {'Txns':>5} {'Total':>15}")
    print(clr("  " + "─" * 34, C.CYAN))
    for month in sorted(monthly, reverse=True):
        amounts = monthly[month]
        print(f"  {month:<10} {len(amounts):>5} {fmt(sum(amounts)):>15}")
