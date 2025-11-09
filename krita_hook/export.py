import os
import shutil


def export_directory(source_dir, target_dir, target_exists=True, same_name=True):
    if same_name and os.path.basename(source_dir) != os.path.basename(target_dir):
        raise FileNotFoundError("Source and target directory names don't match")

    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

    if target_exists and not os.path.exists(target_dir):
        raise FileNotFoundError(f"Target directory must exist: {source_dir}")

    if os.path.exists(target_dir):
        try:
            shutil.rmtree(target_dir)
        except Exception as e:
            print(e)

    shutil.copytree(source_dir, target_dir)
