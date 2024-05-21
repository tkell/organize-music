import json
import pickle
import random
import time
from urllib.parse import urlparse

import requests

CACHE_FILENAME = "discogs-cache.pkl"
USER_AGENT = "DiscogsOrganize +http://tide-pool.ca"
DISCOGS_TOKEN_FILE = (
    "/Volumes/Bragi/Code/music-collection/organize-music/discogs-token.txt"
)


def _load_cache(cache_filename):
    try:
        with open(cache_filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        with open(cache_filename, "wb") as f:
            pickle.dump({}, f)
            return {}


def _get_cache_expiry():
    """Calculate a random cache expiry time (120-300 days)."""
    days = random.randint(120, 300)
    return 60 * 60 * 24 * days


def _read_cache(url):
    if url in DISCOGS_CACHE:
        return DISCOGS_CACHE[url]
    else:
        return None


def _write_cache(url, timestamp, json_data):
    DISCOGS_CACHE[url] = (json_data, timestamp)
    with open(CACHE_FILENAME, "wb") as f:
        pickle.dump(DISCOGS_CACHE, f)


def _load_token(token_filename):
    with open(token_filename) as f:
        return f.readline().strip()


def _make_call(url):
    """Wrapper around requests to make testing easier."""
    headers = {
        "user-agent": USER_AGENT,
        "Authorization": f"Discogs token={DISCOGS_TOKEN}",
    }
    return requests.get(url, headers=headers)


# Load token and cache
DISCOGS_CACHE = _load_cache(CACHE_FILENAME)
DISCOGS_TOKEN = _load_token(DISCOGS_TOKEN_FILE)


def _call_discogs_api(url, is_retry=False):
    """Make a request to the Discogs API with error handling and retries."""
    r = _make_call(url)
    time.sleep(random.randint(4, 5))  # Rate limiting
    print("Calling: ", url)

    try:
        result = r.json()
    except json.JSONDecodeError:
        print("Calling URL failed:", url)
        print("Response reason:", r.reason, r.status_code)
        if r.status_code == 502 and not is_retry:
            time.sleep(random.randint(7, 10))
            result = _call_discogs_api(url, is_retry=True)
        else:
            print("Calling URL failed with retry, panic!", url)
            print("Response reason:", r.reason, r.status_code)

    return result


def call_api(url):
    """Call the Discogs API with caching."""
    now = int(time.time())
    if (cache_contents := _read_cache(url)) is not None:
        (cached_data, timestamp) = cache_contents
        cache_expiry_seconds = _get_cache_expiry()
        if now - timestamp < cache_expiry_seconds:
            print("Cache hit:", url)
            return cached_data

    print("Cache miss:", url)
    json_data = _call_discogs_api(url)
    _write_cache(url, now, json_data)
    return json_data


def get_release_data(releases):
    """Retrieve Discogs data for a list of releases."""
    data = []
    for release in releases:
        release_url = release["basic_information"]["resource_url"]
        release_data = call_api(release_url)
        data.append((release, release_data))
    return data


def get_folder_name_and_releases(discogs_folder):
    """Get the folder name and releases from a Discogs folder."""
    url = discogs_folder["resource_url"] + "/releases?per_page=100"
    name = discogs_folder["name"].replace('""', "")
    folder_data = _call_discogs_api(url)
    releases = folder_data["releases"]
    return name, releases


def download_release_data(album_source_url):
    """
    Download release data from Discogs given a release URL.
    (The album url path looks like /release/4301112-95-North-Let-Go-Remixes)
    """
    album_url = urlparse(album_source_url)
    release_id = album_url.path.split("/")[2].split("-")[0]
    release_api_url = f"https://api.discogs.com/releases/{release_id}"
    release_data = call_api(release_api_url)

    return release_data
