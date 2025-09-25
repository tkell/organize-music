import os
import sys
import json

if __name__ == "__main__":
    folder = sys.argv[1]
    info_file = "info.json"

    for filename in os.listdir(folder):
        old_file_path = os.path.join(folder, filename)
        if not os.path.isdir(old_file_path):
            continue

        new_path = os.path.join(old_file_path, info_file)
        with open(new_path) as f:
            info = json.load(f)

        print("----")
        print(filename)
        if (
            info.get("release_year")
            and info.get("purchase_date")
            and info.get("discogs_url")
            and info.get("num_tracks")
        ):
            print(".")
        else:
            print("bad info file!  bad info file!")
            break
