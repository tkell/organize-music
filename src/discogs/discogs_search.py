import urllib
from itertools import combinations

import src.discogs.lib_discogs as lib_discogs

from src.discogs.discogs_utils import prompt

BASE_URL = "https://api.discogs.com/database/search?"


def _permute_search_terms(all_keys, **kwargs):
    permutations = []
    our_keys = [key for key in all_keys if key in kwargs]

    for i in range(1, len(our_keys) + 1):
        for combination in combinations(our_keys, i):
            permutation = {key: kwargs.get(key) for key in combination}
            permutations.append(permutation)

    permutations = sorted(permutations, key=lambda x: len(x), reverse=True)

    return permutations


def build_search_urls(**kwargs):
    keys = ["artist", "release_title", "track", "label"]
    permutations = _permute_search_terms(keys, **kwargs)
    urls = []
    for p in permutations:
        url = f"{BASE_URL}" + urllib.parse.urlencode(p)
        urls.append(url)

    return urls


def _print_discogs_release(index, release):
    label = release.get("label", "label missing")
    catno = release.get("catno", "catno missing")
    title = release.get("title", "title missing")
    title_str = f"{title} - {label} {catno}"

    year = release.get("year", "year missing")
    released = release.get("released", "released missing")
    year_str = f"{year} or {released}"

    release_format = release.get("format", "no format")

    print(f"{index}: {title_str} -- {year_str}; {release_format}")


def _prompt_and_get_release_details(good_releases):
    """Prompt user to select a release and return details."""
    release_number = prompt("Select a release", int)
    release = good_releases[release_number]

    return release["resource_url"]


def sort_and_filter_releases(all_releases):
    good_releases = []
    for release in all_releases:
        if "master/" in release["resource_url"]:
            continue
        if not release.get("year", None):
            continue
        if "spacer.gif" in release.get("cover_image", ""):
            continue

        good_releases.append(release)

    return sorted(good_releases, key=lambda x: x["year"])


def search(**kwargs):
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
    if "album" in kwargs:
        kwargs["release_title"] = kwargs.get("album", "")
        del kwargs["album"]
    

    done = False
    discogs_json = None
    all_releases = None
    search_attempt = 0
    search_urls = build_search_urls(**kwargs)

    while not done and search_attempt < len(search_urls):
        url = search_urls[search_attempt]
        discogs_json = lib_discogs.call_api(url)

        if not discogs_json or len(discogs_json["results"]) == 0:
            search_attempt += 1
            continue
        else:
            print("Found releases from this search:")
            all_releases = discogs_json["results"]
            good_releases = sort_and_filter_releases(all_releases)
            for index, release in enumerate(good_releases):
                _print_discogs_release(index, release)

        action = prompt("A good search? 'y' or 'n'?")
        if action == "y":
            done = True
        elif action == "n":
            search_attempt += 1

    if done:
        release_api_url = _prompt_and_get_release_details(good_releases)
        return lib_discogs.call_api(release_api_url)
    else:
        return None
