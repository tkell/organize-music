import os

from src.organize_music.local_file_io import download_file


def _cover_art_exists(folder_path):
    filenames = os.listdir(folder_path)
    for filename in filenames:
        if filename.lower() == "cover.jpg" or filename.lower() == "cover.png":
            return True
    return False


def _validate(discogs_release_data):
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
        print(f"---- cover art exists for {album_name}")
        return
    if not _validate(discogs_release_data):
        print(f"~~~~ no images or bad data found on discogs for {album_name}")
        return
    image_url = discogs_release_data["images"][0]["uri"]
    downloaded_path = download_file(image_url, folder_path, "cover.jpg")

    return downloaded_path
