import os
import json
import re
import scratchlivedb


label_matcher = r"\[(.*)\]"
album_matcher = r"\/Albums\/.+? - (.+?)[ \[]"
simple_album_matcher = r"\/Albums\/(.+?)"


def make_track_string(entry):
    artist = entry.trackartist
    title = entry.tracktitle
    length = entry.tracklength
    label = get_label(entry)
    return f"{artist} - {title} [{label}] -- {length}"


def make_json_dict(entry):
    return {
        "artist": entry.trackartist,
        "track": entry.tracktitle,
        "bpm": entry.trackbpm,
        "length": entry.tracklength,
        "timestamp_added": entry.trackadded,
        "label": get_label(entry),
    }


def make_markdown_block(track_strings):
    items = "\n".join(track_strings)
    return "\n" + items + "\n\n"


## ALWAYS DIGITAL
def get_label(entry):
    m = re.search(label_matcher, entry.filebase)
    if not m:
        return ""
    return m.group(1)


## Not currently used, but will need to add "albumness" later
def get_album_from(filebase):
    m = re.search(album_matcher, filebase)
    if not m:
        m = re.search(simple_album_matcher, filebase)
    if not m:
        return ""
    return m.group(1)


def is_album_folder(filebase):
    if "/Albums/" in filebase:
        return True
    else:
        return False


def make_markdown_file(serato_database, output_filename):
    try:
        os.remove(output_filename)
    except FileNotFoundError:
        pass
    track_strings = [make_track_string(entry) for entry in serato_database.entries]
    with open(output_filename, "a") as f:
        f.write(make_markdown_block(track_strings))


def make_json_file(serato_database, output_filename):
    try:
        os.remove(output_filename)
    except FileNotFoundError:
        pass
    json_data = [make_json_dict(entry) for entry in serato_database.entries]
    with open(output_filename, "w") as f:
        json.dump(json_data, f)


if __name__ == "__main__":
    db = scratchlivedb.ScratchDatabase("serato-db/database V2")
    make_markdown_file(db, "serato.md")
    make_json_file(db, "serato.json")
