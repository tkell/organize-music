import json
import pickle
import random
import time

import requests

# import the token
with open("/Volumes/Bragi/Code/music-collection/organize-music/discogs-token.txt") as f:
    discogs_token = f.readline().strip()

# load the cache
cache_filename = "discogs-cache.pkl"
try:
    with open(cache_filename, "rb") as f:
        discogs_cache = pickle.load(f)
except Exception:
    with open(cache_filename, "wb") as f:
        pickle.dump({}, f)
        discogs_cache = {}

# cache for 60 to 120 days
# this jitter at runtime is so we don't just re-hammer discogs
def get_cache_expiry():
    days = random.randint(60, 120)
    return 60 * 60 * 24 * days


def call_discogs_no_cache(url, is_retry=False):
    headers = {
        "user-agent": "DiscogsOrganize +http://tide-pool.ca",
        "Authorization": f"Discogs token={discogs_token}",
    }
    r = requests.get(url, headers=headers)

    time.sleep(random.randint(4, 5))
    print("calling: ", url)
    try:
        result = r.json()
    except json.JSONDecodeError:
        print("calling url failed:", url)
        print("response reason", r.reason, r.status_code)
        if r.status_code == 502 and is_retry is False:
            time_to_sleep = random.randint(7, 10)
            time.sleep(time_to_sleep)
            result = call_discogs_no_cache(url, is_retry=True)
        else:
            print("calling url failed with Retry, panic!", url)
            print("response reason", r.reason, r.status_code)

    return result


def call_discogs(url):
    now = int(time.time())
    if discogs_cache.get(url):
        cached_data, timestamp = discogs_cache[url]
        cache_expiry_seconds = get_cache_expiry()
        if now - timestamp < cache_expiry_seconds:
            print("cache hit: ", url)
            return cached_data
    print("cache miss: ", url)
    json_data = call_discogs_no_cache(url)
    discogs_cache[url] = (json_data, now)
    # load / overwrite cache each time!
    with open(cache_filename, "wb") as f:
        pickle.dump(discogs_cache, f)
    return discogs_cache[url][0]


def get_release_data(releases):
    data = []
    for release in releases:
        release_url = release["basic_information"]["resource_url"]
        release_data = call_discogs(release_url)
        data.append((release, release_data))
    return data


def get_folder_name_and_releases(folder):
    url = folder["resource_url"] + "/releases?per_page=100"
    name = folder["name"].replace('""', "")
    folder_data = call_discogs_no_cache(url)
    releases = folder_data["releases"]
    return name, releases
