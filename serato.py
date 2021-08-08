import os
import re
import scratchlivedb


label_matcher = r"\[(.*)\]"
album_matcher = r"\/Albums\/.+? - (.+?)[ \[]"
simple_album_matcher = r"\/Albums\/(.+?)"


def make_track_string(entry):
    artist = entry.trackartist
    title = entry.tracktitle
    bpm = entry.trackbpm
    length = entry.tracklength
    timestamp_added = entry.trackadded
    label = get_label_from(entry.filebase)
    if is_album_folder(entry.filebase):
        album = get_album_from(entry.filebase)
    return f"{artist} - {title} [{label}] -- {length}"


def make_markdown_block(track_strings):
    items = "\n".join(track_strings)
    return "\n" + items + "\n\n"


def get_label_from(filebase):
    m = re.search(label_matcher, filebase)
    if not m:
        return ""
    return m.group(1)


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
    track_strings = []
    for entry in serato_database.entries:
        track_strings.append(make_track_string(entry))
    with open(output_filename, "a") as f:
        f.write(make_markdown_block(track_strings))


if __name__ == "__main__":
    output_filename = "digital.md"
    try:
        os.remove(output_filename)
    except FileNotFoundError:
        pass
    db = scratchlivedb.ScratchDatabase("serato-db/database V2")
    make_markdown_file(db, output_filename)
