import argparse
import os
import re
import shutil
import mutagen
from mutagen.id3 import ID3, TPUB, TYER
import requests

label_matcher = r"\[(.*)\]"


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


def get_tags_mp3(filepath, tag_name):
    tags = ID3(filepath)
    try:
        if tag_name == "Year":
            return tags["TDRC"].text[0]
        if tag_name == "Publisher":
            return tags["TPUB"].text[0]
    except KeyError:
        return None
    return None


def get_label_from(filebase):
    m = re.search(label_matcher, filebase)
    if not m:
        return ""
    return m.group(1)


def remove_empty_label(filename):
    return filename.replace(" []", "")


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
                label = get_tags_mp3(filepath, "Publisher")
                if not label:
                    print("PANIC", filepath)
                    return
            cleaned_filename = remove_empty_label(filename)
            new_filename = (
                cleaned_filename.replace(extension, "") + f" [{label}]" + extension
            )
            new_filepath = f"{directory}/{new_filename}"
            print(filepath)
            print(new_filepath)
            # shutil.move(filepath, new_filepath)


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
