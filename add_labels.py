import os
import re
import mutagen
from mutagen.id3 import ID3, TPUB, TYER
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
    tags = ID3(filepath)
    if tag_name == "Year":
        tags.add(TYER(encoding=3, text=tag_content))
    if tag_name == "Publisher":
        tags.add(TPUB(encoding=3, text=tag_content))
    tags.save(filepath)


def get_tags(filepath, tag_name):
    tags = ID3(filepath)
    try:
        if tag_name == "Year":
            return tags["TDRC"].text[0]
        if tag_name == "Publisher":
            return tags["TPUB"].text[0]
    except KeyError:
        return None
    return None


label_matcher = r"\[(.*)\]"


def get_label_from(filebase):
    m = re.search(label_matcher, filebase)
    if not m:
        return ""
    return m.group(1)


singles_dir = "/Volumes/Music/Singles"
filenames = os.listdir(singles_dir)
filenames.reverse()
# MP3 ONLY
for filename in filenames:
    if ".mp3" in filename:
        if not get_label_from(filename):
            filepath = f"{singles_dir}/{filename}"
            label = get_tags(filepath, "Publisher")
            release_year = get_tags(filepath, "Year")
            if label is not None and release_year is not None:
                continue

            print(filename)
            (track, extension) = filename.split(".")
            track = track.replace("(Original Mix)", "").strip()
            search_url = (
                f'https://api.discogs.com/database/search?query="{track}"&type=release'
            )
            res = call_discogs(search_url)
            try:
                potential_label = res["results"][0]["label"][0]
                potential_year = res["results"][0]["year"]
            except Exception:
                potential_label = None
                potential_year = None
                print("Discogs failed!  Happy googling =[")

            print(f"Potential Label:  {potential_label}")
            print("Accept Label, y/n?")
            q = input()
            if q == "y":
                label = potential_label
            else:
                print("Enter Label!")
                label = input().strip()

            print(f"Potential Release Year:  {potential_year}")
            print("Accept Release Year, y/n?")
            q = input()
            if q == "y":
                release_year = potential_year
            else:
                print("Enter Release Year!")
                release_year = input().strip()

            ## update tags – we'll move the files later, in another sweep!
            set_tag(filepath, "Publisher", label)
            set_tag(filepath, "Year", release_year)
