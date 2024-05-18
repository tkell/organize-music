import json
import pickle
import random
import time
from urllib.parse import urlparse

import requests

# Constants
CACHE_FILENAME = "discogs-cache.pkl"
USER_AGENT = "DiscogsOrganize +http://tide-pool.ca"
DISCOGS_TOKEN_FILE = (
    "/Volumes/Bragi/Code/music-collection/organize-music/discogs-token.txt"
)

# Load token and cache
with open(DISCOGS_TOKEN_FILE) as f:
    DISCOGS_TOKEN = f.readline().strip()
try:
    with open(CACHE_FILENAME, "rb") as f:
        DISCOGS_CACHE = pickle.load(f)
except Exception:
    with open(CACHE_FILENAME, "wb") as f:
        pickle.dump({}, f)
        DISCOGS_CACHE = {}


def _get_cache_expiry():
    """Calculate a random cache expiry time (120-300 days)."""
    days = random.randint(120, 300)
    return 60 * 60 * 24 * days


def _call_discogs_api(url, is_retry=False):
    """Make a request to the Discogs API with error handling and retries."""
    headers = {
        "user-agent": USER_AGENT,
        "Authorization": f"Discogs token={DISCOGS_TOKEN}",
    }
    r = requests.get(url, headers=headers)

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
    if url in DISCOGS_CACHE:
        cached_data, timestamp = DISCOGS_CACHE[url]
        cache_expiry_seconds = _get_cache_expiry()
        if now - timestamp < cache_expiry_seconds:
            print("Cache hit:", url)
            return cached_data

    print("Cache miss:", url)
    json_data = _call_discogs_api(url)
    DISCOGS_CACHE[url] = (json_data, now)

    with open(CACHE_FILENAME, "wb") as f:
        pickle.dump(DISCOGS_CACHE, f)
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
    (The album url path looks like /release/4301112-95-North-Let-Yourself-Go-Remixes)
    """
    album_url = urlparse(album_source_url)
    release_id = album_url.path.split("/")[2].split("-")[0]
    release_api_url = f"https://api.discogs.com/releases/{release_id}"
    release_data = call_api(release_api_url)

    return release_data
