import argparse

from src.organize_music.local_file_io import albums_dir_to_folder_paths
from src.organize_music.add_info_file import add_id_to_folder
from src.organize_music.ensure_discogs_url import ensure_discogs_url
from src.organize_music.add_cover_art import ensure_cover_art

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path")
    args = parser.parse_args()
    albums_dir = args.folder_path
    folder_paths = albums_dir_to_folder_paths(albums_dir)

    print("Adding info file and IDs")
    for folder_path in folder_paths:
        add_id_to_folder(folder_path)

    print("Ensuring discogs urls")
    for folder_path in folder_paths:
        ensure_discogs_url(folder_path)

    print("Adding cover art")
    for folder_path in folder_paths:
        ensure_cover_art(folder_path)
