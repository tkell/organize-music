import hashlib
import os

from src.organize_music.local_file_io import read_info_file
from src.organize_music.local_file_io import write_info_file


def _get_id_from_folder(folder_path):
    album_name = folder_path.split(os.path.sep)[-1]
    m = hashlib.sha256()
    m.update(album_name.encode("utf-8"))
    return int(m.hexdigest()[0:8], 16)


def add_id_to_folder(folder_path, today_string):
    id_integer = _get_id_from_folder(folder_path)
    metadata = read_info_file(folder_path)
    metadata["id"] = id_integer
    metadata["purchase_date"] = today_string
    write_info_file(folder_path, metadata)
