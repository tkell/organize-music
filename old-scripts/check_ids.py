import json
import sys

if __name__ == "__main__":
    filepath = sys.argv[1]
    with open(filepath) as f:
        all_data = json.load(f)

    ids = {}
    for d in all_data:
        new_id = d["id"]
        if new_id in ids:
            print("DUPLICATE IDS FOUND")
            print(d)
            print(ids[new_id])
        else:
            ids[new_id] = d
