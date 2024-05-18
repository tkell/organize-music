import argparse
import os
import re

import requests
from lxml import html

from src.discogs.lib_discogs import call_api
from src.organize_music.local_file_io import read_info_file, write_info_file


def get_release_year(discogs_url):
    discogs_id = discogs_url.split("/")[-1].split("-")[0]
    discogs_api_uri = f"https://api.discogs.com/releases/{discogs_id}"
    release_data = call_api(discogs_api_uri)
    year = release_data.get("year", None)
    if not year:
        year_string = release_data.get("released", "")
        res = re.search(r"\d\d\d\d", year_string)
        if res:
            year = res.group(0)
    return year


def get_release_year_from_bandcamp(bandcamp_url):
    r = requests.get(bandcamp_url)
    tree = html.fromstring(r.content)
    selector = ".tralbumData.tralbum-credits"
    release_date_div = tree.cssselect(selector)
    if not release_date_div:
        print(f"Could not find release div on Bandcamp for {bandcamp_url}")
        return None
    raw_release_date = release_date_div[0].text_content()
    year = re.search(r"\d\d\d\d", raw_release_date).group(0)
    return year


if __name__ == "__main__":
    print("getting release years")
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path")
    args = parser.parse_args()

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
        year = None
        if "discogs.com" in discogs_url:
            continue
            year = get_release_year(discogs_url)
        elif "bandcamp.com" in discogs_url:
            continue
            year = get_release_year_from_bandcamp(discogs_url)
        else:
            print(f"got some Real Jazz for:  {folder_path}, {discogs_url}")
            print("Enter release year:")
            year = input()

        if year:
            print(f"Would be setting release year for {folder_path} to {year}")
            do_it = input("Do it? (y/n)")
            if do_it == "y":
                metadata = read_info_file(folder_path)
                metadata["release_year"] = int(year)
                write_info_file(folder_path, metadata)
        else:
            print(f"Could not find release year for {folder_path}")
