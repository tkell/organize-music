import argparse
import json
import os
import re

from src.discogs.lib_discogs import call_api
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
        try:
            metadata = read_info_file(folder_path)
        except Exception as e:
            print(f"Error reading metadata for {folder_path}: {e}")
            continue
        if "release_year" in metadata:
            continue
        discogs_url = metadata.get("discogs_url")
        # Ignore non-discogs for now
        if "discogs.com" not in discogs_url:
            missing += 1
            continue

        discogs_id = discogs_url.split("/")[-1].split("-")[0]
        discogs_api_uri = f"https://api.discogs.com/releases/{discogs_id}"
        release_data = call_api(discogs_api_uri)
        year = release_data.get("year", None)
        if not year:
            year_string = release_data.get("released", "")
            res = re.search(r"\d\d\d\d", year_string)
            if res:
                year = res.group(0)

        if year:
            print(f"Would be setting release year for {folder_path} to {year}")
            added += 1
            metadata = read_info_file(folder_path)
            metadata["release_year"] = year
            write_info_file(folder_path, metadata)
        else:
            print(f"Could not find release year for {folder_path} from Discogs")
            missing += 1
