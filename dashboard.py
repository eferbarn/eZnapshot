# %% dashboard.py
import os
import json
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore

# Set base directory relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Shorten wallet address


def shorten(address):
    if not address.startswith("0x") or len(address) < 10:
        return address
    return f"{address[:5]}***{address[-5:]}"


# Load Total.csv
file_path = os.path.join(base_dir, "Total.csv")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ Total.csv not found at {file_path}")

df = pd.read_csv(file_path)
df.sort_values("Holdings", ascending=False, inplace=True)

# Load Token Contracts using Tokens.json
file_path = os.path.join(base_dir, "Tokens.json")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ Total.csv not found at {file_path}")

with open(file_path, "r") as f:
    tokens_list = json.load(f)

tokens_dict = {
    token["symbol"]: token
    for token in tokens_list
    if "symbol" in token
}

# Top 10 holders
top_10 = df.head(10).copy()
top_10["Short Address"] = top_10["Address"].apply(shorten)

print("🔝 Top 10 Token Holders:\n")
print(top_10[["Short Address", "Holdings"]].to_string(index=False))

# Plot with Plotly
fig = px.bar(
    top_10,
    x="Short Address",
    y="Holdings",
    title="Top 10 Token Holders by Total Holdings",
    labels={"Short Address": "Wallet", "Holdings": "Total Holdings"},
    text="Holdings"
)
fig.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor="#f8f8f8",
    font=dict(size=14)
)

# Save HTML
# html_output = os.path.join(base_dir, "top_10_holders_chart.html")
# fig.write_html(html_output)
# print(f"\n🌐 Interactive chart saved to: {html_output}")

# Save PNG
png_output = os.path.join(base_dir, "top_10_holders_chart.png")
fig.write_image(png_output)
print(f"🖼️ PNG chart saved to: {png_output}")

# fig.show()  # Uncomment if needed

# Generate Statistics
stats = {}
token_columns = [
    col for col in df.columns if col not in ["Address", "Holdings"]]

for token in token_columns:
    token_data = df[token]
    stats[token] = {
        "total_holders": int((token_data > 0).sum()),
        "total_tokens_held": int(token_data.sum()),
        "average_tokens": float(token_data[token_data > 0].mean()) if (token_data > 0).any() else 0.0,
        "max_tokens": int(token_data.max()),
        "min_tokens": int(token_data[token_data > 0].min()) if (token_data > 0).any() else 0
    }

# Save Statistics
stats_output = os.path.join(base_dir, "Statistics.json")
with open(stats_output, "w") as f:
    json.dump(stats, f, indent=2)
print(f"📊 Statistics saved to: {stats_output}")

# Generate Markdown Table for Top 10 Holders
holders_table_header = "| Rank | Address | Total Holdings |\n"
holders_table_separator = "|------|---------|----------------|\n"
holders_table_rows = ""

for i, row in top_10.iterrows():
    rank = i + 1
    addr = f'[{row["Short Address"]}](https://explorer.zero.network/address/{row["Address"]})'
    amount = row["Holdings"]
    holders_table_rows += f"| {rank} | {addr} | {amount} |\n"

top_10_table = holders_table_header + \
    holders_table_separator + holders_table_rows

# Generate Markdown Table for Detailed Token Statistics
stats_header = "| Token | Total Holders | Total Tokens Held | Average Tokens | Max Tokens | Min Tokens |\n"
stats_separator = "|-------|----------------|--------------------|----------------|-------------|-------------|\n"
stats_rows = ""

for token, data in stats.items():
    link = f'[{token}](https://highlight.xyz/mint/zero:{tokens_dict[token]["contract"]}:1)'
    stats_rows += f"| {link} | {data['total_holders']} | {data['total_tokens_held']} | {data['average_tokens']:.2f} | {data['max_tokens']} | {data['min_tokens']} |\n"

detailed_stats_table = stats_header + stats_separator + stats_rows

# Create full README section
readme_section = f"""
# Znapshot
The automated snapshot taker using Caldera/Blockscout API and GitHub workflow 

## 📊 Token Statistics (Auto-Generated)

Here is a quick snapshot of the current token statistics and top holders.

1. Raw Tokens File: [Tokens.json](Tokens.json)
2. Raw Leaderboard File: [Total.json](Total.json)
3. Raw Statistics File: [Statistics.json](Statistics.json)

---

### 📈 Top 10 Token Holders

![Top Holders Chart](top_10_holders_chart.png)

#### 🔢 Top 10 Holders Table

{top_10_table}

---

### 📋 Detailed Statistics

{detailed_stats_table}

---

Hope you enjoy it!
Made with ❤️

[![MΞHDI ⧗](https://img.shields.io/badge/M%CE%9EHDI-Zerion-darkblue)](https://link.zerion.io/)

---
"""

# Save to README_section.md
readme_output = os.path.join(os.getcwd(), "README.md")
with open(readme_output, "w") as f:
    f.write(readme_section)

print(
    f"📝 README section with statistics and top holders saved to: {readme_output}")

# %%
