import requests
import json


def call_discogs(url):
    headers = {
        "user-agent": "DiscogsOrganize +http://tide-pool.ca",
        "Authorization": f"Discogs token={discogs_token}",
    }
    r = requests.get(url, headers=headers)
    print("calling: ", url)
    return r.json()


# import the token
with open("discogs-token.txt") as f:
    discogs_token = f.readline().strip()

# call collection by folder
url = "https://api.discogs.com/users/tkell/collection/folders"
# /users/{username}/collection/folders/{folder_id}/releases
collection = call_discogs(url)
for folder in collection["folders"]:
    if folder["id"] == 0:
        url = folder["resource_url"] + "/releases"
        print(call_discogs(url))
