# %% main.py
import os
import json
import requests
import csv
import time
from datetime import datetime, timezone
from collections import defaultdict
import pandas as pd  # type: ignore
import calendar
import math

# Setup paths
base_dir = os.path.dirname(os.path.abspath(__file__))
tokens_path = os.path.join(base_dir, "Tokens.json")
index_file = os.path.join(base_dir, "index.json")
total_json_path = os.path.join(base_dir, "Total.json")
pagination_dir = os.path.join(base_dir, "Pagination")

# Load Tokens.json
if not os.path.exists(tokens_path):
    raise FileNotFoundError(f"❌ Tokens.json not found at {tokens_path}")
with open(tokens_path, "r") as f:
    tokens = json.load(f)

# Generate ISO-8601 timestamp in UTC
now = datetime.now(timezone.utc)
iso_timestamp = now.strftime("%Y%m%dT%H%M%SZ")
month_folder = f"{calendar.month_abbr[now.month]}{now.year}"
day_folder = f"{now.day:02d}"
snapshot_dir = os.path.join(
    base_dir, "historical_data", month_folder, day_folder)
os.makedirs(snapshot_dir, exist_ok=True)

# Aggregated holdings
aggregated = defaultdict(lambda: defaultdict(int))

# Make sure index.json exists or is initialized
if os.path.exists(index_file):
    with open(index_file, "r") as f:
        index_data = json.load(f)
else:
    index_data = []

# Process each token
for token in tokens:
    name = token.get("name", "")
    symbol = token.get("symbol", "")
    contract = token.get("contract", "")

    print(f"\n🔍 Processing: {symbol} ({contract})")

    base_url = f"https://zero-network.calderaexplorer.xyz/api/v2/tokens/{contract}/instances/1/holders"
    all_data = []
    params = None
    page = 1

    while True:
        print(f"📦 Page {page} for {symbol}")
        try:
            res = requests.get(base_url, params=params)
            res.raise_for_status()
            result = res.json()
        except Exception as e:
            print(f"❌ Error fetching page {page} for {symbol}: {e}")
            break

        items = result.get("items", [])
        for entry in items:
            address = entry["address"]["hash"]
            value = int(entry.get("value", 0))
            all_data.append({"address": address, "holding": value})
            aggregated[address][symbol] += value
            aggregated[address]["Holdings"] += value

        print(f"✅ Page {page} done. Total collected so far: {len(all_data)}")

        if result.get("next_page_params"):
            params = result["next_page_params"]
            page += 1
            time.sleep(0.5)
        else:
            break

    # Save snapshot files
    csv_path = os.path.join(snapshot_dir, f"{symbol}_{iso_timestamp}.csv")
    json_path = os.path.join(snapshot_dir, f"{symbol}_{iso_timestamp}.json")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["address", "holding"])
        writer.writeheader()
        writer.writerows(all_data)

    with open(json_path, "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"✅ Saved snapshot for {symbol}")

    # Update index.json immediately
    index_data.append({
        "symbol": symbol,
        "timestamp": iso_timestamp,
        "type": "csv",
        "path": os.path.relpath(csv_path, base_dir).replace("\\", "/")
    })
    index_data.append({
        "symbol": symbol,
        "timestamp": iso_timestamp,
        "type": "json",
        "path": os.path.relpath(json_path, base_dir).replace("\\", "/")
    })

    with open(index_file, "w") as f:
        json.dump(index_data, f, indent=2)

    print(f"📘 index.json updated after snapshot for {symbol}")

# Total holders summary
print("\n📊 Generating Total.csv and Total.json")
rows = []
for address, holdings in aggregated.items():
    row = {"Address": address, "Holdings": holdings["Holdings"]}
    for token in tokens:
        row[token["symbol"]] = holdings.get(token["symbol"], 0)
    rows.append(row)

df = pd.DataFrame(rows)
df.sort_values("Holdings", ascending=False, inplace=True)
df.to_csv(os.path.join(base_dir, "Total.csv"), index=False)
df.to_json(total_json_path, orient="records", indent=2)

print(f"\n✅ Aggregated {len(rows)} addresses. All done.")

# Generate Pagination files
print("\n📄 Creating paginated Total JSON files")
os.makedirs(pagination_dir, exist_ok=True)

with open(total_json_path, "r") as f:
    total_data = json.load(f)

page_size = 100
total_items = len(total_data)
total_pages = math.ceil(total_items / page_size)

# Build metadata for 0.json
pagination_index = {
    "total_items": total_items,
    "total_pages": total_pages,
    "page_size": page_size,
    "description": "Paginated snapshot of Total.json with 100 items per page",
    "pages": [f"{i + 1}.json" for i in range(total_pages)]
}

# Save 0.json
with open(os.path.join(pagination_dir, "0.json"), "w") as f:
    json.dump(pagination_index, f, indent=2)
print("✅ Saved pagination metadata to 0.json")

# Save each page
for page in range(total_pages):
    start = page * page_size
    end = start + page_size
    page_data = total_data[start:end]

    file_name = f"{page + 1}.json"
    file_path = os.path.join(pagination_dir, file_name)

    with open(file_path, "w") as out_file:
        json.dump(page_data, out_file, indent=2)

print(f"✅ Pagination complete: {total_pages} pages saved in Pagination/")
