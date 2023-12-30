import os
import requests

# Get the directory path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "ebay.pdf"
file_path = os.path.join(current_dir, file_name)

def send_file(file_path):
    url = 'http://127.0.0.1:8000/receive_file/'  # Replace with your server's URL

    with open(file_path, 'rb') as file:
        files = {'file': file}

        try:
            response = requests.post(url, files=files)
            if response.status_code == 200:
                print(response)
                print("File sent successfully!")
            else:
                print(f"Failed to send file. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_file(file_path)
