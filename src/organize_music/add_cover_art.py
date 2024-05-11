import os
from urllib.parse import urlparse


import src.discogs.lib_discogs as lib_discogs
from src.organize_music.local_file_io import read_info_file
from src.organize_music.local_file_io import download_file


def _find_and_download_discog_cover(album_source_url, folder):
    album_url = urlparse(album_source_url)
    if "master/" in album_url.path:
        print("---- A stray master release!!", album_source_url)
        return None

    # path looks like /release/4301112-95-North-Let-Yourself-Go-Remixes
    release_id = album_url.path.split("/")[2].split("-")[0]
    release_api_url = f"https://api.discogs.com/releases/{release_id}"
    release_data = lib_discogs.call_discogs(release_api_url)
    if "images" not in release_data.keys():
        print(f"~~~~ no images found on discogs for {album_source_url}")
        return
    image_url = release_data["images"][0]["uri"]
    downloaded_path = download_file(image_url, folder, "cover.jpg")

    return downloaded_path


def _cover_art_exists(folder_path):
    filenames = os.listdir(folder_path)
    for filename in filenames:
        if filename.lower() == "cover.jpg" or filename.lower() == "cover.png":
            return True
    return False


def ensure_cover_art(folder_path):
    album_name = folder_path.split(os.path.sep)[-1]
    if _cover_art_exists(folder_path):
        return

    metadata = read_info_file(folder_path)
    album_source_url = metadata.get("discogs_url", "not-on-discogs")
    if album_source_url == "not-on-discogs":
        print(f"not on discogs: {album_name}")
        return

    return _find_and_download_discog_cover(album_source_url, folder_path)
