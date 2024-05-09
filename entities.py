import re
from dataclasses import dataclass


@dataclass
class Album:
    artist: str
    title: str
    label: str


def album_from_folder_name(folder: str):
    artist = folder.split(" - ")[0]
    artist = folder.split(" - ")[0].strip()
    title = folder.split(" - ")[1].split(" [")[0].strip()
    title = title.replace(" : ", " / ")
    label = re.search(r"\[(.+?)\]", folder).group(1)
    return Album(artist, title, label)


@dataclass
class Track:
    artist: str
    title: str
    label: str
    extension: str
    position: int
