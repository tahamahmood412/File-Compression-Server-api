import os
import gzip
from django.shortcuts import HttpResponse,render
from django.core.files.storage import FileSystemStorage
from .forms import FileUploadForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import quote


def provide_download(compressed_file_path, file_name):
    try:
        if os.path.exists(compressed_file_path):
            # Assuming MEDIA_URL is the base URL for your media files
            download_url = f'http://127.0.0.1:8000/static/{quote(file_name)}.gz'
            print(download_url)
            return download_url
        else:
            print("Compressed file not found.")
    except Exception as e:
        print(f"An error occurred during download: {e}")
    return None



@csrf_exempt
def receive_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Path where the files will be saved
        # save_directory = 'media/uploads/'  # Replace this with your desired directory
        save_directory = 'static/'  # Replace this with your desired directory

        # Check if the directory exists, create it if not
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Save the uploaded file to the specified location
        file_path = os.path.join(save_directory, uploaded_file.name)
        print(file_path)
        print(uploaded_file)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Compress the uploaded file
        print("Before: File name", file_path)
        print("Before: File Path",uploaded_file.name)
        compressed_file_path = compress_file(file_path, uploaded_file.name)
        print("After: File name",file_path)
        print("After: File Path",uploaded_file.name)
        print("COMPESSED FILE PATH",compressed_file_path)

        if compressed_file_path:
            # Provide the download URL for the compressed file
            download_url = provide_download(compressed_file_path, uploaded_file.name)
            print("Download Url" + download_url)
            if download_url:
                # Create a download link in HTML format
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
                    compressed_file.writelines(file)
            print(f"File '{file_name}' compressed successfully as '{file_name}.gz'")
            print("After Compression" + compressed_file_path)
            return compressed_file_path
            
        else:
            print("File not found.")
    except Exception as e:
        print(f"An error occurred during compression: {e}")
    return None



