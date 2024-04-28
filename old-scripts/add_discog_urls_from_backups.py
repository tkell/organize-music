import json
import os

with open("folders_to_urls.json") as f:
    folders_to_urls = json.load(f)


album_path = "/Volumes/Mimir/Music/Albums"
for folder in os.listdir(album_path):
    if folder[0] == ".":
        continue
    info_filepath = os.path.join(album_path, folder, "info.json")
    with open(info_filepath) as f:
        info = json.load(f)
    if "discogs_url" in info:
        continue
    if folder in folders_to_urls:
        print(folder)
        info["discogs_url"] = folders_to_urls[folder]

        with open(info_filepath, "w") as f:
            json.dump(info, f)
