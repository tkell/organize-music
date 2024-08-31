import os
import json

import src.discogs.lib_discogs as lib_discogs


def make_release_string(release):
    title = release["basic_information"]["title"]
    artist = release["basic_information"]["artists"][0]["name"]
    label = release["basic_information"]["labels"][0]["name"]
    catno = release["basic_information"]["labels"][0]["catno"]
    year = release["basic_information"]["year"]
    release_string = f"{artist} - {title} [{label}] -- {catno}, {year}"
    return release_string


def make_release_json(release, folder_name):
    date_added = release["date_added"]
    date_added = date_added.split("T")[0]
    return {
        "id": release["id"],
        "title": release["basic_information"]["title"],
        "artist": release["basic_information"]["artists"][0]["name"],
        "label": release["basic_information"]["labels"][0]["name"],
        "catno": release["basic_information"]["labels"][0]["catno"],
        "year": release["basic_information"]["year"],
        "purchase_date": date_added,
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
    collection = lib_discogs.call_api_no_cache(url)

    # make and write strings
    all_json_data = []
    all_markdown_strings = []
    for folder in collection["folders"]:
        if folder["name"] not in ["All", "Uncategorized"]:
            folder_name, releases = lib_discogs.get_folder_name_and_releases(folder)
            releases_and_release_data = lib_discogs.get_release_data(releases)

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
