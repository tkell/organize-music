import os
import re
import mutagen
import requests


def set_tag(filepath, tag_name, tag_content):
    f = mutagen.File(filepath)
    tag_name = tag_name.lower()
    f[tag_name] = tag_content
    f.save()


def get_tags(filepath, tag_name):
    f = mutagen.File(filepath)
    try:
        return f.tags[tag_name][0]
    except KeyError:
        return None


label_matcher = r"\[(.*)\]"


def get_label_from(filebase):
    m = re.search(label_matcher, filebase)
    if not m:
        return ""
    return m.group(1)


singles_dir = "/Volumes/Productions"
filenames = os.listdir(singles_dir)
# FLAC only
for filename in filenames:
    if ".flac" in filename:
        if not get_label_from(filename):
            filepath = f"{singles_dir}/{filename}"
            label = get_tags(filepath, "Publisher")
            release_year = get_tags(filepath, "Date")
            if label is not None and release_year is not None:
                continue

            print(filename)
            print("Enter Label!")
            label = input().strip()
            print("Enter Release Year!")
            release_year = input().strip()

            ## update tags – we'll move the files later, in another sweep!
            set_tag(filepath, "Publisher", label)
            set_tag(filepath, "Date", release_year)
