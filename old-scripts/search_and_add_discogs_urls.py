import json
import os
import sys

from discogs_album_search import search


if __name__ == "__main__":
    start_letter = sys.argv[1]
    albums_dir = "/Volumes/Mimir/Music/Albums"
    folders = os.listdir(albums_dir)

    total = 0
    for folder in folders:
        if folder[0] == "." or folder[0].lower() < start_letter.lower():
            continue
        print(".", end="", flush=True)
        metadata = {}
        with open(os.path.join(albums_dir, folder, "info.json"), "r") as f:
            metadata = json.load(f)
        if "discogs_url" in metadata:
            continue
        else:
            total += 1

        try:
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
        except ValueError as e:
            print(f"Error with {folder}")
            raise e

    print(f"Found {total} albums without Discogs URLs, out of like 3000")
