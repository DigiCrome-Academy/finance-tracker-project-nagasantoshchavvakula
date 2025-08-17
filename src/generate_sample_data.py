#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

# 1) transactions.csv (1000+ rows)
"""
Generate sample transaction data for a personal finance application.
Each transaction has:
- transaction_id: unique identifier
- user_id: random user ID (1-200)
"""
n = 1200
start = datetime(2023,1,1)
categories = ["groceries","rent","utilities","entertainment","transport","health","education","investment"]
merchants = ["Amazon", "Walmart", "Starbucks", "Uber", "Shell", "WholeFoods", "Spotify", "LocalGym"]
currencies = ["USD"]

rows = []
for i in range(n):
    date = start + timedelta(days=random.randint(0, 730))
    amount = round(np.random.exponential(scale=50.0),2)
    # add some larger transactions
    if random.random() < 0.02:
        amount *= random.randint(3,10)
    # add occasional refunds/negative
    if random.random() < 0.01:
        amount *= -1
    rows.append({
        "transaction_id": f"tx_{i+1:06d}",
        "user_id": random.randint(1,200),
        "date": date.strftime("%Y-%m-%d"),
        "amount": amount,
        "category": random.choice(categories),
        "merchant": random.choice(merchants),
        "currency": random.choice(currencies)
    })
df_tx = pd.DataFrame(rows)
df_tx.to_csv("data/raw/transactions.csv", index=False)
print("Wrote data/raw/transactions.csv", df_tx.shape)

# 2) market_data.csv -- simulate daily close prices for 4 symbols
symbols = ["AAPL","GOOG","TSLA","SPY"]
dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
rows = []
for sym in symbols:
    price = 100 + random.random()*50
    for d in dates:
        # simple random walk with drift
        price = price * (1 + np.random.normal(loc=0.0002, scale=0.02))
        rows.append({"date": d.strftime("%Y-%m-%d"), "symbol": sym, "close": round(max(price,0.1),2)})
df_market = pd.DataFrame(rows)
df_market.to_csv("data/raw/market_data.csv", index=False)
print("Wrote data/raw/market_data.csv", df_market.shape)

# 3) budget_data.json
budget = {
    "monthly_budgets": {
        "groceries": 500,
        "rent": 1500,
        "utilities": 200,
        "entertainment": 150,
        "transport": 100,
        "health": 100,
        "education": 200,
        "investment": 600
    },
    "currency": "USD",
    "notes": "Sample monthly budgets used to compute adherence"
}
with open("data/raw/budget_data.json", "w") as f:
    json.dump(budget, f, indent=2)
print("Wrote data/raw/budget_data.json")