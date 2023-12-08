import json
import os

if __name__ == "__main__":
    print("stating JSON file construction for digital")
    albums_dir = "/Volumes/Music/Albums"
    folders = os.listdir(albums_dir)

    all_tracks_json = []
    for folder in folders:
        if folder == ".DS_Store":
            continue
        folder_path = os.path.join(albums_dir, folder)
        info_filepath = os.path.join(folder_path, "info.json")
        with open(info_filepath, "r") as f:
            info_dict = json.load(f)
            release_id = int(info_dict["id"])

        try:
            print(folder)
            artist = folder.split(" - ")[0].strip()
            title = folder.split(" - ")[1].split(" [")[0].strip()
            title = title.replace(" : ", " / ")
            label = folder.split(" [")[1][0:-1].strip()
        except Exception as e:
            print(folder)
            raise e

        folder_files = os.listdir(folder_path)

        tracks = []
        formats = ["flac", "mp3", "m4a", "aac", "wav"]
        for folder_file in folder_files:
            if folder_file.split(".")[-1] in formats:
                tracks.append(folder_file)

        formatted_tracks = []
        for track in tracks:
            position = track.split(" - ")[0]

            track_title = " - ".join(track.split(" - ")[1:])
            track_title = ".".join(track_title.split(".")[0:-1])
            track_filepath = os.path.join(folder_path, track)

            tracks_dict = {
                "position": position,
                "title": track_title,
                "filepath": track_filepath,
            }
            formatted_tracks.append(tracks_dict)

        valid_cover_files = ["cover.jpg", "cover.png"]
        for folder_file in folder_files:
            if folder_file in valid_cover_files:
                cover_file_path = os.path.join(folder_path, folder_file)

        if not cover_file_path:
            print(f"panic!  no cover for {folder_path}")
            raise RuntimeError

        json_dict = {
            "id": release_id,
            "title": title,
            "artist": artist,
            "label": label,
            "tracks": formatted_tracks,
            "image_path": cover_file_path,
        }
        all_tracks_json.append(json_dict)

    with open("digital.json", "w") as f:
        json.dump(all_tracks_json, f)
