import os
import json
import requests

# import the token
with open("discogs-token.txt") as f:
    discogs_token = f.readline().strip()


def call_discogs(url):
    headers = {
        "user-agent": "DiscogsOrganize +http://tide-pool.ca",
        "Authorization": f"Discogs token={discogs_token}",
    }
    r = requests.get(url, headers=headers)
    print("calling: ", url)
    return r.json()


def make_release_string(release):
    title = release["basic_information"]["title"]
    artist = release["basic_information"]["artists"][0]["name"]
    label = release["basic_information"]["labels"][0]["name"]
    catno = release["basic_information"]["labels"][0]["catno"]
    year = release["basic_information"]["year"]
    release_string = f"{artist} - {title} [{label}] -- {catno}, {year}"
    return release_string


def make_markdown_block(folder_name, release_strings):
    title = f"#{folder_name}"
    items = "\n".join(release_strings)
    return title + "\n" + items + "\n\n"


if __name__ == "__main__":
    output_file = "vinyl.md"
    try:
        os.remove(output_file)
    except FileNotFoundError:
        pass

    # call collection by folder
    url = "https://api.discogs.com/users/tkell/collection/folders"
    collection = call_discogs(url)

    # make and write strings
    for folder in collection["folders"]:
        if folder["name"] not in ["All", "Uncategorized"]:
            url = folder["resource_url"] + "/releases?per_page=100"
            folder_name = folder["name"].replace('""', "")
            folder_data = call_discogs(url)
            releases = folder_data["releases"]

            release_strings = []
            for release in releases:
                release_strings.append(make_release_string(release))
            with open(output_file, "a") as f:
                f.write(make_markdown_block(folder_name, release_strings))
