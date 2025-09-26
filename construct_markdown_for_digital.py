import argparse
import json

def is_audio_file(filename):
    if (
        filename.endswith(".mp3")
        or filename.endswith(".wav")
        or filename.endswith(".flac")
        or filename.endswith(".m4a")
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    args = parser.parse_args()
    source_file = args.source_file

    with open(source_file, "r") as f:
        releases = json.load(f)
    for release in releases:
        release_string = (
            f"{release['artist']} - {release['title']} [{release['label']}]"
        )
        print(release_string)
        for track in release["tracks"]:
            track_string = f"  {track['position']} - {track['title']}"
            print(track_string)
