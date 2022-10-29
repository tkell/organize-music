import hashlib
import json
import os

if __name__ == "__main__":
    albums_dir = "/Volumes/Music/Albums"
    folders = os.listdir(albums_dir)
    print("listed directories")

    # a bonus offset of 3 for windage
    current_id = len(folders) + 3
    for folder in folders:
        if folder == ".DS_Store":
            continue

        folder_path = os.path.join(albums_dir, folder)
        info_dict = {"id": current_id}
        current_id += 1

        info_filepath = os.path.join(folder_path, "info.json")
        with open(info_filepath, "w") as f:
            json.dump(info_dict, f)
