import random
import urllib

import src.discogs.lib_discogs as lib_discogs


class SkipRelease(Exception):
    pass


class StopRelease(Exception):
    pass


class DiscogsSearchFailed(Exception):
    pass


def search(artist, album, label):
    def prompt(msg, klass=str):
        char = random.choice(["-", "_", "~", ">", "*"])
        print(char * 4 + " " + msg)
        return klass(input().strip())

    def enter_data_manually():
        discogs_url = prompt("Enter the discogs url for this release")

        return discogs_url

    def parse_releases_from_discogs(discogs_json):
        release_number = prompt("Select a release", int)
        release = discogs_json["results"][release_number]
        release_url = release["resource_url"]
        release_details = lib_discogs.call_discogs_no_cache(release_url)
        discogs_url = release_details["uri"]

        return discogs_url

    def print_discogs_releases(index, release):
        label = release.get("label", "label missing")
        catno = release.get("catno", "catno missing")
        title = release.get("title", "title missing")
        year = release.get("year", "year missing")

        # hopefully we can use this to avoid "master" releases
        discogs_url = release.get("resource_url", "no resource_url")
        print(f"{index}: {title} - {label} {catno} {year}; {discogs_url}")

    def search_discogs_for_album(artist, album, label, search_attempt):
        a = urllib.parse.quote(artist.lower())
        al = urllib.parse.quote(album.lower())
        l = urllib.parse.quote(label.lower())

        if search_attempt == 0:
            url = f"https://api.discogs.com/database/search?artist={a}&label={l}&release_title={al}"
        elif search_attempt == 1:
            url = (
                f"https://api.discogs.com/database/search?artist={a}&release_title={al}"
            )
        else:
            raise DiscogsSearchFailed

        discogs_json = lib_discogs.call_discogs_no_cache(url)
        return discogs_json

    print(f"about to search for: {artist} - {album} [{label}]")
    ## so this is tricky, we need to do a bunch of searches
    ## if we get an empty search result, do the next search
    ## if we get a search result we don't want,
    ## we want to be able to skip that search manually
    the_search_is_good = False
    discogs_json = None
    search_attempt = 0
    while not the_search_is_good:
        try:
            discogs_json = search_discogs_for_album(
                artist, album, label, search_attempt
            )
        except DiscogsSearchFailed:
            break

        if not discogs_json or len(discogs_json["results"]) == 0:
            search_attempt += 1
            continue
        else:
            print("Found releases from this search:")
            for index, release in enumerate(discogs_json["results"]):
                print_discogs_releases(index, release)

        action = prompt("A good search? 'y' or 'n'?")
        if action == "y":
            the_search_is_good = True
        elif action == "n":
            search_attempt += 1

    if not discogs_json or the_search_is_good is False:
        action = prompt("Fall back to manual entry, or skip?, 'e' or 's'?")
        if action == "e":
            return enter_data_manually()
        elif action == "s":
            raise SkipRelease

    discogs_url = parse_releases_from_discogs(discogs_json)

    return discogs_url
