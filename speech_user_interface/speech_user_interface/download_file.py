import requests
from tqdm import tqdm


def download_file(url, filename):
    """
    Download a file from a URL and save it to a local file with a progress bar.

    Args:
    url (str): The URL of the file to download.
    filename (str): The path to which the file should be saved locally.
    """
    try:
        # Send a HTTP request to the URL
        response = requests.get(url, stream=True)

        # Raise an exception if the request returned an unsuccessful status code
        response.raise_for_status()

        # Get the total file size from the header of the response
        total_size = int(response.headers.get("content-length", 0))

        # Open the local file for writing in binary mode
        with open(filename, "wb") as f, tqdm(
            desc=filename,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:

            # Iterate over the response data in chunks
            for chunk in response.iter_content(chunk_size=8192):
                # Write the data chunk to the local file
                f.write(chunk)
                # Update the progress bar
                bar.update(len(chunk))

        print(f"File downloaded successfully: {filename}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
