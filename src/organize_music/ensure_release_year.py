import os

from src.organize_music.local_file_io import read_info_file
from src.organize_music.local_file_io import write_info_file


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
