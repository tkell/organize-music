import os
import random
import re
import shutil
from collections import defaultdict


import discogs_grouper

OLD_PATH = "/Users/thor/Desktop/parsed/singles"
NEW_PATH = "/Users/thor/Desktop/parsed/albums"


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


def create_folder_and_meta(new_data, artist, label):
    release_title, track_number, num_tracks, discogs_url = new_data

    folder = f"{artist} - {release_title} [{label}]".replace("/", ":")
    meta_filename = f"{num_tracks}.tracks"

    print(f"New folder is {folder}")
    print(f"Would write the discogs url to {meta_filename}")
    action = prompt("Write, y / n?")

    if action == "y":
        folder_path = os.path.join(NEW_PATH, folder)
        meta_path = os.path.join(folder_path, meta_filename)
        os.mkdir(folder_path)
        with open(meta_path, "w") as f:
            f.write(discogs_url)

    return folder_path


def move_file(folder_path, new_data, old_data):
    release_title, track_number, num_tracks, discogs_url = new_data
    filename, artist, track, label, extension = old_data
    track_number = track_number + 1
    new_filename = f"{track_number:02d} - {track}.{extension}"

    old_track_path = os.path.join(OLD_PATH, filename)
    track_path = os.path.join(folder_path, new_filename)

    print(f"Preparing to move {filename} to {track_path}")
    action = prompt("Write, y / n?")
    if action == "y":
        shutil.move(old_track_path, track_path)


if __name__ == "__main__":
    print("starting single grouper ...")
    singles = os.listdir(OLD_PATH)
    artist_and_label_groups = group_by_artist_and_label(singles)
    print(f"*** {len(artist_and_label_groups.items())} to go **")

    # This case is "easy":  we just move the one file
    for key, matched_singles in artist_and_label_groups.items():
        if len(matched_singles) == 1:
            artist, label = key
            filename = matched_singles[0]
            track = filename.split(" - ")[1].split(" [")[0]
            extension = filename.split(".")[-1]
            try:
                result = discogs_grouper.group(artist, track, label)
                if result:
                    folder_path = create_folder_and_meta(result, artist, label)
                    old_data = (filename, artist, track, label, extension)
                    release_title, track_numbers, num_tracks, discogs_url = result
                    new_data = (
                        release_title,
                        track_numbers[0],
                        num_tracks,
                        discogs_url,
                    )
                    move_file(folder_path, new_data, old_data)
                    print("done writing, insert celebratory emojis here")
            except SkipRelease:
                next
            except StopRelease:
                break
        else:
            artist, label = key
            matched_singles.sort()
            print("")
            print("Matched multiple tracks:  ", matched_singles)
            print("")
            filename = matched_singles[0]
            first_track = filename.split(" - ")[1].split(" [")[0]
            try:
                print("Getting release from first track")
                result = discogs_grouper.group(artist, first_track, label)
                if result:
                    folder_path = create_folder_and_meta(result, artist, label)

                    release_title, track_numbers, num_tracks, discogs_url = result
                    for track_number, filename in zip(track_numbers, matched_singles):
                        track = filename.split(" - ")[1].split(" [")[0]
                        extension = filename.split(".")[-1]
                        old_data = (filename, artist, track, label, extension)
                        new_data = (
                            release_title,
                            track_number,
                            num_tracks,
                            discogs_url,
                        )
                        move_file(folder_path, new_data, old_data)
                    print("done writing, insert celebratory emojis here")
            except SkipRelease:
                next
            except StopRelease:
                break
