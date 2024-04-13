import zipfile
import os
from tqdm import tqdm


def unzip_file(zip_path, extract_to, chunk_size=1024):
    """
    Unzip a ZIP file to a specified directory with a progress bar that updates every n bytes.

    Args:
    zip_path (str): The path to the ZIP file.
    extract_to (str): The directory to extract the files into.
    chunk_size (int): Number of bytes to process before updating the progress bar.
    """
    try:
        # Ensure the target directory exists
        os.makedirs(extract_to, exist_ok=True)

        print("tying to open zip file:", zip_path)
        # Open the zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            print("calculating the total zip size")
            # Get the total size of all files in the archive
            total_size = sum(zinfo.file_size for zinfo in zip_ref.infolist())
            print("total_size:", total_size)

            # Initialize the progress bar
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc="Extracting files",
            ) as bar:
                # Iterate over each file in the zip archive
                for zinfo in zip_ref.infolist():
                    # Extract the file in chunks
                    with zip_ref.open(zinfo) as file, open(
                        os.path.join(extract_to, zinfo.filename), "wb"
                    ) as f_out:
                        while True:
                            chunk = file.read(chunk_size)
                            if not chunk:
                                break
                            f_out.write(chunk)
                            bar.update(len(chunk))

            print(f"Files have been extracted to: {extract_to}")
    except zipfile.BadZipFile:
        print("Error: The file is a bad zip file and cannot be extracted.")
    except Exception as e:
        print(f"An error occurred: {e}")
