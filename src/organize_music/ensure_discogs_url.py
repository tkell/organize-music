import os

from src.discogs.discogs_album_search import search_for_albums
from src.organize_music.local_file_io import read_info_file
from src.organize_music.local_file_io import write_info_file


def get_album_details(folder_path):
    album_name = os.path.basename(folder_path)
    artist_and_release, label = album_name.split("[")
    artist = artist_and_release.split(" - ")[0]
    release = " - ".join(artist_and_release.split(" - ")[1:])
    label = label[:-1]
    artist = artist.strip()
    # Discogs hates `Various Artists`, so we replace it
    if artist == "Various Artists":
        artist = "Various"
    release = release.strip()
    label = label.strip()
    return artist, release, label


def ensure_discogs_url(folder_path):
    metadata = read_info_file(folder_path)
    if "discogs_url" in metadata:
        return None

    artist, release, label = get_album_details(folder_path)
    discogs_url = search_for_albums(artist, release, label)
    metadata["discogs_url"] = discogs_url
    written = write_info_file(folder_path, metadata)
    return written
