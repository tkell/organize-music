import os

releases_path = "/Volumes/Music/Albums/"


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
    for filename in os.listdir(releases_path):
        filepath = os.path.join(releases_path, filename)
        if os.path.isdir(filepath):
            release_title = filename
            tracks = os.listdir(filepath)
            print(release_title)
            for track in tracks:
                if is_audio_file(track):
                    print("  " + track)

    print("\n" + "#Productions")
    for filename in os.listdir("/Volumes/Productions"):
        if is_audio_file(filename):
            print(filename)

    print("\n" + "#Tide Pool")
    for filename in os.listdir("/Volumes/Tide Pool"):
        if is_audio_file(filename):
            print(filename)
