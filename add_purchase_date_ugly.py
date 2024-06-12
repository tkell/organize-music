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
    # Remove 'GMT' from the string for BC stuff
    date_string = date_string.replace("GMT", "").strip()

    date_formats = ["%d %b %Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%B %d, %Y"]
    for format in date_formats:
        try:
            return datetime.datetime.strptime(date_string, format)
        except ValueError:
            pass
    print(f"Could not parse date: {date_string}")


def to_string(date):
    return date.strftime("%Y-%m-%d")


def make_lookup_dict(filename):
    with open(filename) as f:
        purchase_data = json.load(f)
    lookup = {}
    for purchase in purchase_data:
        artist_name = normalize(purchase["artist_name"])
        item_title = normalize(purchase["item_title"])
        search_string = f"{artist_name}{item_title}"
        lookup[search_string] = purchase

    return lookup


def get_single_possibilities(normalized, lookup):
    return difflib.get_close_matches(normalized, lookup.keys(), n=3, cutoff=0.6)


def get_all_possibilities(normalized, lookups):
    results = []
    for source, lookup in lookups.items():
        p = get_single_possibilities(normalized, lookup)
        if p:
            results.append((source, p))

    return results


if __name__ == "__main__":
    bc_lookup = make_lookup_dict("crawlers/bandcamp_purchases.json")
    bp_lookup = make_lookup_dict("crawlers/beatport_purchases.json")
    bl_lookup = make_lookup_dict("crawlers/bleep_purchases.json")
    lookups = {"bandcamp": bc_lookup, "beatport": bp_lookup, "bleep": bl_lookup}

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("albums_dir")
    arg_parser.add_argument("break_after")
    arg_parser.add_argument("start_from")
    args = arg_parser.parse_args()
    albums_dir = args.albums_dir
    break_after = int(args.break_after)
    start_from = args.start_from
    folders = os.listdir(albums_dir)

    count = 0
    missing = 0
    for folder in folders:
        count += 1
        if folder.startswith(".") or folder[0].lower() < start_from[0]:
            continue
        folder_path = os.path.join(albums_dir, folder)

        try:
            metadata = read_info_file(folder_path)
            if "purchase_date" in metadata:
                print(".", end="", flush=True)
                continue
            else:
                missing += 1

        except Exception as e:
            print(f"Error processing {folder_path}: {e}")
            raise e

        if count >= break_after:
            break

    print(f"\nProcessed {count} albums, {missing} missing purchase dates")
