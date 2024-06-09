import requests
import json

url = "https://api.beatport.com/v4/my/downloads/"
auth_token = "MbfduKMMu71EK4VM5yc4h0DUj2jtqu"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"

headers = {
    "authority": "api.beatport.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.5",
    "authorization": f"Bearer {auth_token}",
    "origin": "https://dj.beatport.com",
    "referer": "https://dj.beatport.com/",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": user_agent,
}
params = {"per_page": 100, "page": 1}


page = 1
item_data = []
while True:
    params = {"per_page": 100, "page": page}
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    items = result["results"]

    for item in items:
        item_info = {}
        item_info["artist_name"] = item["artists"][0]["name"]
        item_info["item_title"] = item["release"]["name"]
        item_info["sold_date"] = item["purchase_date"] # 2022-03-24T18:37:46-06:00
        item_info["release_date"] = item["publish_date"] # 2001-01-01
        item_data.append(item_info)

    print(item_data[-1])
    print(f"We have {len(item_data)} items")
    print(f"Page {page} done")
    print("press G to get more items, Q to write and quit")
    user_input = input()
    if user_input.lower() == "q":
        json.dump(item_data, open("beatport_purchases.json", "w"))
        break
    else:
        page += 1
        continue
