import argparse
import json
import os

from discogs_album_search import search

if __name__ == "__main__":
    print("ensuring discogs url")
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path")
    args = parser.parse_args()

    albums_dir = args.folder_path
    folders = os.listdir(albums_dir)

    for folder in folders:
        if folder == ".DS_Store":
            continue
        folder_path = os.path.join(albums_dir, folder)
        metadata = {}
        with open(os.path.join(albums_dir, folder, "info.json"), "r") as f:
            metadata = json.load(f)
        if "discogs_url" in metadata:
            continue
        artist_and_release, label = folder.split("[")
        artist = artist_and_release.split(" - ")[0]
        release = " - ".join(artist_and_release.split(" - ")[1:])
        label = label[:-1]
        artist = artist.strip()
        # Discogs hates `Various Artists`, so we replace it
        if artist == "Various Artists":
            artist = "Various"
        release = release.strip()
        label = label.strip()
        discogs_url = search(artist, release, label)

        with open(os.path.join(albums_dir, folder, "info.json"), "r") as f:
            metadata = json.load(f)
        metadata["discogs_url"] = discogs_url
        with open(os.path.join(albums_dir, folder, "info.json"), "w") as f:
            json.dump(metadata, f)
