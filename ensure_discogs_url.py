import argparse
import os

from discogs_album_search import search
from local_file_io import albums_dir_to_folder_paths
from local_file_io import read_info_file
from local_file_io import write_info_file


def _ensure_discogs_url(folder_path):
    album_name = folder_path.split(os.path.sep)[-1]
    metadata = read_info_file(folder_path)
    if "discogs_url" in metadata:
        return

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
    discogs_url = search(artist, release, label)

    metadata["discogs_url"] = discogs_url
    write_info_file(folder_path, metadata)


if __name__ == "__main__":
    print("ensuring discogs url")
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path")
    args = parser.parse_args()

    albums_dir = args.folder_path
    folder_paths = albums_dir_to_folder_paths(albums_dir)
    for folder_path in folder_paths:
        result = _ensure_discogs_url(folder_path)
