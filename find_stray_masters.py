import argparse
import os
import json
from collections import defaultdict
from src.organize_music.local_file_io import read_info_file


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("albums_dir")
    arg_parser.add_argument("break_after")
    args = arg_parser.parse_args()
    albums_dir = args.albums_dir
    break_after = int(args.break_after)
    folders = os.listdir(albums_dir)

    count = 0
    results = defaultdict(list)
    for folder in folders:
        if folder.startswith("."):
            continue
        folder_path = os.path.join(albums_dir, folder)
        metadata = read_info_file(folder_path)
        print(".", end="", flush=True)
        if "discogs_url" in metadata:
            release_url = metadata["discogs_url"]

            if "master/" in release_url:
                results["master"].append(folder_path)
            elif "discogs.com" in release_url:
                continue
            elif "not-on-discogs" == release_url:
                results["not-on-discogs"].append(folder_path)
            elif "bandcamp" in release_url:
                results["bandcamp"].append(folder_path)
            else:
                results["other"].append(folder_path)
        else:
            results["missing"].append(folder_path)
        count += 1
        if count >= break_after:
            break

    with open("strays.json", "w") as f:
        json.dump(results, f)
