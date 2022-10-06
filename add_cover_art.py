import os
import shutil
import sys
import time
from collections import defaultdict
from urllib.parse import urlparse

import requests

import lib_discogs
import discogs_album_search


def find_and_download_discog_cover(album_source_url):
    album_url = urlparse(album_source_url)
    key = "tracks file is at " + album_url.hostname
    if album_url.hostname != "www.discogs.com":
        print(f"____ not a discogs url, we'll get it later:  {album_source_url}")
        return
    else:
        if "master/" in album_url.path:
            print("---- A stray master release!!", album_source_url)
            return

        # path looks like /release/4301112-95-North-Let-Yourself-Go-Remixes
        release_id = album_url.path.split("/")[2].split("-")[0]
        release_api_url = f"https://api.discogs.com/releases/{release_id}"
        release_data = lib_discogs.call_discogs(release_api_url)
        ## what if we have no images?
        if "images" not in release_data.keys():
            print(f"~~~~ no images found on discogs for {album_source_url}")
            return

        image_url = release_data["images"][0]["uri"]
        path = os.path.join(albums_dir, folder, "cover.jpg")
        if not os.path.isfile(path):
            # print(f"downloading for {folder}:  {image_url}")
            response = requests.get(image_url, stream=True)
            with open(path, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            time.sleep(2)
            # print("downloaded!")
        else:
            pass
            # print("cover file already exists for ", folder)

    return


def search_discogs_for_albums(folder):
    print(folder)
    artist = folder.split(" - ")[0].strip()
    if artist == "Various Artists":
        artist = "Various"  # discogs!

    album_and_label = folder.split(" - ")[-1].strip()
    album = album_and_label.split("[")[0].strip()
    label = album_and_label.split("[")[1].strip().replace("]", "")
    discogs_url = discogs_album_search.search(artist, album, label)

    folder_path = os.path.join(albums_dir, folder)
    num_tracks = len(os.listdir(folder_path))
    tracks_filename = os.path.join(folder_path, f"{num_tracks}.tracks")
    print(f"here's our discogs url: {discogs_url}")
    with open(tracks_filename, "w") as f:
        f.write(discogs_url)


if __name__ == "__main__":
    albums_dir = "/Volumes/Music/Albums"
    folders = os.listdir(albums_dir)
    print("listed directories")

    counts = defaultdict(int)
    for folder in folders:
        # Alphabets!
        if folder[0].lower() != "e":
            continue

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
            for filename in filenames:
                if filename.endswith(".tracks"):
                    tracks_file_flag = True
                    counts["tracks file exists"] += 1
                    tracks_file_path = os.path.join(albums_dir, folder, filename)
                    with open(tracks_file_path) as f:
                        album_source_url = f.readline().strip()
                        if album_source_url == "not-on-discogs":
                            counts[
                                "tracks file is not on discogs or anywhere else"
                            ] += 1
                        else:
                            try:
                                find_and_download_discog_cover(album_source_url)
                            except TypeError:
                                print("an error", folder)

            if not cover_flag and not tracks_file_flag:
                print("yikes!  We should have none of these!")
                search_discogs_for_albums(folder)
    print(counts)
