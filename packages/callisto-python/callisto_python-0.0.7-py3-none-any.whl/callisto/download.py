import os

import requests
import tqdm  # type: ignore


def download_file(
    url, destination=None, overwrite=False, progress_bar=True, quiet=False
):
    """This method downloads the given URL to a local file.

    :param url: The URL to download (required)
    :param destination: The filename where the file will be download.
    If this value is `None`, the filename is taken from the last component of
    the URL.  (Default = None)
    :param overwrite: If this value is true, the URL will always be downloaded.
    If false, the URL won't be downloaded if the destination file already
    exists.  (Default = False)
    :param progress_bar: When true, show a tqdm style progress bar during
    download.  (Default = True)
    :param quiet: When true, suppress status messages.  (Default = False)
    """

    if destination is None:
        local_filename = url.split("/")[-1]
        destination = os.path.join(os.getcwd(), local_filename)

    if os.path.exists(destination) and overwrite is False:
        if not quiet:
            print(f"Skipping download -- {destination} already exists.")
        return
    else:
        if not quiet:
            print(f"Downloading {url} to {destination}.")
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte

    if progress_bar:
        tqdm_bar = tqdm.tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    with open(destination, "wb") as file:
        for data in response.iter_content(block_size):
            if progress_bar:
                tqdm_bar.update(len(data))
            file.write(data)
    if progress_bar:
        tqdm_bar.close()
