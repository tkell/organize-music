import argparse
import os
import shutil
import time
from urllib.parse import urlparse

import requests

import lib_discogs
from local_file_io import albums_dir_to_folder_paths
from local_file_io import read_info_file


## This should really be moved to lib_discogs, I think
## maybe without the guard clause for "discogs url"
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


def _ensure_cover_art(folder_path):
    album_name = folder_path.split(os.path.sep)[-1]
    cover_flag = False
    if os.path.isdir(folder_path):
        filenames = os.listdir(folder_path)

        # Do we have cover art
        for filename in filenames:
            if filename.lower() == "cover.jpg" or filename.lower() == "cover.png":
                cover_flag = True
                break
        if cover_flag:
            return

        # if not, looks for N.tracks, and find it!
        metadata = read_info_file(folder_path)
        album_source_url = metadata.get("discogs_url", "not-on-discogs")
        if album_source_url == "not-on-discogs":
            print(f"not on discogs: {album_name}")
        else:
            try:
                find_and_download_discog_cover(album_source_url, album_name)
            except TypeError as e:
                print(e)
                print("an error", folder_path)


if __name__ == "__main__":
    print("starting add cover art")
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path")
    args = parser.parse_args()

    albums_dir = args.folder_path
    folder_paths = albums_dir_to_folder_paths(albums_dir)
    for folder_path in folder_paths:
        _ensure_cover_art(folder_path)
