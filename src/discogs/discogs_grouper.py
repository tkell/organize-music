from src.discogs.discogs_search import search

from src.discogs.discogs_utils import (
    SkipRelease,
    StopRelease,
    prompt,
)


def _enter_data_manually(track):
    release_title = prompt("Enter the title for this release")
    discogs_url = prompt("Enter the discogs url for this release")
    num_tracks = prompt("How many tracks do we have?", int)
    track_numbers = prompt("Enter the track index for this track(s)", str)
    track_numbers = list(map(int, track_numbers.split(",")))

    return release_title, track_numbers, num_tracks, discogs_url


def _prompt_and_pick_tracks(artist, release_details):
    for index, track in enumerate(release_details["tracklist"]):
        title = track["title"]
        print(f"{index}, {artist}, {title}")

    track_numbers = prompt("Enter the track index(es) / '-1' to go back", str)
    # this is our "we did not like this release" state,
    # not sure if this still works post-refactor
    if track_numbers == "-1":
        raise SkipRelease
    else:
        track_numbers = list(map(int, track_numbers.split(",")))

    return track_numbers


def _prompt_and_do_manual_entry(track):
    action = prompt("Fall back to manual entry, or skip?, 'e' or 's'?")
    if action == "e":
        return _enter_data_manually(track)
    elif action == "s":
        raise SkipRelease


def group(artist, track, label):
    print(f"{artist} - {track} [{label}]")
    action = prompt("'s' to skip, 'd' for discogs search, 'e' to enter data manually")
    if action == "s":
        raise SkipRelease
    elif action == "q":
        raise StopRelease
    elif action == "d":
        release_details = search(artist=artist, track=track, label=label)
        if not release_details or "tracklist" not in release_details:
            return _prompt_and_do_manual_entry(track)

        track_numbers = _prompt_and_pick_tracks(artist, release_details)

        num_tracks = len(release_details["tracklist"])
        discogs_url = release_details["uri"]
        release_title = release_details["title"]
        return release_title, track_numbers, num_tracks, discogs_url

    elif action == "e":
        return _enter_data_manually(track)
