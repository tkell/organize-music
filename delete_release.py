import argparse
import json
import sys

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("external_id", type=str, help="The release ID to delete")
    arg_parser.add_argument(
        "collection_name", type=str, help="The collection to delete from"
    )

    args = arg_parser.parse_args()
    external_id = int(args.external_id.strip())
    collection_name = args.collection_name.strip()

    # remove from json file
    json_file_name = f"{collection_name}.json"
    with open(json_file_name, "r") as json_file:
        all_releases = json.load(json_file)

    for release in all_releases:
        if release["id"] == external_id:
            print("About to remove entry from json file, y/n:")
            print(release)

            choice = input()
            if choice == "y":
                print("Removing from json file")
                all_releases.remove(release)
                with open(json_file_name, "w") as json_file:
                    json.dump(all_releases, json_file)
            else:
                print("Not removing, not re-saving file")

            sys.exit(0)
    print("Release not found!  Check the external_id and collection_name")
