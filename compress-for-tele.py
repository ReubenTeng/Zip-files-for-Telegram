import os
import sys
import zipfile


def compress_and_split_photos(input_folder, output_folder, max_size_mb=2000):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize variables
    current_zip_file = None
    current_size = 0
    zip_counter = 1

    # Loop through the photos in the input folder
    for root, _, files in os.walk(input_folder):
        print("Processing folder:", root)
        length = len(files)
        for index, file in enumerate(files):
            if (index + 1) % 5 == 0:
                # print loading bar
                sys.stdout.write("\r")
                sys.stdout.write(
                    f"[{'=' * int((index + 1) / length * 100):<100}] {index + 1}/{length}"
                )
                sys.stdout.flush()
            # check if the file is a photo
            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            file_path = os.path.join(root, file)

            # Get the size of the file in MB
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

            # If adding this file would exceed the maximum size, create a new zip file
            if current_zip_file is None or (current_size + file_size_mb) > max_size_mb:
                print("Creating new zip file:", current_zip_file)
                current_zip_file = os.path.join(
                    output_folder, f"photos_{zip_counter}.zip"
                )
                current_size = 0
                zip_counter += 1

            # Add the file to the current zip file
            with zipfile.ZipFile(current_zip_file, "a") as zip_file:
                zip_file.write(file_path, os.path.relpath(file_path, input_folder))

            current_size += file_size_mb

    print("Compression and splitting completed successfully.")


if __name__ == "__main__":
    # get flag from sys.argv for upload to telegram
    input_folder = input("Enter the path to the folder containing the photos: ")
    output_folder = input("Enter the path to the output folder: ")
    max_size_mb = int(input("Enter the maximum size of each zip file in MB: "))
    max_size_mb = max_size_mb if max_size_mb and max_size_mb > 0 else 2000
    compress_and_split_photos(input_folder, output_folder, max_size_mb)
