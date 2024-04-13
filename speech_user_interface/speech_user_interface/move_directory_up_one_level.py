import os
import shutil


def move_directory_up_one_level(dir_path):
    # Get the absolute path of the directory to ensure accuracy
    dir_path = os.path.abspath(dir_path)

    # Calculate the parent directory (i.e., one level up)
    parent_dir = os.path.dirname(dir_path)
    target_dir = os.path.join(
        os.path.dirname(parent_dir), os.path.basename(dir_path)
    )

    # Moving the directory
    shutil.move(dir_path, target_dir)
    print(f"Moved '{dir_path}' to '{target_dir}'")
