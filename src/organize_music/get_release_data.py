import os
import src.discogs.lib_discogs as lib_discogs
from src.organize_music.local_file_io import read_info_file


def get_discogs_release_data(folder_path):
    album_name = folder_path.split(os.path.sep)[-1]
    metadata = read_info_file(folder_path)
    album_source_url = metadata.get("discogs_url", "not-on-discogs")
    if album_source_url == "not-on-discogs" or "master/" in album_source_url:
        print(f"not on discogs, or a stray master release for: {album_name}")
        return {}

    return lib_discogs.download_release_data(album_source_url)
