import shutil
import zipfile
from pureml.schema import PredictSchema
import os


# def zip_content(src_path, dst_path):
#     print(src_path)
#     ignore_patterns = shutil.ignore_patterns(".pureml", "*.venv", "*.pyc")

#     # Create a zip archive of the folder
#     shutil.make_archive(
#         base_dir=src_path,
#         root_dir=src_path,
#         format=PredictSchema().resource_format,
#         base_name=dst_path,
#         ignore=ignore_patterns,
#     )


def zip_content(src_path, dst_path):

    # folder_path = '.'
    # zip_path = '/path/to/zipfile.zip'
    folders_to_ignore = PredictSchema().folders_to_ignore  # ["./.pureml", "./.venv"]

    # Create a zip archive of the folder, excluding the specified folder
    with zipfile.ZipFile(dst_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(src_path):
            for file in files:
                file_path = os.path.join(root, file)
                # print("ignored", file_path)
                if not any(
                    file_path.startswith(folder) for folder in folders_to_ignore
                ):
                    zip_file.write(file_path, file_path)
                    print(file_path)


def unzip_content(src_path, dst_path):
    shutil.unpack_archive(src_path, dst_path, format=PredictSchema().resource_format)

    # Delete the zip file
    # os.remove(src_path)
