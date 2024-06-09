import argparse
import os
import json
import re
import datetime
import difflib

from src.organize_music.local_file_io import read_info_file, write_info_file


def normalize(name):
    return re.sub(r"[^a-zA-Z0-9]", "", name)


def to_datetime(date_string):
    # Remove 'GMT' from the string
    date_string = date_string.replace("GMT", "").strip()
    return datetime.datetime.strptime(date_string, "%d %b %Y %H:%M:%S")


def to_string(date):
    return date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    # just BC, for now
    with open("crawlers/bandcamp_purchases.json") as f:
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
    missing = 0
    for folder in folders:
        if folder.startswith("."):
            continue
        folder_path = os.path.join(albums_dir, folder)

        try:
            metadata = read_info_file(folder_path)
            if "purchase_date" in metadata:
                print(".", end="", flush=True)
                continue

            artist_and_title = folder.split("[")[0]
            normalized = normalize(artist_and_title)
            possibilities = difflib.get_close_matches(
                normalized, lookup.keys(), n=3, cutoff=0.6
            )
            if not possibilities:
                print("x", end="", flush=True)
                continue

            print(f"Potentials for {folder_path}")
            for index, p in enumerate(possibilities):
                print(f"{index}: {p}, {lookup[p]['sold_date']}")
            choice = input("Choose the correct match, or 's' to skip: ")
            if choice == "s":
                print("Skipping")
                continue

            choice = int(choice)
            best_key = possibilities[choice]
            purchase = lookup[best_key]
            sold_date = to_datetime(purchase["sold_date"])
            metadata["purchase_date"] = to_string(sold_date)
            print(f"\na match - {folder}, {sold_date}")
            write_info_file(folder_path, metadata)

        except Exception as e:
            print(f"Error processing {folder_path}: {e}")
            raise e

        count += 1
        if count >= break_after:
            break

    print(f"\nProcessed {count} albums, {missing} missing purchase dates")
