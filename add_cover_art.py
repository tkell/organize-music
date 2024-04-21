import json
import os
import shutil
import time
from collections import defaultdict
from urllib.parse import urlparse

import requests

import lib_discogs


def find_and_download_discog_cover(album_source_url, folder):
    album_url = urlparse(album_source_url)
    if album_url.hostname != "www.discogs.com":
        print(f"____ not a discogs url for {folder}: {album_source_url}")
        return
    else:
        if "master/" in album_url.path:
            print("---- A stray master release!!", album_source_url)
            return

        # path looks like /release/4301112-95-North-Let-Yourself-Go-Remixes
        release_id = album_url.path.split("/")[2].split("-")[0]
        release_api_url = f"https://api.discogs.com/releases/{release_id}"
        release_data = lib_discogs.call_discogs(release_api_url)
        if "images" not in release_data.keys():
            print(f"~~~~ no images found on discogs for {album_source_url}")
            return

        image_url = release_data["images"][0]["uri"]
        path = os.path.join(albums_dir, folder, "cover.jpg")
        if not os.path.isfile(path):
            print(f"downloading for {folder}:  {image_url}")
            headers = {
                "User-Agent": "Thor's Music Organizer",
            }
            response = requests.get(image_url, stream=True, headers=headers)
            with open(path, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            time.sleep(2)
            print("downloaded!")
        else:
            pass
            print("cover file already exists for ", folder)

    return


if __name__ == "__main__":
    print("starting add cover art")
    albums_dir = "/Users/thor/Desktop/parsed/albums/"
    folders = os.listdir(albums_dir)

    counts = defaultdict(int)
    for folder in folders:
        cover_flag = False
        tracks_file_flag = False
        dir_path = os.path.join(albums_dir, folder)
        if os.path.isdir(dir_path):
            filenames = os.listdir(dir_path)
            counts["total"] += 1

            # Do we have cover art
            for filename in filenames:
                if filename.lower() == "cover.jpg" or filename.lower() == "cover.png":
                    cover_flag = True
                    counts["cover art exists"] += 1
                    break
            if cover_flag:
                continue

            # if not, looks for N.tracks, and find it!
            tracks_file_path = os.path.join(albums_dir, folder, "info.json")
            with open(tracks_file_path) as f:
                metadata = json.load(f)
                album_source_url = metadata.get("discogs_url", "not-on-discogs")
                if album_source_url == "not-on-discogs":
                    print(f"not on discogs: {folder}")
                    counts["not on discogs or anywhere else"] += 1
                else:
                    try:
                        find_and_download_discog_cover(album_source_url, folder)
                    except TypeError as e:
                        print(e)
                        print("an error", folder)

            if not cover_flag and not tracks_file_flag:
                print("yikes!  We should have none of these!")
    print(counts)
