import os
import re
import mutagen
import requests

# import the token
with open("discogs-token.txt") as f:
    discogs_token = f.readline().strip()


def call_discogs(url):
    headers = {
        "user-agent": "DiscogsOrganize +http://tide-pool.ca",
        "Authorization": f"Discogs token={discogs_token}",
    }
    r = requests.get(url, headers=headers)
    return r.json()


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
# FLACS DONE, GOTTA MAKE MP3S WORK
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
