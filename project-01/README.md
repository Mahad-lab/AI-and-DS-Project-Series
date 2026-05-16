# AI Expense Tracker

A smart, menu-driven console application for tracking personal expenses — built entirely with core Python, no external libraries.

---

## Overview

Managing money is easy to ignore until it's too late. This project solves that by giving users a fast, keyboard-driven tool to record, categorize, search, and analyze their daily spending — plus logic-based AI suggestions that flag overspending and recommend savings targets.

Built as **Project 01** of a AI DS Project Series. Every feature uses only the Python standard library, making it a clean demonstration of real-world problem-solving without framework shortcuts.

---

## Features

| Feature | Description |
|---|---|
| **Add Expense** | Record title, amount, category, date, and optional note |
| **View Expenses** | Sorted table with running total |
| **Category Analysis** | Ranked breakdown with percentage share and inline bar chart |
| **Search** | Filter by category, date, or keyword |
| **Delete Expense** | Remove any record by ID |
| **AI Insights** | Budget progress bar, daily average, monthly projection, 20% savings rule, category-specific tips |
| **Monthly Summary** | Spending totals grouped by month |
| **Export to CSV** | One-click export with today's date in the filename |
| **Set Budget** | Persistent monthly budget limit stored in `budget.json` |

---

## Project Structure

```
project-01/
├── main.py          # Entry point — menu loop and dispatch table
├── functions.py     # Core features (add, view, search, delete, insights, export)
├── utility.py       # Shared helpers (prompt, date parsing, progress bar, file I/O)
├── colors.py        # Terminal color constants and clr() formatter
├── config.py        # Categories list, file paths, default budget
├── expenses.json    # Persistent expense records (auto-created)
└── budget.json      # Persistent budget setting (auto-created)
```

### Why multiple files?

| File | Responsibility |
|---|---|
| `config.py` | Single source of truth for constants — change a file path or add a category in one place |
| `colors.py` | Isolated so color codes can be swapped or disabled without touching business logic |
| `utility.py` | Pure helpers with no side effects — easy to test independently |
| `functions.py` | One function per feature — open for extension, easy to read |
| `main.py` | Thin orchestration only — loads data, runs the loop, dispatches to functions |

This separation follows the **Single Responsibility Principle**: each file has one reason to change.

---

## Setup & Usage

**Requirements:** Python 3.8+ (standard library only)

```bash
cd project-01
python main.py
```

On first run, `expenses.json` and `budget.json` are created automatically.

**Navigation:** Type the menu number and press Enter. Use `Ctrl+C` at any prompt to cancel back to the menu.

---

## Data Storage

Expenses are persisted in `expenses.json` — a human-readable format that can be inspected or edited directly if needed. Budget settings are stored separately in `budget.json` so they survive between sessions independently of expense data.

A CSV snapshot can be exported at any time via menu option **8**, producing a file named `expenses_YYYY-MM-DD.csv`.

---

## AI Suggestions Logic

The insights engine is rule-based, not model-based — but it covers the practical cases that matter:

- **Budget bar** — visual progress toward the monthly limit with color thresholds (green → yellow → red)
- **Over-budget alert** — fires when monthly total exceeds the set limit
- **Category tip** — category-specific advice for the top spending category (Food, Entertainment, Shopping, Transport)
- **Daily average + projection** — extrapolates current pace to a full 30-day estimate
- **20% savings rule** — recommends a concrete savings target based on projected spending

---

## Python Concepts Used

`variables` · `data types` · `conditional statements` · `loops` · `functions` · `lists` · `dictionaries` · `string handling` · `file handling` · `exception handling`

---

## Possible Extensions

- Password protection per user session
- Matplotlib bar/pie charts for visual reports
- Multi-user support with separate data files
- Recurring expense tracking
- Date range filtering in search
