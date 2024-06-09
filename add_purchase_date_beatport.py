import argparse
import os
import json
import re
import datetime

from src.organize_music.local_file_io import read_info_file, write_info_file


def normalize(name):
    return re.sub(r"[^a-zA-Z0-9]", "", name)


def to_datetime(date_string):
    # Remove 'GMT' from the string
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")


def to_string(date):
    return date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    with open("crawlers/beatport_purchases.json") as f:
        purchase_data = json.load(f)

    lookup = {}
    for purchase in purchase_data:
        artist_name = normalize(purchase["artist_name"])
        item_title = normalize(purchase["item_title"])
        search_string = f"{artist_name}{item_title}"
        lookup[search_string] = purchase

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("albums_dir")
    arg_parser.add_argument("break_after")
    args = arg_parser.parse_args()
    albums_dir = args.albums_dir
    break_after = int(args.break_after)
    folders = os.listdir(albums_dir)

    count = 0
    for folder in folders:
        if folder.startswith("."):
            continue
        folder_path = os.path.join(albums_dir, folder)

        try:
            metadata = read_info_file(folder_path)
            if "purchase_date" in metadata:
                print(".", end="")
                continue

            artist_and_title = folder.split("[")[0]
            normalized = normalize(artist_and_title)
            if normalized in lookup:
                purchase = lookup[normalized]
                sold_date = to_datetime(purchase["sold_date"])
                metadata["purchase_date"] = to_string(sold_date)
                print(f"\na match - {folder}, {artist_and_title}, {sold_date}")
                write_info_file(folder_path, metadata)
            else:
                print("x", end="")

        except Exception as e:
            print(f"Error processing {folder_path}: {e}")
            raise e

        count += 1
        if count >= break_after:
            break
