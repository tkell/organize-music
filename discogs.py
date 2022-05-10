import os
import json
import pickle
import time
import random
import requests

# import the token
with open("discogs-token.txt") as f:
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

    time.sleep(2)
    print("calling: ", url)
    try:
        result = r.json()
    except json.JSONDecodeError:
        print("calling url failed:", url)
        print("response reason", r.reason, r.status_code)
        if r.status_code == 502 and is_retry == False:
            time_to_sleep = random.randint(3, 6)
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


def make_release_string(release):
    title = release["basic_information"]["title"]
    artist = release["basic_information"]["artists"][0]["name"]
    label = release["basic_information"]["labels"][0]["name"]
    catno = release["basic_information"]["labels"][0]["catno"]
    year = release["basic_information"]["year"]
    release_string = f"{artist} - {title} [{label}] -- {catno}, {year}"
    return release_string


def make_release_json(release, folder_name):
    return {
        "id": release["id"],
        "title": release["basic_information"]["title"],
        "artist": release["basic_information"]["artists"][0]["name"],
        "label": release["basic_information"]["labels"][0]["name"],
        "catno": release["basic_information"]["labels"][0]["catno"],
        "year": release["basic_information"]["year"],
        "cover_image": release["basic_information"]["cover_image"],
        "folder": folder_name,
    }


def markdown_block(folder_name, release_strings):
    title = f"#{folder_name}"
    items = "\n".join(release_strings)
    return title + "\n" + items + "\n\n"


def make_track_string(track):
    return f"  {track['position']} - {track['title']} - {track['duration']}"


def make_track_json(track):
    return {
        "position": track["position"],
        "title": track["title"],
        "duration": track["duration"],
    }


def create_markdown_for_release(release, release_data):
    release_strings = []
    release_strings.append(make_release_string(release))
    tracks = release_data["tracklist"]
    for track in tracks:
        release_strings.append(make_track_string(track))
    return "\n".join(release_strings)


if __name__ == "__main__":
    output_file = "vinyl.md"
    output_json = "vinyl.json"
    try:
        os.remove(output_file)
        os.remove(output_json)
    except FileNotFoundError:
        pass

    # call collection by folder
    url = "https://api.discogs.com/users/tkell/collection/folders"
    collection = call_discogs_no_cache(url)

    # make and write strings
    all_json_data = []
    all_markdown_strings = []
    for folder in collection["folders"]:
        if folder["name"] not in ["All", "Uncategorized"]:
            folder_name, releases = get_folder_name_and_releases(folder)
            releases_and_release_data = get_release_data(releases)

            folder_markdown_strings = []
            for release, release_data in releases_and_release_data:
                markdown_string = create_markdown_for_release(release, release_data)
                folder_markdown_strings.append(markdown_string)

            for release, release_data in releases_and_release_data:
                json_entry = make_release_json(release, folder_name)
                track_json = [
                    make_track_json(track) for track in release_data["tracklist"]
                ]
                json_entry["tracks"] = track_json
                all_json_data.append(json_entry)

            all_markdown_strings.append(
                markdown_block(folder_name, folder_markdown_strings)
            )

    with open(output_file, "w") as f:
        f.write("\n".join(all_markdown_strings))
    with open(output_json, "w") as f:
        json.dump(all_json_data, f)
