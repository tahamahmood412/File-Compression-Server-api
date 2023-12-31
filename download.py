import os
import requests
import shutil
import gzip

def download_file(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open('downloaded_file.gz', 'wb') as file:
                # Write the content directly to the file in chunks
                shutil.copyfileobj(response.raw, file)
            print("File downloaded successfully.")

            # Check if the downloaded file is a valid Gzip file
            try:
                with gzip.open('downloaded_file.gz', 'rb') as test_file:
                    test_file.read(2)  # Attempt to read to check for Gzip validity
                    print("File is a valid Gzip file.")
            except gzip.BadGzipFile:
                print("Downloaded file is not a valid Gzip file.")
                os.remove('downloaded_file.gz')  # Remove the downloaded file
        else:
            print("Failed to download the file")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_url = 'http://127.0.0.1:8000/static/ebay.pdf.gz'
download_file(file_url)
