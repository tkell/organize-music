import argparse
import os
import re
import shutil
import mutagen
import requests

label_matcher = r"\[(.*)\]"
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


def get_label_from(filebase):
    m = re.search(label_matcher, filebase)
    if not m:
        return ""
    return m.group(1)


def copy_tag_to_filename(extension, filename, directory):
    if extension in filename:
        if not get_label_from(filename):
            filepath = f"{directory}/{filename}"
            if extension == ".flac":
                label = get_tags(filepath, "Publisher")
                if not label:
                    print("PANIC", filepath)
                    return
            elif extension == ".mp3":
                print("oh no, need to get the mp3 tag reader in")
            new_filename = filename.replace(extension, "") + f" [{label}]" + extension
            new_filepath = f"{directory}/{new_filename}"
            print(filepath)
            print(new_filepath)
            # shutil.move(filepath, new_filepath)


def remove_empty_label(filename):
    return filename.replace("[]", "").strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir")
    parser.add_argument("--file_type")
    args = parser.parse_args()
    if args.file_type != "folder":
        extension = f".{args.file_type}"
        for filename in os.listdir(args.dir):
            copy_tag_to_filename(extension, filename, args.dir)
    elif args.file_type == "folder":
        for filename in os.listdir(args.dir):
            filepath = f"{args.dir}/{filename}"
            if os.path.isdir(filepath):
                if not get_label_from(filepath):
                    print(filepath)
                    print("Enter Label!")
                    label = input().strip()
                    new_filename = remove_empty_label(filename) + f" [{label}]"
                    new_filepath = f"{args.dir}/{new_filename}"
                    print(filepath)
                    print(new_filepath)
                    # shutil.move(filepath, new_filepath)
