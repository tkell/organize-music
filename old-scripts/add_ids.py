import hashlib
import os
import sys
import json

if __name__ == "__main__":
    folder = sys.argv[1]
    info_file = "info.json"

    for filename in os.listdir(folder):
        old_file_path = os.path.join(folder, filename)
        if not os.path.isdir(old_file_path):
            continue

        print("----")
        print(filename)
        new_path = os.path.join(old_file_path, info_file)
        with open(new_path) as f:
            info = json.load(f)
        if info.get("id"):
            print(".")
            continue

        # this is the same as the 'real' organize music code,
        # so I could probably abstract things a bit if I wanted to!
        m = hashlib.sha256()
        m.update(new_path.encode("utf-8"))
        id_int = int(m.hexdigest()[0:8], 16)
        print(id_int)

        info["id"] = id_int
        with open(new_path, 'w') as f:
            json.dump(info, f)
