import os
import json


def albums_dir_to_folder_paths(albums_dir):
    folders = os.listdir(albums_dir)
    folder_paths = []
    for folder in folders:
        if folder == ".DS_Store":
            continue
        folder_paths.append(os.path.join(albums_dir, folder))

    return folder_paths


def read_info_file(folder_path):
    info_filepath = os.path.join(folder_path, "info.json")
    if os.path.exists(info_filepath):
        with open(info_filepath, "r") as f:
            metadata = json.load(f)
        return metadata
    else:
        return {}


def write_info_file(folder_path, metadata):
    info_filepath = os.path.join(folder_path, "info.json")
    with open(info_filepath, "w") as f:
        json.dump(metadata, f)
