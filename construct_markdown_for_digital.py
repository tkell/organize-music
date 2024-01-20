import json
import os


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
    print("#Releases")
    with open("digital.json", "r") as f:
        releases = json.load(f)
    for release in releases:
        release_string = (
            f"{release['artist']} - {release['title']} [{release['label']}]"
        )
        print(release_string)
        for track in release["tracks"]:
            track_string = f"  {track['position']} - {track['title']}"
            print(track_string)

    print("\n" + "#Productions")
    for filename in os.listdir("/Volumes/Mimir/Productions"):
        if is_audio_file(filename):
            print(filename)

    print("\n" + "#Tide Pool")
    for filename in os.listdir("/Volumes/Mimir/Tide Pool"):
        if is_audio_file(filename):
            print(filename)
