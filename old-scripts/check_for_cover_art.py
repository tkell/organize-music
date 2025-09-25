import os
import sys

if __name__ == "__main__":
    folder = sys.argv[1]
    info_file = "info.json"

    for filename in os.listdir(folder):
        old_file_path = os.path.join(folder, filename)
        if not os.path.isdir(old_file_path):
            continue

        jpg_path = os.path.join(old_file_path, "cover.jpg")
        png_path = os.path.join(old_file_path, "cover.png")
        if not os.path.isfile(jpg_path) and not os.path.isfile(png_path):
            print(f"No cover art at {filename}")
