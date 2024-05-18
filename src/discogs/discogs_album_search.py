from src.discogs.discogs_search import search
from src.discogs.discogs_utils import SkipRelease, prompt


def enter_data_manually():
    discogs_url = prompt("Enter the discogs url for this release")
    return discogs_url


def search_for_albums(artist, album, label):
    print(f"about to search for: {artist} - {album} [{label}]")
    release_details = search(artist=artist, album=album, label=label)

    if not release_details:
        action = prompt("Fall back to manual entry, or skip?, 'e' or 's'?")
        if action == "e":
            return enter_data_manually()
        elif action == "s":
            raise SkipRelease
    else:
        return release_details["uri"]
