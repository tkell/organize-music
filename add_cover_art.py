import os
from collections import defaultdict
from urllib.parse import urlparse

import lib_discogs
import discogs_album_search


if __name__ == "__main__":
    albums_dir = "/Volumes/Music/Albums"
    folders = os.listdir(albums_dir)
    print("listed directories")

    counts = defaultdict(int)
    for folder in folders:
        cover_flag = False
        tracks_file_flag = False
        dir_path = os.path.join(albums_dir, folder)
        if os.path.isdir(dir_path):
            filenames = os.listdir(dir_path)
            counts["total"] += 1

            for filename in filenames:
                if filename.lower() == "cover.jpg" or filename.lower() == "cover.png":
                    cover_flag = True
                    counts["cover art exists"] += 1
                elif filename.endswith(".tracks"):
                    tracks_file_flag = True
                    counts["tracks file exists"] += 1
                    tracks_file_path = os.path.join(albums_dir, folder, filename)
                    with open(tracks_file_path) as f:
                        album_source_url = f.readline().strip()
                        if album_source_url == "not-on-discogs":
                            counts[
                                "tracks file is not on discogs or anywhere else"
                            ] += 1
                        else:
                            try:
                                hostname = urlparse(album_source_url).hostname
                                key = "tracks file is at " + hostname
                                counts[key] += 1
                            except TypeError:
                                print("an error", folder)

            if not cover_flag and not tracks_file_flag:
                counts["no cover or no tracks"] += 1
                print(folder)

                artist = folder.split(" - ")[0].strip()
                if artist == "Various Artists":
                    artist = "Various"  # discogs!

                album_and_label = folder.split(" - ")[-1].strip()
                album = album_and_label.split("[")[0].strip()
                label = album_and_label.split("[")[1].strip().replace("]", "")
                discogs_url = discogs_album_search.search(artist, album, label)

                folder_path = os.path.join(albums_dir, folder)
                num_tracks = len(os.listdir(folder_path))
                tracks_filename = os.path.join(folder_path, f"{num_tracks}.tracks")
                print(f"here's our discogs url: {discogs_url}")
                with open(tracks_filename, "w") as f:
                    f.write(discogs_url)
    print(counts)
