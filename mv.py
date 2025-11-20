import requests
from bs4 import BeautifulSoup

# Fetch the page
url = "https://saka46.fun/nogi/mv/"
response = requests.get(url)
response.raise_for_status()  # Ensure the request succeeded
response.encoding = response.apparent_encoding  # Handle Japanese characters correctly

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# The data is in a <table> with <thead> and <tbody>
table = soup.find("table")
if not table:
    raise ValueError("Table not found on the page")

rows = table.find_all("tr")

# List to hold the data
videos = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) < 4:
        continue  # Skip malformed rows
    
    rank = cols[0].get_text(strip=True)
    title_cell = cols[1]
    title = title_cell.find_all("a")[0].get_text(strip=True)  # Includes any extra text like affiliate icons, but mainly the title
    print(title)
    # Extract total views (in ten-thousands, e.g., "9261")
    total_views_str = cols[2].get_text(strip=True).replace(",", "")
    total_views = int(total_views_str) * 10000  # Convert to actual total views
    
    # Extract yesterday's (previous day) views (raw number, e.g., "9595")
    yesterday_views_str = cols[3].get_text(strip=True).replace(",", "")
    yesterday_views = int(yesterday_views_str)
    
    videos.append({
        "rank": rank,
        "title": title,
        "total_views": total_views,
        "yesterday_views": yesterday_views
    })

# Sort by yesterday_views descending and take top 20
top_20_yesterday = sorted(videos, key=lambda x: x["yesterday_views"], reverse=True)[:20]

# Print the result nicely
print("Top 20 Nogizaka46 MVs by views gained yesterday:")
print("-" * 80)
for i, video in enumerate(top_20_yesterday, 1):
    print(f"{i:2}. {video['title']}")
    print(f"    Yesterday views : {video['yesterday_views']:,}")
    print(f"    Total views     : {video['total_views']:,}")
    print()