#!/usr/bin/python3

import argparse
import zipfile
import os

class FileToDeleteNotFoundError(Exception):
    pass

class FileToAddNotFoundError(Exception):
    pass

class FileToAddAlreadyExistsError(Exception):
    pass

parser = argparse.ArgumentParser(description='Replaces files in a zip archive')

parser.add_argument('-i', '--input', metavar='archive', help='Original zip file')
parser.add_argument('-d', '--delete', metavar='file', default=[], type=str, nargs='+', help='The files that will be removed from the archive')
parser.add_argument('-a', '--append', metavar='file', default=[], type=str, nargs='+', help='The files that will be added into the archive')
parser.add_argument('-o', '--output', metavar='output_file', required=True, help='The zip file that will be created')

args = parser.parse_args()


def modify_zip_archive(zip_file_path, files_to_delete, files_to_add, new_zip_file_path):
    # Create a new zip file to write to

    with zipfile.ZipFile(new_zip_file_path, mode='w') as new_zip_file:
        # Open the original zip file in read mode
        with zipfile.ZipFile(zip_file_path, mode='r') as zip_file:
            # Copy all files except the ones to remove to the new zip file
            remaining_files = []
            for item in zip_file.infolist():
                if item.filename not in files_to_delete:
                    new_zip_file.writestr(item, zip_file.read(item.filename))
                    remaining_files.append(item.filename)

            # Check that the files to add exist, and that they don't already exist in the archive
            for file_path in files_to_add:
                if not os.path.isfile(file_path):
                    raise FileToAddNotFoundError(f'The file to add "{file_path}" does not exist')
                if os.path.basename(file_path) in remaining_files:
                    raise FileToAddAlreadyExistsError(f'The file to add "{file_path}" already exists in the archive')

                # Add the new files to the new zip file
                new_zip_file.write(file_path)

    # Replace the original zip file with the new one
    os.replace(new_zip_file_path, zip_file_path)

try:
    remaining_files = modify_zip_archive(args.input, args.delete, args.append, args.output)
except FileToDeleteNotFoundError as e:
    print(f'Error: {e}')
except FileToAddNotFoundError as e:
    print(f'Error: {e}')
except FileToAddAlreadyExistsError as e:
    print(f'Error: {e}')
