import argparse
import json
import os

from lib_discogs import call_discogs

if __name__ == "__main__":
    print("getting release years")
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
        if "release_date" in metadata:
            continue

        discogs_url = metadata.get("discogs_url")
        # Ignore non-discogs for now
        if "discogs.com" not in discogs_url:
            continue
        discogs_id = discogs_url.split("/")[-1].split("-")[0]
        discogs_api_uri = f"https://api.discogs.com/releases/{discogs_id}"
        release_data = call_discogs(discogs_api_uri)
        year = release_data.get("year", "no-year-found")

        # with open(os.path.join(albums_dir, folder, "info.json"), "r") as f:
        #     metadata = json.load(f)
        # metadata["release_year"] = discogs_url
        # with open(os.path.join(albums_dir, folder, "info.json"), "w") as f:
        #     json.dump(metadata, f)
