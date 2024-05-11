import argparse
import json
import os

from src.discogs.lib_discogs import call_discogs
from src.organize_music.local_file_io import read_info_file, write_info_file

if __name__ == "__main__":
    print("getting release years")
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path")
    args = parser.parse_args()
    missing = 0
    added = 0

    albums_dir = args.folder_path
    folders = os.listdir(albums_dir)

    for folder in folders:
        if folder == ".DS_Store" or folder.startswith("."):
            continue
        folder_path = os.path.join(albums_dir, folder)
        metadata = {}
        with open(os.path.join(albums_dir, folder, "info.json"), "r") as f:
            metadata = json.load(f)
        if "release_year" in metadata:
            continue

        discogs_url = metadata.get("discogs_url")
        # Ignore non-discogs for now
        if "discogs.com" not in discogs_url:
            missing += 1
            continue
        discogs_id = discogs_url.split("/")[-1].split("-")[0]
        discogs_api_uri = f"https://api.discogs.com/releases/{discogs_id}"
        release_data = call_discogs(discogs_api_uri)
        year = release_data.get("year", None)
        if year:
            print(f"Would be setting release year for {folder_path} to {year}")
            added += 1

            continue  ## toooo scared to run this still!

            metadata = read_info_file(folder_path)
            metadata["release_year"] = year
            write_info_file(folder_path, metadata)

        print(missing, added)
