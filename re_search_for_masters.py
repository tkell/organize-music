import json


from src.organize_music.local_file_io import read_info_file, write_info_file
from src.discogs.discogs_album_search import search

with open("strays.json", "r") as f:
    strays = json.load(f)


for folder_path in strays["master"]:
    try:
        metadata = read_info_file(folder_path)
        if "master" not in metadata["discogs_url"]:
            continue

        release = folder_path.split("/")[-1]
        artist = release.split(" - ")[0]
        if artist == "Various Artists":
            artist = "Various"
        album_and_label = release.split(" - ")[1]
        album = album_and_label.split(" [")[0]
        if ":" in album:
            album = album.split(":")[0]
        label = album_and_label.split(" [")[1].split("]")[0]

        new_uri = search(artist, album, label)

        print(folder_path, new_uri)
        metadata["discogs_url"] = new_uri
        write_info_file(folder_path, metadata)
    except Exception as e:
        print("an error:", folder_path, e)
        break
