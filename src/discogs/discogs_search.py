import urllib

import src.discogs.lib_discogs as lib_discogs

from src.discogs.discogs_utils import DiscogsSearchFailed, prompt

BASE_URL = "https://api.discogs.com/database/search?"


def _print_discogs_releases(index, release):
    label = release.get("label", "label missing")
    catno = release.get("catno", "catno missing")
    title = release.get("title", "title missing")
    year = release.get("year", "year missing")
    released = release.get("released", "released missing")

    discogs_url = release.get("resource_url", "no resource_url")
    print(f"{index}: {title} - {label} {catno} -- {year} or {released}; {discogs_url}")


def _prompt_and_get_release_details(all_releases):
    """Prompt user to select a release and return details."""
    release_number = prompt("Select a release", int)
    release = all_releases[release_number]
    release_url = release["resource_url"]
    release_details = lib_discogs.call_api(release_url)

    return release_details


def search_for_release(**kwargs):
    """
    Search Discogs based on provided artist, album, track, and label.

    Args:
        artist (str): Artist name.
        album (str, optional): Album name.
        track (str, optional): Track name.
        label (str, optional): Label name.

    Returns:
        discogs release details, as a dict
    """
    artist = kwargs.get("artist")
    album = kwargs.get("album")
    track = kwargs.get("track")
    label = kwargs.get("label")

    if artist and track:
        url_builder = url_builder_for_tracks
    elif artist and album:
        url_builder = url_builder_for_albums
    else:
        raise ValueError("Must provide artist, and either track or album.")

    done = False
    discogs_json = None
    search_attempt = 0
    while not done:
        try:
            url = url_builder(artist, track or album, label, search_attempt)
            discogs_json = lib_discogs.call_api(url)
        except DiscogsSearchFailed:
            break

        if not discogs_json or len(discogs_json["results"]) == 0:
            search_attempt += 1
            continue
        else:
            print("Found releases from this search:")
            all_releases = discogs_json["results"]
            for index, release in enumerate(all_releases):
                url = release.get("resource_url", "")
                if "master/" in url:
                    continue
                _print_discogs_releases(index, release)

        action = prompt("A good search? 'y' or 'n'?")
        if action == "y":
            done = True
        elif action == "n":
            search_attempt += 1

    release = _prompt_and_get_release_details(all_releases)

    return release


def url_builder_for_tracks(artist, track, label, search_attempt):
    ar = urllib.parse.quote(artist.lower())
    tr = urllib.parse.quote(track.lower().replace("(original mix)", ""))
    la = urllib.parse.quote(label.lower())

    if search_attempt == 0:
        url = f"{BASE_URL}artist={ar}&label={la}&track={tr}"
    elif search_attempt == 1:
        url = f"{BASE_URL}artist={ar}&track={tr}"
    elif search_attempt == 2:
        url = f"{BASE_URL}artist={ar}&label={la}"
    elif search_attempt == 3:
        url = f"{BASE_URL}track={tr}&label={la}"
    elif search_attempt == 4:
        url = f"{BASE_URL}artist={ar}"
    elif search_attempt == 5:
        url = f"{BASE_URL}track={tr}"
    else:
        raise DiscogsSearchFailed

    return url


def url_builder_for_albums(artist, album, label, search_attempt):
    ar = urllib.parse.quote(artist.lower())
    al = urllib.parse.quote(album.lower())
    la = urllib.parse.quote(label.lower())

    if search_attempt == 0:
        url = f"{BASE_URL}artist={ar}&label={la}&release_title={al}"
    elif search_attempt == 1:
        url = f"""{BASE_URL}artist={ar}&release_title={al}"""
    else:
        raise DiscogsSearchFailed

    return url
