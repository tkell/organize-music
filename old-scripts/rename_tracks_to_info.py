import json
import os

albums_dir = "/Volumes/Mimir/Music/Albums"
folders = os.listdir(albums_dir)

stop_count = 3000
count = 0
for folder in folders:
    break ## don't run this again, it lost the discogs_url from the tracks files, sigh
    if folder[0] != ".":
        print(folder)
        album_dir = os.path.join(albums_dir, folder)
        album_files = os.listdir(album_dir)

        to_remove = None
        num_tracks = None
        for filename in album_files:
            if filename.endswith(".tracks"):
                to_remove = filename
                num_tracks = filename.split(".")[0]
        if not num_tracks:
            continue

        info_filepath = os.path.join(album_dir, "info.json")
        with open(info_filepath, "r") as f:
            json_data = json.load(f)
        json_data["num_tracks"] = int(num_tracks)
        with open(info_filepath, "w") as f:
            json.dump(json_data, f)
        stop_flag = True
        os.remove(os.path.join(album_dir, to_remove))
        count += 1
    if count >= stop_count:
        print("done the dry run!")
        break
