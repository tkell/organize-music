import hashlib
import json
import os

if __name__ == "__main__":
    albums_dir = "/Volumes/Music/Albums"
    folders = os.listdir(albums_dir)
    print("listed directories")

    for folder in folders:
        if folder == ".DS_Store":
            continue
        folder_path = os.path.join(albums_dir, folder)

        m = hashlib.sha256()
        m.update(folder.encode("utf-8"))
        id_integer = int(m.hexdigest()[0:8], 16)
        info_dict = {"id": id_integer}
        print(folder_path, id_integer)

        info_filepath = os.path.join(folder_path, "info.json")
        with open(info_filepath, "w") as f:
            json.dump(info_dict, f)
