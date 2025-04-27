import argparse
import os
import random
import re
import shutil
from collections import defaultdict

import src.discogs.discogs_grouper as discogs_grouper
from src.organize_music.local_file_io import write_info_file


class SkipRelease(Exception):
    pass


class StopRelease(Exception):
    pass


class DiscogsSearchFailed(Exception):
    pass


def prompt(msg, klass=str):
    char = random.choice(["-", "_", "~", ">", "*"])
    print(char * 4 + " " + msg)
    return klass(input().strip())


def group_by_artist_and_label(singles):
    def is_music_file(filename):
        return filename.endswith(".mp3") or filename.endswith(".flac")

    def key_by_artist_and_label(single):
        artist = single.split(" - ")[0]
        label = re.search(r"\[(.+?)\]", single).group(1)
        return (artist, label)

    artist_and_label_groups = defaultdict(list)
    for single in singles:
        if is_music_file(single):
            key = key_by_artist_and_label(single)
            artist_and_label_groups[key].append(single)
    return artist_and_label_groups


def create_folder_and_meta(new_data, artist, label, albums_path):
    release_title, track_number, num_tracks, discogs_url = new_data
    folder = f"{artist} - {release_title} [{label}]".replace("/", ":")
    print(f"New folder is {folder}")
    action = prompt("Write, y / n?")

    if action == "y":
        folder_path = os.path.join(albums_path, folder)
        os.mkdir(folder_path)
        metadata = {"num_tracks": num_tracks, "discogs_url": discogs_url}
        write_info_file(folder_path, metadata)

    return folder_path


def move_file(folder_path, new_data, old_data, singles_path):
    release_title, track_number, num_tracks, discogs_url = new_data
    filename, artist, track, label, extension = old_data
    track_number = track_number + 1
    new_filename = f"{track_number:02d} - {track}.{extension}"

    old_track_path = os.path.join(singles_path, filename)
    track_path = os.path.join(folder_path, new_filename)

    print(f"Preparing to move {filename} to {track_path}")
    action = prompt("Write, y / n?")
    if action == "y":
        shutil.move(old_track_path, track_path)


def _handle_and_move_each_file(filename, track_number, artist, label, singles_path):
    track = filename.split(" - ")[1].split(" [")[0]
    extension = filename.split(".")[-1]
    old_data = (filename, artist, track, label, extension)
    new_data = (
        release_title,
        track_number,
        num_tracks,
        discogs_url,
    )
    move_file(folder_path, new_data, old_data, singles_path)


if __name__ == "__main__":
    print("starting single grouper ...")
    parser = argparse.ArgumentParser()
    parser.add_argument("singles_path")
    parser.add_argument("album_path")
    args = parser.parse_args()

    singles_path = args.singles_path
    album_path = args.album_path
    singles = os.listdir(singles_path)

    artist_and_label_groups = group_by_artist_and_label(singles)
    print(f"*** {len(artist_and_label_groups.items())} to go **")

    for key, matched_singles in artist_and_label_groups.items():
        artist, label = key
        matched_singles.sort()
        print(f"Matched tracks:  {matched_singles}\n")
        filename = matched_singles[0]
        first_track = filename.split(" - ")[1].split(" [")[0]
        try:
            print("Getting release from first track")
            result = discogs_grouper.group(artist, first_track, label)
            if result:
                folder_path = create_folder_and_meta(result, artist, label, album_path)
                release_title, track_numbers, num_tracks, discogs_url = result
                for track_number, filename in zip(track_numbers, matched_singles):
                    _handle_and_move_each_file(
                        filename, track_number, artist, label, singles_path
                    )
                print("done writing, insert celebratory emojis here 🎊🎉🎈")
        except SkipRelease:
            next
        except StopRelease:
            break
