import os
from urllib.parse import urlparse

import src.discogs.lib_discogs as lib_discogs
from src.organize_music.local_file_io import read_info_file
from src.organize_music.local_file_io import write_info_file
from src.organize_music.local_file_io import download_file


def ensure_release_year(folder_path, discogs_release_data):
    album_name = folder_path.split(os.path.sep)[-1]
    if discogs_release_data is None or "year" not in discogs_release_data.keys():
        print(f"no discogs data or discogs year for {album_name}")
        print(f"enter the year manually for {album_name}:")
        raw_year = input()
        release_year = int(raw_year.strip())
    else:
        release_year = discogs_release_data["year"]

    metadata = read_info_file(folder_path)
    metadata["release_year"] = release_year
    write_info_file(folder_path, metadata)


def get_discogs_data(folder_path):
    album_name = folder_path.split(os.path.sep)[-1]
    if _cover_art_exists(folder_path):
        return

    metadata = read_info_file(folder_path)
    album_source_url = metadata.get("discogs_url", "not-on-discogs")
    if album_source_url == "not-on-discogs":
        print(f"not on discogs: {album_name}")
        return None

    return download_discogs_release_data(album_source_url)


## This probably goes into lib_discogs
def download_discogs_release_data(folder_path, album_source_url):
    album_url = urlparse(album_source_url)
    if "master/" in album_url.path:
        print("---- A stray master release!!", album_source_url)
        return {}
    # path looks like /release/4301112-95-North-Let-Yourself-Go-Remixes
    release_id = album_url.path.split("/")[2].split("-")[0]
    release_api_url = f"https://api.discogs.com/releases/{release_id}"
    release_data = lib_discogs.call_discogs(release_api_url)

    return release_data


def _cover_art_exists(folder_path):
    filenames = os.listdir(folder_path)
    for filename in filenames:
        if filename.lower() == "cover.jpg" or filename.lower() == "cover.png":
            return True
    return False


def _validate_discogs_data(discogs_release_data):
    if discogs_release_data is None or "images" not in discogs_release_data.keys():
        return False
    if len(discogs_release_data["images"]) == 0:
        return False
    if "uri" not in discogs_release_data["images"][0].keys():
        return False
    return True


def ensure_cover_art(folder_path, discogs_release_data):
    album_name = folder_path.split(os.path.sep)[-1]
    if _cover_art_exists(folder_path):
        return
    if not _validate_discogs_data(discogs_release_data):
        print(f"~~~~ no images or bad data found on discogs for {album_name}")
        return
    image_url = discogs_release_data["images"][0]["uri"]
    downloaded_path = download_file(image_url, folder_path, "cover.jpg")

    return downloaded_path
