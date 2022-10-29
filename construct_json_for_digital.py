import json
import os

if __name__ == "__main__":
    albums_dir = "/Volumes/Music/Albums"
    folders = os.listdir(albums_dir)
    print("listed directories ...")

    all_tracks_json = []
    for folder in folders:
        if folder == ".DS_Store":
            continue
        folder_path = os.path.join(albums_dir, folder)
        print(folder_path)
        info_filepath = os.path.join(folder_path, "info.json")
        with open(info_filepath, "r") as f:
            info_dict = json.load(f)
            id_string = info_dict["id"]

        artist = folder.split(" - ")[0].strip()
        title = folder.split(" - ")[1].split(" [")[0].strip()
        title = title.replace(" : ", " / ")
        label = folder.split(" [")[1][0:-1].strip()

        folder_files = os.listdir(folder_path)

        tracks = []
        formats = ["flac", "mp3", "m4a", "aac", "wav"]
        for folder_file in folder_files:
            if folder_file.split(".")[-1] in formats:
                tracks.append(folder_file)

        formatted_tracks = []
        for track in tracks:
            position = track.split(" - ")[0]
            track_title = track.split(" - ")[1].split(".")[0]
            tracks_dict = {"position": position, "title": track_title}
            formatted_tracks.append(tracks_dict)

        json_dict = {
            "id": id_string,
            "title": title,
            "artist": artist,
            "label": label,
            "tracks": formatted_tracks,
        }
        all_tracks_json.append(json_dict)

    with open("digital.json", "w") as f:
        json.dump(all_tracks_json, f)
