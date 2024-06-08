import requests
import json

url = "https://bandcamp.com/api/orderhistory/1/get_items"

# These will need to be updated if I run this again!
# I probably have a few dupes in the json, but nbd!
client_id = "E30C4D3D88946E0A2636EF7FCC14A3DA083AB49F55CAED609DEB4D8066DD4223"
identity = "7%09mCJyxtQwGYeN1%2BYOXOUiqwgPEoLSJ54wzYlTp9cUyfw%3D%09%7B%22id%22%3A238517382%2C%22ex%22%3A0%7D"
session = "1%09t%3A1717805928%09r%3A%5B%22248611623c824649c0x1717805928%22%2C%22285708693l2a3676392455x1717799685%22%2C%22nilZ0c0x1717719075%22%5D%09bp%3A1%09c%3A1"
cookie_string = f"client_id={client_id}; identity={identity}; js_logged_in=1; download_encoding=401; session={session}"
user_agent_string = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "cookie": cookie_string,
    "dnt": "1",
    "origin": "https://bandcamp.com",
    "priority": "u=1, i",
    "referer": "https://bandcamp.com/thorkell/purchases?from=menubar",
    "sec-ch-ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": user_agent_string,
    "x-requested-with": "XMLHttpRequest",
}

data = {
    "username": "thorkell",
    "last_token": "1705421410:274496443",
    "platform": "mac",
    "crumb": "|api/orderhistory/1/get_items|1717807739|3mwyJJVEXaINGnbG9AcWvg9ic1M=",
}

last_token = "1716742253:290677104"
item_data = []

while True:
    data["last_token"] = last_token
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    last_token = result["last_token"]

    for item in result["items"]:
        item_info = {}
        item_info["sold_date"] = item["sold_date"]
        item_info["artist_name"] = item["artist_name"]
        item_info["item_title"] = item["item_title"]
        item_info["item_url"] = item["item_url"]
        item_data.append(item_info)

    print(item_data[-1])
    print(f"We have {len(item_data)} items")
    print("Last token is", last_token)
    print("press G to get more items, Q to quit")
    user_input = input()
    if user_input.lower() == "q":
        json.dump(item_data, open("bandcamp_purchases.json", "w"))
    else:
        continue
