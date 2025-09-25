import os
import sys
import shutil

if __name__ == "__main__":
    folder = sys.argv[1]

    for filename in os.listdir(folder):
        old_file_path = os.path.join(folder, filename)
        if not os.path.isdir(old_file_path) and "[" in filename:
            print(filename)
            new_folder, extension = filename.split(".")
            new_folder_path = os.path.join(folder, new_folder)
            os.mkdir(new_folder_path)
            print("folder made ...")

            new_filename = filename.split("[")[0].strip() + '.' + extension
            new_file_path = os.path.join(new_folder_path, new_filename)
            shutil.copy(old_file_path, new_file_path)
            print("copied!")
