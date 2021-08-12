import argparse
import os
import re
import shutil
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


def old_stuff():
    ## update tags – we'll move the files later, in another sweep!
    set_tag(filepath, "Publisher", label)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir")
    parser.add_argument("--file_type")
    args = parser.parse_args()
    extension = f".{args.file_type}"

    # OK, need to get mp3s working, and need to get something that works for directories
    # Albums look pretty good, tbh?
    for filename in os.listdir(args.dir):
        if extension in filename:
            if not get_label_from(filename):
                filepath = f"{args.dir}/{filename}"
                if extension == ".flac":
                    label = get_tags(filepath, "Publisher")
                    if not label:
                        print("PANIC", filepath)
                        break
                elif extension == ".mp3":
                    print("oh no, need to get the mp3 tag reader in")
                new_filename = (
                    filename.replace(extension, "") + f" [{label}]" + extension
                )
                new_filepath = f"{args.dir}/{new_filename}"
                print(filepath)
                print(new_filepath)
                shutil.move(filepath, new_filepath)
