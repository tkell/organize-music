import os
from collections import defaultdict
from urllib.parse import urlparse

import lib_discogs


if __name__ == "__main__":
    albums_dir = "/Volumes/Music/Albums"
    folders = os.listdir(albums_dir)

    debug_count = 50
    counts = defaultdict(int)
    for folder in folders:
        if counts["total"] >= debug_count:
            break

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
                            counts["tracks file is not on discogs"] += 1
                        else:
                            hostname = urlparse(album_source_url).hostname
                            key = "tracks file is at " + hostname
                            counts[key] += 1

            if not cover_flag and not tracks_file_flag:
                counts["no cover or no tracks"] += 1

    print(counts)
