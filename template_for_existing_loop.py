import argparse
import os

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("albums_dir")
    arg_parser.add_argument("break_after")
    args = arg_parser.parse_args()
    albums_dir = args.albums_dir
    break_after = int(args.break_after)
    folders = os.listdir(albums_dir)

    count = 0
    for folder in folders:
        if folder.startswith("."):
            continue
        folder_path = os.path.join(albums_dir, folder)

        try:
            pass

        except Exception as e:
            print(f"Error processing {folder_path}: {e}")

        count += 1
        if count >= break_after:
            break
