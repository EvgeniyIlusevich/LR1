import os
import zipfile

def archive_file(filename):
    zip_name = get_path_to_file()

    with zipfile.ZipFile(zip_name, 'w') as zip_archive:
        zip_archive.write(filename, arcname=os.path.basename(filename))

    with zipfile.ZipFile(zip_name, 'r') as zip_archive:
        info = zip_archive.getinfo(os.path.basename(filename))
        return {
            "filename": info.filename,
            "size": info.file_size,
            "compress_size": info.compress_size
        }


def save_results_to_file(filename, results):
    with open(filename, "w") as file:
        for result in results:
            file.write(f"{result}\n\n")


def get_path_to_file():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'result.zip')