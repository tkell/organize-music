import json
from bs4 import BeautifulSoup

filenames = [
    "bleep-data/bleep-page-1.html",
    "bleep-data/bleep-page-2.html",
    "bleep-data/bleep-page-3.html",
    "bleep-data/bleep-page-4.html",
]


item_data = []
for filename in filenames:
    with open(filename, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

        orders = soup.find_all("li", class_="orders-list-item")
        for order in orders:
            # strptime(order_date, "%B %d, %Y").date()
            order_date = order.find("dd", string=True).text.strip()
            items = order.find_all("li", class_="order-item-status-new")
            for item in items:
                item_info = {}
                artist = item.find("a", class_="artist").text.strip()
                release_title = item.find("a", class_="release-title").text.strip()
                item_info["artist_name"] = artist
                item_info["item_title"] = release_title
                item_info["sold_date"] = order_date
                print(item_info)
                item_data.append(item_info)

with open("bleep_purchases.json", "w") as f:
    json.dump(item_data, f)
