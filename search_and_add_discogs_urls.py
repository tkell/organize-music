import json
import os

from discogs_album_search import search

albums_dir = "/Volumes/Mimir/Music/Albums"
folders = os.listdir(albums_dir)

stop_count = 1
count = 0
for folder in folders:
    if folder[0] == ".":
        continue
    metadata = {}
    with open(os.path.join(albums_dir, folder, "info.json"), "r") as f:
        metadata = json.load(f)
    if "discogs_url" in metadata:
        continue

    artist_and_release, label = folder.split("[")
    artist, release = artist_and_release.split(" - ")
    label = label[:-1]
    artist = artist.strip()
    release = release.strip()
    label = label.strip()
    discogs_url = search(artist, release, label)

    with open(os.path.join(albums_dir, folder, "info.json"), "r") as f:
        metadata = json.load(f)
    metadata["discogs_url"] = discogs_url
    with open(os.path.join(albums_dir, folder, "info.json"), "w") as f:
        json.dump(metadata, f)

    count += 1
    if count == stop_count:
        break
