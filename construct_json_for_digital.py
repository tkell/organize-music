import json
import os
import sys


def update_from_existing_json_file(existing_json_file):
    with open(existing_json_file) as f:
        all_tracks_json = json.load(f)
        for existing in all_tracks_json:
            image_path = existing["image_path"]
            folder_path = os.path.dirname(image_path)
            existing_folders.add(folder_path)
    return all_tracks_json, existing_folders


def get_album_data(folder_path):
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

        return artist, title, label, release_id
    except Exception as e:
        print(folder)
        raise e


def get_tracks(folder_files):
    tracks = []
    formats = ["flac", "mp3", "m4a", "aac", "wav"]
    for folder_file in folder_files:
        if folder_file.split(".")[-1] in formats:
            tracks.append(folder_file)

    return tracks


def get_formatted_tracks(tracks):
    formatted_tracks = []
    for track in tracks:
        position = track.split(" - ")[0]
        track_title = " - ".join(track.split(" - ")[1:])
        track_title = ".".join(track_title.split(".")[0:-1])
        track_filepath = os.path.join(folder, track)

        tracks_dict = {
            "position": position,
            "title": track_title,
            "filepath": track_filepath,
        }
        formatted_tracks.append(tracks_dict)

    return formatted_tracks


def get_cover(folder_files):
    valid_cover_files = ["cover.jpg", "cover.png"]
    for folder_file in folder_files:
        if folder_file in valid_cover_files:
            cover_file_path = os.path.join(folder_path, folder_file)

    if not cover_file_path:
        print(f"panic!  no cover for {folder_path}")
        raise RuntimeError

    return cover_file_path


if __name__ == "__main__":
    print("starting JSON file construction for digital")
    albums_dir = sys.argv[1]

    all_tracks_json = []
    existing_folders = set()
    if len(sys.argv) == 3:
        all_tracks_json, existing_folders = update_from_existing_json_file(sys.argv[2])

    folders = os.listdir(albums_dir)
    for folder in folders:
        if folder == ".DS_Store":
            continue
        folder_path = os.path.join(albums_dir, folder)
        if folder_path in existing_folders:
            continue

        artist, title, label, release_id = get_album_data(folder_path)
        tracks = get_tracks(folder_path)

        folder_files = os.listdir(folder_path)
        tracks = get_tracks(folder_files)
        formatted_tracks = get_formatted_tracks(tracks)
        cover_file_path = get_cover(folder_files)

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
