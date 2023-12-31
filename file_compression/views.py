from django.views.decorators.csrf import csrf_exempt
import os
import gzip
from django.http import JsonResponse
from urllib.parse import quote

def provide_download(compressed_file_path, file_name):
    try:
        if os.path.exists(compressed_file_path):
            # Assuming MEDIA_URL is the base URL for your media files
            download_url = f'http://127.0.0.1:8000/static/{quote(file_name)}.gz'
            return download_url
        else:
            print("Compressed file not found.")
            return None
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return None

@csrf_exempt
def receive_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        save_directory = 'static/'  # Replace this with your desired directory

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        file_path = os.path.join(save_directory, uploaded_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        compressed_file_path = compress_file(file_path, uploaded_file.name)

        if compressed_file_path:
            download_url = provide_download(compressed_file_path, uploaded_file.name)
            if download_url:
                download_link = f'<a href="{download_url}" download="{uploaded_file.name}.gz">Download Compressed File</a>'
                return JsonResponse({'download_link': download_link})
            else:
                return JsonResponse({'error': 'Failed to generate download link'})
        else:
            return JsonResponse({'error': 'Failed to compress file'})
    else:
        return JsonResponse({'error': 'Invalid request'})

def compress_file(file_path, file_name):
    try:
        if os.path.exists(file_path):
            compressed_file_path = file_path + '.gz'
            with open(file_path, 'rb') as file:
                with gzip.open(compressed_file_path, 'wb') as compressed_file:
                    for line in file:
                        compressed_file.write(line)
            print(f"File '{file_name}' compressed successfully as '{file_name}.gz'")
            return compressed_file_path
        else:
            print("File not found.")
            return None
    except Exception as e:
        print(f"An error occurred during compression: {e}")
        return None
