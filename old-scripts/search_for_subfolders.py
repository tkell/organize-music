import os
# find all folders that have subfolders:
base_folder = "/Volumes/Mimir/Music/Albums"

for filename in os.listdir(base_folder):
    if os.path.isdir(os.path.join(base_folder, filename)):
        subfolders = [f for f in os.listdir(os.path.join(base_folder, filename)) if os.path.isdir(os.path.join(base_folder, filename, f))]
        if len(subfolders) > 0:
            print(filename)
            print(subfolders)
            print("\n")
