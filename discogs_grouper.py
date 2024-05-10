import random
import urllib

import org.discogs.lib_discogs as lib_discogs


class SkipRelease(Exception):
    pass


class StopRelease(Exception):
    pass


class DiscogsSearchFailed(Exception):
    pass


def group(artist, track, label):
    def prompt(msg, klass=str):
        char = random.choice(["-", "_", "~", ">", "*"])
        print(char * 4 + " " + msg)
        return klass(input().strip())

    def enter_data_manually(track):
        release_title = prompt("Enter the title for this release")
        discogs_url = prompt("Enter the discogs url for this release")
        num_tracks = prompt("How many tracks do we have?", int)
        track_numbers = prompt("Enter the track index for this track(s)", str)
        track_numbers = list(map(int, track_numbers.split(",")))

        return release_title, track_numbers, num_tracks, discogs_url

    def parse_releases_from_discogs(discogs_json):
        release_number = prompt("Select a release", int)
        release = discogs_json["results"][release_number]
        release_url = release["resource_url"]
        release_details = lib_discogs.call_discogs_no_cache(release_url)

        for index, track in enumerate(release_details["tracklist"]):
            title = track["title"]
            print(f"{index}, {artist}, {title}")

        track_numbers = prompt("Enter the track index(es) / '-1' to go back", str)
        if track_numbers == "-1":
            # this is our "we did not like this release" state!
            return None
        else:
            track_numbers = list(map(int, track_numbers.split(",")))

        num_tracks = len(release_details["tracklist"])
        discogs_url = release_details["uri"]
        release_title = release_details["title"]
        return release_title, track_numbers, num_tracks, discogs_url

    def print_discogs_releases(index, release):
        url = release.get("resource_url", "")
        # try a bit harder to avoid master releases
        if "masters/" in url:
            print("skipped master release")
            return

        label = release.get("label", "label missing")
        catno = release.get("catno", "catno missing")
        title = release.get("title", "title missing")
        year = release.get("year", "year missing")
        print(f"{index}: {title} - {label} {catno} {year}")

    def search_discogs_for_track(artist, track, label, search_attempt):
        a = urllib.parse.quote(artist.lower())
        t = urllib.parse.quote(track.lower().replace("(original mix)", ""))
        l = urllib.parse.quote(label.lower())

        if search_attempt == 0:
            url = f"https://api.discogs.com/database/search?artist={a}&label={l}&track={t}"
        elif search_attempt == 1:
            url = f"https://api.discogs.com/database/search?artist={a}&track={t}"
        elif search_attempt == 2:
            url = f"https://api.discogs.com/database/search?artist={a}&label={l}"
        elif search_attempt == 3:
            url = f"https://api.discogs.com/database/search?track={t}&label={l}"
        elif search_attempt == 4:
            url = f"https://api.discogs.com/database/search?artist={a}"
        elif search_attempt == 5:
            url = f"https://api.discogs.com/database/search?track={t}"
        else:
            raise DiscogsSearchFailed

        discogs_json = lib_discogs.call_discogs_no_cache(url)
        return discogs_json

    print(f"{artist} - {track} [{label}]")
    action = prompt("'s' to skip, 'd' for discogs search, 'e' to enter data manually")
    if action == "s":
        raise SkipRelease
    elif action == "q":
        raise StopRelease
    elif action == "d":
        ## so this is tricky, we need to do a bunch of searches
        ## if we get an empty search result, do the next search
        ## if we get a search result, we don't want, we want to be able to skip that search manually
        the_search_is_good = False
        discogs_json = None
        search_attempt = 0
        while not the_search_is_good:
            try:
                discogs_json = search_discogs_for_track(
                    artist, track, label, search_attempt
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
                return enter_data_manually(track)
            elif action == "s":
                raise SkipRelease

        results = parse_releases_from_discogs(discogs_json)
        while not results:
            print("Found releases from this search:")
            for index, release in enumerate(discogs_json["results"]):
                print_discogs_releases(index, release)
            results = parse_releases_from_discogs(discogs_json)

        return results

    elif action == "e":
        return enter_data_manually(track)
