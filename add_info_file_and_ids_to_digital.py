import argparse
import hashlib
import os

from local_file_io import albums_dir_to_folder_paths
from local_file_io import read_info_file
from local_file_io import write_info_file


def _add_id_to_folder(folder_path):
    album_name = folder_path.split(os.path.sep)[-1]

    m = hashlib.sha256()
    m.update(album_name.encode("utf-8"))
    id_integer = int(m.hexdigest()[0:8], 16)

    print(folder_path, id_integer)
    metadata = read_info_file(folder_path)
    metadata["id"] = id_integer
    write_info_file(folder_path, metadata)


if __name__ == "__main__":
    print("starting info_file adder")
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path")
    args = parser.parse_args()

    albums_dir = args.folder_path
    folder_paths = albums_dir_to_folder_paths(albums_dir)
    for folder_path in folder_paths:
        _add_id_to_folder(folder_path)
