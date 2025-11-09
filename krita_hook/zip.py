import os
import zipfile


def zip_directory(folder_path, zip_path, ignored=None):
    folder_path = os.path.abspath(os.path.normpath(folder_path))
    zip_path = os.path.abspath(zip_path)

    if os.path.exists(zip_path) and os.path.isfile(zip_path):
        os.remove(zip_path)


    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            if ignored and root in ignored:
                continue

            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
