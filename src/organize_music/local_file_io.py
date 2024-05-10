import os
import json
import requests
import shutil
import time


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


def download_file(image_url, folder_path, filename):
    path = os.path.join(folder_path, filename)
    print(f"downloading for {folder_path}:  {image_url}")
    headers = {"User-Agent": "Thor's Music Organizer"}
    response = requests.get(image_url, stream=True, headers=headers)
    with open(path, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    time.sleep(2)
    print("downloaded!")
    return path
